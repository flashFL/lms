#coding = utf-8
from django.db import models

# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=64)
    author = models.CharField(max_length=32)
    publisher = models.CharField(max_length=64)
    def __unicode__(self):
        return '%s--%s--%s' % (self.book_name, self.author, self.publisher)


class User(models.Model):
    user_name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    last_time = models.DateTimeField()