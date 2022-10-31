from django.shortcuts import render
from django.urls import reverse
from app.forms import CommentForm
from app.models import Comments, Post
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]   
    context = {'posts': posts, 'top_posts': top_posts, 'recent_posts': recent_posts}  
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post = post, parent=None)
    form = CommentForm()

    post.view_count = 1 if post.view_count is None else post.view_count + 1
    post.save()
    context = {'post': post,'form': form, 'comments': comments}
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            if request.POST.get('parent'):
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()      
                    return HttpResponseRedirect(reverse('app:post_page', kwargs={'slug': slug}))
            else:     
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('app:post_page', kwargs={'slug': slug}))  
    else:
        return render(request, 'app/post.html', context)