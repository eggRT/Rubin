from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length = 200)
	textPost = models.TextField()
	imagePost = models.ImageField(blank = True, null=True, upload_to='images/')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("detailArticle", kwargs={"pk": self.pk})

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	descript = models.CharField(max_length = 250)
	profilePic = models.ImageField(null = True, blank = True, upload_to= 'profile/', default='images/chelovek.jpg')
	link = models.CharField(max_length =255, null=True, blank=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.profilePic.path)

		if img.height > 300 or img.weight >300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.profilePic.path)

	def __str__(self):
		return str(self.user)

	def get_absolute_url(self):
		return reverse('home')

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	content = models.TextField(max_length = 200)
	timestamp = models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return '{}-{}'.format(self.post.title, str(self.user.username))

	def datepublished(self):
		return self.timestamp.strftime('%Y')

	def get_absolute_url(self):
		return reverse("detailArticle", kwargs={"id": self.id})