from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from blog.models import Category, Post


# Create your views here.
def index(request):
    return render(request, 'index.html')

def show_all_categories(request):  # new code
    categories = Category.objects.all()
    return render(request, 'show_all_categories.html', {'categories': categories})

def show_category(request, id):
    category = Category.objects.get(id=id)
    return render(request, 'show_category.html', {'category': category})

def update_category(request):
    id = request.POST['id']
    name = request.POST['name']
    category = Category.objects.get(id=id)
    category.name = name
    category.save()
    return redirect('show_category', id=id)

def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('show_all_categories')

def create_category(request):
    name = request.POST['name']
    Category.objects.create(name=name)
    return redirect('show_all_categories')

class PostListView(ListView):
    model = Post
    template_name = "show_all_posts.html"

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = "update_post.html"
    success_url = reverse_lazy('show_all_posts')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email)
        user.groups.add(1)
        user.save()
    return render(request, 'register_user.html')

def create_user(username, password, first_name, last_name, email):
    user = User.objects.create_user(username=username,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
    user.groups.add(1)
    user.save()

def like_dislike_post(request, id):
    post = Post.objects.get(id=id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('show_all_posts')