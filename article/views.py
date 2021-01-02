from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Post, Comment
from .forms import postForm, commentForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

class HomeView(ListView):
	model = Post
	template_name = 'home.html'

def detailPost(request, pk):
	post = get_object_or_404(Post, id=pk)
	comments = Comment.objects.filter(post=post)

	if request.method == "POST":
		comment_form = commentForm(request.POST or None)
		if comment_form.is_valid():
			content = request.POST.get('content')
			comment = Comment.objects.create(post=post, user=request.user, content=content)
			comment.save()
			return HttpResponseRedirect(post.get_absolute_url())
	else:
		comment_form =commentForm

	context = {
		'post': post,
		'comments': comments,
		'comment_form': comment_form,
	}
	return render(request, 'detailArticle.html', context)


class CreatePostView(CreateView):
	model = Post
	template_name = 'add_post.html'
	form_class = postForm
	success_url = reverse_lazy('home')

class EditPostView(UpdateView):
	model = Post
	template_name = 'edit_post.html'
	form_class = postForm
	success_url = reverse_lazy('home')