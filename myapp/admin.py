from django.contrib import admin
from .models import Users, Subject, Tests, Questions, Options, UserAnswer, UserPerformance

# Register your models here.
admin.site.register(Users)
admin.site.register(Subject)
admin.site.register(Tests)
admin.site.register(Questions)
admin.site.register(Options)
admin.site.register(UserAnswer)
admin.site.register(UserPerformance)