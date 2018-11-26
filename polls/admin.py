from django.contrib import admin

from django.contrib import admin

from .models import Question

from django.contrib import admin

from .models import Choice, Question, Comments


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

    inlines = [ChoiceInline]

    list_display = ('question_text', 'pub_date', 'was_published_recently')

    list_filter = ['pub_date']

    search_fields = ['question_text']


class AdminQuestion(admin.ModelAdmin):

     pass

admin.site.register(Question, QuestionAdmin)
admin.site.register(Comments, AdminQuestion)
