from django.db import models

from django.core.validators import URLValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)


class Post(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    body = models.TextField()
    image_url = models.CharField(null=True, max_length=1999, validators=[URLValidator()])
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')


class Comments(models.Model):
    author = models.CharField(max_length=100)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)