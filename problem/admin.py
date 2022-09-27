from django.contrib import admin

from . import models


# Register your models here.

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'template', 'description', 'tips', 'is_display', 'pass_count')
    list_display_links = ('id', 'title', 'description', 'tips')


admin.site.register(models.Problem, ProblemAdmin)


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem_id', 'user_id', 'answer', 'is_correct', 'submit_time')
    list_display_links = ('id', 'answer')


admin.site.register(models.Solution, SolutionAdmin)


class CorrectLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem_id', 'user_id', 'solution_id', 'attempt_times', 'submit_time')
    list_display_links = ('id', 'solution_id')


admin.site.register(models.CorrectLog, CorrectLogAdmin)
