from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import Http404
import subprocess
import os

# Create your views here.

from .forms import BlogPostModelForm
from .models import BlogPost
from nlp import *


@login_required
def blog_post_list_view(request):
    qs = BlogPost.objects.all().published()
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        # qs = BlogPost.objects.filter(user=request.user.id)
        # qs = BlogPost.objects.published()
        qs = (qs | my_qs).distinct()

    template_name = 'blog/list.html'
    context = {'object_list' : qs}
    return render(request, template_name, context)


#@staff_member_required
@login_required
def blog_post_create_view(request):

    if not request.user.is_authenticated:
        return render(request,'not-a-user.html', {})
 
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        name = form.cleaned_data["slug"]

        with open(f"{name}.txt", "w") as text_file:
            text_file.write(f"{form.cleaned_data['content']}\n\n")
            text_file.close()
            subprocess.call (f"/usr/bin/Rscript nlp.R {name}.txt", shell=True)

        os.remove(f"{name}.txt")

        # summarized = bert_sumarizar(f"{form.cleaned_data['content']}\n\n")
        # adicionar summarized ao sql

        obj = form.save(commit=False)
        obj.user = request.user
        obj.wordcloud = f'image/plots/wordclouds/{name}_word_cloud.jpeg'
        obj.barplot = f'image/plots/barplots/{name}_word_freq.jpeg'
        obj.sents_1 = f'image/plots/sents_1/{name}_sents_1.jpeg'
        #obj.sents_2 = f'image/plots/sents_2/{name}_sents_2.jpeg'
        obj.reinert = f'image/plots/reinerts/{name}_reinert.png'
        obj.save()
        form = BlogPostModelForm()


    template_name = 'form.html'
    context = {'form' : form}
    return render(request, template_name, context)


@login_required
def blog_post_detail_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'

    context = {'object' : obj}
    return render(request, template_name, context)


@login_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()

    template_name = 'form.html'
    context = {'form' : form, 'title' : f"Update {obj.title}" }
    return render(request, template_name, context)


@login_required
def blog_post_delete_view(request, slug):
    template_name = 'blog/delete.html'
    obj = get_object_or_404(BlogPost, slug=slug)

    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/")
 
    return render(request, template_name)


@login_required
def blog_post_reinert_view(request, slug):
    return HttpResponseRedirect(reverse('127.0.0.1:7459'))
