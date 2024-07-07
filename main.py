import telebot
import psycopg2
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('7325864976:AAFqOW2OFlWgZOIv-6Q90QloMBlT9Mqfpvo')
BOT_TOKEN = '7325864976:AAFqOW2OFlWgZOIv-6Q90QloMBlT9Mqfpvo'
APP_URL = 'https://brandonline-7b6bec56d5d1.herokuapp.com/' + BOT_TOKEN

# Подключение к базе данных
conn = psycopg2.connect(host='localhost',dbname='brand',user='postgres',password='arnur',port=5432)
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    telegram_name = message.from_user.username
    cursor.execute("""
        INSERT INTO users (telegram_name) 
        VALUES (%s) 
        ON CONFLICT (telegram_name) DO NOTHING
        RETURNING id, created_at
    """, (telegram_name,))
    user = cursor.fetchone()
    conn.commit()
    if user:
        user_id, created_at = user
        print(f'New user created: ID={user_id}, created_at={created_at}')
    else:
        print('User already exists')
    bot.reply_to(message, 'Добро пожаловать! Используйте команду /test для начала теста.')
    
@bot.message_handler(commands=['test'])
def send_test_list(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    cursor.execute("SELECT id, name FROM tests")
    tests = cursor.fetchall()
    for test in tests:
        markup.add(KeyboardButton(f"Тест {test[0]}: {test[1]}"))
    bot.send_message(message.chat.id, 'Выберите тест:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.startswith('Тест'))
def handle_test_selection(message):
    test_id = int(message.text.split()[1].rstrip(':'))
    cursor.execute("SELECT id, question_text FROM questions WHERE test_id = %s", (test_id,))
    questions = cursor.fetchall()
    context = {'questions': questions, 'current_question': 0, 'test_id': test_id, 'telegram_name': message.from_user.username}
    ask_question(message.chat.id, context)

def ask_question(chat_id, context):
    question = context['questions'][context['current_question']]
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    cursor.execute("SELECT id, option_text FROM options WHERE question_id = %s", (question[0],))
    options = cursor.fetchall()
    for option in options:
        markup.add(KeyboardButton(option[1]))
    bot.send_message(chat_id, question[1], reply_markup=markup)
    context['question_id'] = question[0]
    bot.register_next_step_handler_by_chat_id(chat_id, process_answer, context)

def process_answer(message,context):
    selected_option = message.text
    time = datetime.fromtimestamp(message.date)
    cursor.execute('SELECT correct_answer FROM questions WHERE id = %s',(context['question_id'],))
    correct_answer = cursor.fetchone()[0]
    is_correct = (selected_option==correct_answer)

    cursor.execute('SELECT id FROM users WHERE telegram_name = %s',(context['telegram_name'],))
    user_id = cursor.fetchone()[0]
    context['user_id'] = user_id

    cursor.execute('INSERT INTO user_answer(user_id,question_id,selected_option,is_correct,answered_at) VALUES(%s,%s,%s,%s,%s)' ,(user_id,context['question_id'],selected_option,is_correct,time))
    conn.commit()
    context['current_question'] += 1
    if context['current_question'] < len(context['questions']):
        ask_question(message.chat.id,context)
    else:
        completed_time = datetime.fromtimestamp(message.date)
        calculate_score(message.chat.id,context,completed_time)

def calculate_score(chat_id, context, completed_time):
    # Проверка правильности ID пользователя и теста
    user_id = context.get('user_id')
    test_id = context.get('test_id')
    if not user_id or not test_id:
        bot.send_message(chat_id, 'Ошибка: не удалось получить ID пользователя или теста.')
        return

    # Подсчет количества правильных ответов
    cursor.execute("""
        SELECT COUNT(*)
        FROM user_answer
        WHERE user_id = %s AND question_id IN (
            SELECT id FROM questions WHERE test_id = %s
        ) AND is_correct = TRUE
    """, (user_id, test_id))
    correct_answers = cursor.fetchone()[0]

    # Вставка результатов в таблицу UserPerformance
    cursor.execute("""
        INSERT INTO user_performance (user_id, test_id, score, completed_at)
        VALUES (%s, %s, %s, %s)
    """, (user_id, test_id, correct_answers, completed_time))
    conn.commit()

    # Отправка сообщения с результатами
    bot.send_message(chat_id, f'Тест завершен! Ваш результат: {correct_answers} правильных ответов.')

# # Обработчик команды /results
@bot.message_handler(commands=['results'])
def send_results(message):
    telegram_name = message.from_user.username
    cursor.execute("SELECT test_id, score, completed_at FROM user_performance WHERE user_id = (SELECT id FROM users WHERE telegram_name = %s)", (telegram_name,))
    results = cursor.fetchall()
    response = "Ваши результаты:\n"
    for result in results:
        response += f"Тест ID: {result[0]}, Баллы: {result[1]}, Дата: {result[2]}\n"
    bot.send_message(message.chat.id, response)

bot.infinity_polling()