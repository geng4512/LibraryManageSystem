from django.db import models

# Create your models here.
class BOOKS(models.Model):
    ISBN = models.CharField(max_length = 13, primary_key = True)
    NAME = models.CharField(max_length = 50)
    AUTHOR = models.CharField(max_length = 50)
    PUBLISHING_HOUSE = models.CharField(max_length = 50)
    NUM = models.IntegerField()

class READER(models.Model):
    ACCOUNT = models.CharField(max_length = 20, primary_key = True)
    PASSWORD = models.CharField(max_length = 300)
    NAME = models.CharField(max_length = 50)

class BORROR(models.Model):
    ISBN = models.ForeignKey(BOOKS, on_delete = models.CASCADE)
    ACCOUNT = models.ForeignKey(READER, on_delete = models.CASCADE)
    DEADLINE = models.DateField()

class REVIEW(models.Model):
    ISBN = models.ForeignKey(BOOKS, on_delete = models.CASCADE)
    ACCOUNT = models.ForeignKey(READER, on_delete = models.CASCADE)
    SCORE = models.IntegerField()
    COMMENT = models.CharField(max_length = 300)

