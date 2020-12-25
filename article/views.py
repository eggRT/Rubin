from django.views.generic import ListView, CreateView
from .models import Post
from .forms import postForm
from django.urls import reverse_lazy

class HomeView(ListView):
	model = Post
	template_name = 'home.html'

class CreatePostView(CreateView):
	model = Post
	template_name = 'add_post.html'
	form_class = postForm
	success_url = reverse_lazy('home')