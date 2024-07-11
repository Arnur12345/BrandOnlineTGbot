# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Options(models.Model):
    id = models.BigIntegerField(primary_key=True)
    question = models.ForeignKey('Questions', models.DO_NOTHING)
    option_text = models.TextField()

    class Meta:
        managed = False
        verbose_name_plural = 'Options'
        db_table = 'options'


class Questions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    test = models.ForeignKey('Tests', models.DO_NOTHING)
    question_text = models.TextField()
    correct_answer = models.TextField()

    class Meta:
        managed = False
        verbose_name_plural = 'Questions'
        db_table = 'questions'


class Subject(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField()
    def __str__(self):
        return self.name

    class Meta:
        managed = False
        verbose_name_plural = 'Subject'
        db_table = 'subject'


class Tests(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField()
    subject = models.ForeignKey(Subject, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        verbose_name_plural = 'Tests'
        db_table = 'tests'


class UserAnswer(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    question = models.ForeignKey(Questions, models.DO_NOTHING)
    selected_option = models.TextField()
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField()

    class Meta:
        managed = False
        verbose_name_plural = 'User Answer'
        db_table = 'user_answer'


class UserPerformance(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    test = models.ForeignKey(Tests, models.DO_NOTHING)
    score = models.BigIntegerField()
    completed_at = models.DateTimeField()

    
    class Meta:
        managed = False
        db_table = 'user_performance'


class Users(models.Model):
    id = models.BigIntegerField(primary_key=True)
    telegram_name = models.TextField(unique=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        verbose_name_plural = 'Users'
        db_table = 'users'
