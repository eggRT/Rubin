from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
	title = models.CharField(max_length = 200)
	textPost = models.TextField()
	imagePost = models.ImageField(blank = True, null=True, upload_to='images/')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title