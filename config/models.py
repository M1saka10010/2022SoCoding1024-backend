# Create your models here.
from django.db import models


# Create your models here.


class Site(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField()

    class Meta:
        verbose_name = "站点配置"
        verbose_name_plural = verbose_name
        db_table = 'config'

    def __str__(self):
        return self.key
