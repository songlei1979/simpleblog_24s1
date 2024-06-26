import pandas
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from blog.models import Category, Post, Comment, Profile


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


class PostDetailView(DetailView):
    model = Post
    template_name = "show_post.html"


def create_comment(request, id):
    post = Post.objects.get(id=id)
    content = request.POST['content']
    author = request.user  ## means the login user
    # post.comment_set.create(content=content, author=author)
    comment = Comment.objects.create(post=post, content=content, author=author)
    return redirect('post_detail', pk=id)


def create_profile(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES['image']
        address = request.POST['address']
        phone = request.POST['phone']
        youtube = request.POST['youtube']
        Profile.objects.create(user=user,
                               image=image,
                               address=address,
                               phone=phone,
                               youtube=youtube)
    return render(request, 'create_profile.html')


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['image', 'address', 'phone', 'youtube']
    template_name = "update_profile.html"
    success_url = reverse_lazy('home')


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "show_profile.html"

def sum_numbers(request):
    num1 = int(request.POST['num1'])
    num2 = int(request.POST['num2'])
    result = num1 + num2
    return render(request, 'sum_numbers.html', {'result': result})


def send_email_out(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        from_email = request.POST['from_email']
        to_email = request.POST['to_email']
        send_mail(subject, body, from_email, [to_email])
    return render(request, 'send_email_out.html')


def read_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        worksheet = pandas.read_excel(excel_file)
        data = pandas.DataFrame(worksheet, columns=[
            "Username", "DOB", "Firstname", "Lastname",
            "email", "Address", "Phone", "Youtube"
        ])
        usernames = data["Username"].tolist()
        dobs = data["DOB"].tolist()
        firstnames = data["Firstname"].tolist()
        lastnames = data["Lastname"].tolist()
        emails = data["email"].tolist()
        addresses = data["Address"].tolist()
        phones = data["Phone"].tolist()
        youtubes = data["Youtube"].tolist()
        i = 0
        while i < len(usernames):
            dob = dobs[i]
            dob = dob.strftime('%Y-%m-%d') #1999-12-31
            dob = str(dob)
            password = dob.split('-')[0]+dob.split('-')[1]+dob.split('-')[2]
            username = usernames[i]
            first_name = firstnames[i]
            last_name = lastnames[i]
            email = emails[i]
            address = addresses[i]
            phone = phones[i]
            youtube = youtubes[i]
            User.objects.create_user(username=username,
                                      password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
            Profile.objects.create(user=User.objects.get(username=username),
                                   address=address,
                                   phone=phone,
                                   youtube=youtube)
            i += 1

        return render(request, 'read_excel.html', {
            'msg': 'Done'
        })
    else:
        return render(request, 'read_excel.html', {
            'msg': ''
        })
