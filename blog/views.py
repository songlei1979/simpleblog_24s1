from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

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


