from django.shortcuts import render
from django.urls import reverse
from app.forms import CommentForm
from app.models import Comments, Post
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'app/index.html', {'posts': posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post = post)
    form = CommentForm()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('app:post_page', kwargs={'slug': slug}))
        

    post.view_count = 1 if post.view_count is None else post.view_count + 1
    post.save()
    context = {'post': post,'form': form, 'comments': comments}

    return render(request, 'app/post.html', context)