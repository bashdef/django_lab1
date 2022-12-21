from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    life_time = models.DateTimeField(default=datetime.now() + timedelta(days=1), verbose_name='Время жизни', null=False)
    votes = models.IntegerField(default=0)
    img = models.ImageField(null=True, default='default.jpg', upload_to='images/question')
    description = models.TextField(max_length=600, null=True)
    description2 = models.TextField(max_length=600, null=True)

    def was_published_recently(self):
        return self.pub_date >= datetime.now() - timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def percentage(self):
        all_votes = Choice.objects.all()
        votes_count = 0
        for obj in all_votes:
            votes_count += obj.votes
        if self.votes != 0:
            return round((self.votes / votes_count) * 100)
        else:
            return 0

    def __str__(self):
        return self.choice_text
