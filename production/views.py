from django.http import	HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .forms import ContactForm
from blog.models import BlogPost

def home(request):
	
	if request.user.is_authenticated:
		my_title = 'título blablbalba'
		qs = BlogPost.objects.filter(user=request.user.id)[:5]
		context = {'title': 'Welcome' , 'blog_list': qs}
		return render(request, 'home.html', context)

	else:
		return render(request, 'about.html', {'title': 'about us'})

def about(request):
	return render(request, 'about.html', {'title': 'about us'})

def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		form = ContactForm()

	context = {
		'title' : 'Contact Us',
		'form' : form 
	}
	return render(request, 'form.html', context)

