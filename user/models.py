from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20)
    uuid = models.CharField(max_length=36)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=11)
    student_code = models.CharField(null=True, blank=True, max_length=20)
    is_updated = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_submitted = models.DateTimeField(blank=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        db_table = 'user'

    def __str__(self):
        return self.username
