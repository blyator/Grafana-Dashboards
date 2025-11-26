# views.py
from django.shortcuts import render
from .models import Post

def blog_list(request):
    # Logic: Get all blog posts from the database
    posts = Post.objects.all()
    # Send data to the template to be rendered
    return render(request, 'blog_list.html', {'posts': posts})
