from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Post, Comment, Images, Profile, storyViews, Tag, favoriteTag
from .forms import postForm, commentForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from itertools import cycle, chain
import random 
from django.core.paginator import Paginator
from django.core.cache import cache

def homeList(request):
	post = (Post.objects.all().order_by('-date'))[:10]
	if request.user.is_authenticated:
		favtag = get_object_or_404(favoriteTag.objects.filter(userOp = request.user))

	fav_post_list = []				# post with certain tag
	tags_posts = []
	tags_posts_id = []				# for post_id with certain tags

	random_post = []				# post in random order

	after_list_post = []			# list post with tags_posts and random_post

	final_list = []					# all post in random order

	if request.user.is_authenticated:
		proll = 0
		for tag in favtag.tags.all():
			if Post.objects.filter(tags = tag).order_by('-date'):
				for k in Post.objects.filter(tags = tag):
					# check one post with many tags
					if(proll != k.id):
						fav_post_list.append(k)
					proll = k.id
		
		print(fav_post_list)				

		b = list(reversed(fav_post_list))

		for i in range(len(fav_post_list)):
			postCat = (b[i])
			tags_posts.append(postCat)
			tags_posts_id.append(b[i].id)				

	for ranpost in post:
		if ranpost.id not in tags_posts_id:
			random_post.append(ranpost)

	after_list_post = tags_posts + random_post
	

	while len(after_list_post) != 0:
		random_post_p = after_list_post[random.randrange(0, len(after_list_post))]
		final_list.append(random_post_p)
		after_list_post.remove(random_post_p)


	RANDOM_EXPERIENCES=5
	if not request.session.get('random_exp'):
		request.session['random_exp']=random.randrange(0,RANDOM_EXPERIENCES)

	object_list = cache.get("random_exp_%s" % request.session['random_exp'])
	if not object_list:
		object_list = []
		for post in final_list:
			object_list.append(post)
		cache.set("random_exp_%s" % request.session['random_exp'], object_list,60*1)

	p  = Paginator(object_list, 6)
	page_number = request.GET.get('page')
	page_obj = p.get_page(page_number)

	context ={
		'object_list': page_obj,
	}
	return render(request, 'home.html', context)

def storyList(request):
	useract = storyViews.objects.filter(user = request.user).order_by('-date')

	context = {
		'story_post': useract,
	}
	return render(request, 'storypost.html', context)

def DislikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	disliked = False

	if post.likes.filter(id = request.user.id).exists():
		post.likes.remove(request.user)

	if post.dislikes.filter(id = request.user.id).exists():
		post.dislikes.remove(request.user)
		disliked = False
	else:
		post.dislikes.add(request.user)
		disliked = True

	return HttpResponseRedirect(reverse('detailArticle', args=[str(pk)]))


def LikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False

	if post.dislikes.filter(id = request.user.id).exists():
		post.dislikes.remove(request.user)

	if post.likes.filter(id = request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True

	return HttpResponseRedirect(reverse('detailArticle', args=[str(pk)]))

def tags(request, tag_slug):
	tag = get_object_or_404(Tag, slug =tag_slug)
	posts = Post.objects.filter(tags=tag).order_by('-date')

	context = {
		'posts': posts,
		'tag': tag,
	}
	return render(request, 'tagsList.html', context)

def detailPost(request, pk):
	post = get_object_or_404(Post, id=pk)
	photos = Images.objects.filter(post = post)
	comments = Comment.objects.filter(post=post).order_by('-timestamp')

	if request.user.is_authenticated:
		if storyViews.objects.filter(post = post, user = request.user).exists():
			storyViews.objects.filter(post = post, user = request.user).update(date = timezone.now())
		else:
			storyw = storyViews.objects.create(post = post, user = request.user)
			useract = storyViews.objects.filter(user = request.user)


		if favoriteTag.objects.filter(userOp = request.user).exists():
			favtags = get_object_or_404(favoriteTag, userOp = request.user)
		else:
			favtags = favoriteTag.objects.create(userOp = request.user)
		
		
		# delete first 3 tags in favtags, when count.favtags > 10
		if len(favtags.tags.all()) > 10:
			i = 0
			for gk in favtags.tags.all():
				i+=1
				if i < 4:
					favtags.tags.remove(gk)

		tags_objs = []
		tag_obj = []

		if post.tags:
			for p in post.tags.all():
				tags_objs.append(p)
			if post.tags.all().count() <= 3:
				for h in tags_objs:
					tag_obj.append(h)
			else:
				tag_obj.append(tags_objs[0])
				tag_obj.append(tags_objs[1])
				tag_obj.append(tags_objs[2])
	
		if tag_obj != []:	
			for m in range(len(tag_obj)):	
				favtags.tags.add(tag_obj[m])

		print(len(favtags.tags.all()), len(tag_obj))


	if request.method == "POST":
		comment_form = commentForm(request.POST or None)
		if comment_form.is_valid():
			content = request.POST.get('content')
			comment = Comment.objects.create(post=post, user=request.user, content=content)
			comment.save()
			return HttpResponseRedirect(post.get_absolute_url())
	else:
		comment_form =commentForm

	liked = False
	if post.likes.filter(id=request.user.id).exists():
		liked = True

	context = {
		'post': post,
		'comments': comments,
		'comment_form': comment_form,
		'photos': photos,
		'liked': liked,
	}
	return render(request, 'detailArticle.html', context)

def create_post_view(request):
	tags_objs = []

	if request.method == 'POST':
		length = request.POST.get('length')
		description = request.POST.get('description')
		tags = request.POST.get('tags')
		imagefirst = request.FILES.get(f'images{0}')

		tags_p = tags.replace(" ", "")
		tags_list = list(tags_p.split(','))

		for tag in tags_list:
			t, created = Tag.objects.get_or_create(title=tag)
			tags_objs.append(t)

		print(tags_objs)

		post = Post.objects.create(
			textPost = description,
			author = request.user,
			imagePost = imagefirst,
		)

		post.tags.set(tags_objs)
		post.save()

		for file_num in range(0, int(length)):
			Images.objects.create(
				post =post,
				image = request.FILES.get(f'images{file_num}')
			)
	return render(request, 'add_post.html')


def edit_post_view(request):
	post = get_object_or_404(Post, id=pk)

	if request.method == 'POST':
		length = request.POST.get('length')
		description = request.POST.get('description')
		imagefirst = request.FILES.get(f'images{0}')


def comments(request, pk):
	comment = get_object_or_404(Comment, id=pk)
	

	if request.POST.get('action') == 'aja':
		comment.delete()
		return HttpResponseRedirect(reverse('home'))

	if request.POST.get('action') == 'ajax':
		description = request.POST.get('description')
		comment.content = description
		comment.save()


	context = {
		'comment': comment,
	}

	return render(request, 'edit_comment.html', context)

class EditPostView(UpdateView):
	model = Post
	template_name = 'edit_post.html'
	form_class = postForm
	success_url = reverse_lazy('home')

def deletePost(request, pk):
	post = get_object_or_404(Post, id = pk)
	id1 = post.author.profile.id 
	id2 = post.author.id

	print(id1, id2)

	if request.method == 'POST':
		post.delete()
		return HttpResponseRedirect(reverse('profile_page', args=[id1, id2]))

	context = {
		'post': post,
	}

	return render(request, 'delete_post.html', context)

class DeletePostView(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')

class Search(ListView):
	def get_queryset(self):
		return Post.objects.filter(textPost__icontains=self.request.GET.get("q"))

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context["q"] = self.request.GET.get("q")
		return context