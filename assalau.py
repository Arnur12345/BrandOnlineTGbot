import requests
from bs4 import BeautifulSoup

google_form_link = 'https://docs.google.com/forms/d/e/1FAIpQLSfS9naslAOcEnD6_es0aTnTmEGwsl1fw3VemqwM4ubq8NopDA/viewform?usp=sf_link'

# Fetch Google Form data
response = requests.get(google_form_link)
response.raise_for_status()
soup = BeautifulSoup(response.content, 'html.parser')

# Extract questions and options
form_fields = soup.find_all('div', {'role': 'listitem'})

questions_data = []

for field in form_fields:
    # Extract question text
    question_title = field.find('div', {'role': 'heading'})
    if question_title:
        question_text = question_title.text.strip()
        
        # Extract options
        options = []
        option_fields = field.find_all('span', {'role': 'presentation'})
        for opt in option_fields:
            if opt.text.strip() != '':
                options.append(opt.text.strip())
        
        # Assuming there is no direct way to find correct answers, just collect questions and options
        questions_data.append({
            'question': question_text,
            'options': options,
            'correct_answer': "Not Available"
        })

# Print extracted data
for data in questions_data:
    print(f"Question: {data['question']}")
    for option in data['options']:
        print(f"Option: {option}")
    print(f"Correct Answer: {data['correct_answer']}")
    print()
