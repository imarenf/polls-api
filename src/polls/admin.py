from django.contrib import admin

from .models import Poll, Question


class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'context')
    list_display_links = ('title',)
    search_fields = ('title', 'context')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text',)
    list_display_links = ('question_text',)


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
