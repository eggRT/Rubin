from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from .forms import SignUpForm, ProfilePageForm
from article.models import Profile, Post
from django.contrib.auth.models import User
from django.views import generic
from django.http import HttpResponse

class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')

class CreateUserProfile(generic.CreateView):
	model = Profile
	form_class = ProfilePageForm
	template_name = 'registration/creationProfile.html'
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class ShowProfilePage(DetailView):
	model = Profile
	template_name = 'registration/user_profile.html'

	def get_context_data(self, *args, **kwargs):
		users = Profile.objects.all()
		context = super(ShowProfilePage, self).get_context_data(*args, **kwargs)

		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
		postik =  Post.objects.filter(author_id= self.kwargs['authorid'])

		context = {
			'page_user': page_user,
			'postik': postik,
		}
		return context

class EditProfilePage(generic.UpdateView):
	model = Profile
	template_name = 'registration/edit_profile.html'
	fields = ['descript', 'profilePic', 'link']
	success_url = reverse_lazy('home')

