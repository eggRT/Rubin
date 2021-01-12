from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse
from ckeditor.fields import RichTextField
from slugify import slugify

class Tag(models.Model):
	title = models.CharField(max_length=60, verbose_name= 'Tag')
	slug = models.SlugField(null=False, unique=True)

	class Meta:
		verbose_name='tag'
		verbose_name_plural='tags'

	def get_absolute_url(self):
		return reverse('tags', args=[self.slug])

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)

class favoriteTag(models.Model):
	userOp = models.ForeignKey(User, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, related_name='tagsFav')

class Post(models.Model):
	textPost = models.TextField()
	imagePost = models.ImageField(blank = True, null=True, upload_to='images/')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	likes = models.ManyToManyField(User, related_name='blog_posts')
	dislikes = models.ManyToManyField(User, related_name='dislikes_posts')
	tags = models.ManyToManyField(Tag, related_name='tags')

	def datepublished(self):
		return self.date.strftime('%Y %B %d')

	def total_likes(self):
		return self.likes.count()

	def total_dislikes(self):
		return self.dislikes.count()

	def __str__(self):
		return self.textPost

	def get_absolute_url(self):
		return reverse("detailArticle", args=[str(self.id)])

def get_image_filename(instance, filename):
	id = instance.post.id
	return "post_images/%s" % (id)


class Images(models.Model):
	post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
	image = models.ImageField(upload_to = 'images/')

class storyViews(models.Model):
	post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null = True, on_delete= models.CASCADE)
	date = models.DateTimeField(auto_now_add= True)

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	descript = models.CharField(max_length = 250)
	profilePic = models.ImageField(null = True, blank = True, upload_to= 'profile/', default='images/chelovek.jpg')
	link = models.CharField(max_length =255, null=True, blank=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.profilePic.path)
		print(img.format)

		if img.format == 'JPEG':
			if img.height > 300 or img.weight >300:
				output_size = (300,340)
				img.thumbnail(output_size)
				img.save(self.profilePic.path)
		else:
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
