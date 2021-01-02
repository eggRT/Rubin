from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from article.models import Profile
from PIL import Image

class SignUpForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs ={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'

class ProfilePageForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('profilePic', 'descript', 'link')

		widgets = {
			'descript': forms.TextInput(attrs={'class': 'form-control'}),
			'link': forms.TextInput(attrs={'class': 'form-control'}),
		}
	
