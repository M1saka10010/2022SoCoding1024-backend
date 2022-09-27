from django.db import models


# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=100)
    template = models.IntegerField(default=0)
    description = models.TextField()
    tips = models.TextField()
    is_display = models.BooleanField(default=False)
    solution = models.CharField(max_length=100)
    pass_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "题目"
        verbose_name_plural = verbose_name
        db_table = 'problem'

    def __str__(self):
        return self.title


class Solution(models.Model):
    problem_id = models.IntegerField()
    user_id = models.IntegerField()
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    submit_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "提交记录"
        verbose_name_plural = verbose_name
        db_table = 'solution'

    def __str__(self):
        return self.answer


class CorrectLog(models.Model):
    problem_id = models.IntegerField()
    user_id = models.IntegerField()
    solution_id = models.IntegerField()
    submit_time = models.DateTimeField(auto_now_add=True)
    attempt_times = models.IntegerField()

    class Meta:
        verbose_name = "正确提交记录"
        verbose_name_plural = verbose_name
        db_table = 'correct_log'

    def __str__(self):
        return self.solution_id
