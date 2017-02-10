from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)
    views= models.IntegerField(default=0)
    likes= models.IntegerField(default=0)
    slug= models.SlugField(unique=True)
    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        super(Category,self).save(*args,**kwargs)
    class Meta:
        verbose_name_plural="Categories"
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Page(models.Model):
    category=models.ForeignKey(Category)
    title=models.CharField(max_length=128)
    url=models.URLField()
    views=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural="Pages"
    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
class UserProfile(models.Model):
    user=models.OneToOneField(User)
    website=models.URLField(blank=True)
    picture=models.ImageField(upload_to='profile_images')
    def __str__(self):
        return self.user.username
    def __unicode__(self):
        return self.user.username
