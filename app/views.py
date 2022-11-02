from turtle import title
from django.shortcuts import render
from django.urls import reverse
from app.forms import CommentForm, PostForm, SubscribeForm
from app.models import Comments, Post, Tag, Profile, WebsiteMeta
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    subscribe_form = SubscribeForm()
    subscribe_succsesful = None
    featured_post = Post.objects.filter(is_featured = True)
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_post:
         featured_post = featured_post[0]

    if request.method =='POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_succsesful = 'Subscribed Succsesfully'
            subscribe_form = SubscribeForm()

    context = {
        'posts': posts,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'subscribe_form': subscribe_form,
        'subscribe_succsesful': subscribe_succsesful,
        'featured_post': featured_post,
        'website_info': website_info

    }  
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post = post, parent=None)
    form = CommentForm()
    top_posts = Post.objects.all().order_by('-view_count')[0:2]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]

    post.view_count = 1 if post.view_count is None else post.view_count + 1
    post.save()
    context = {'post': post,'form': form, 'comments': comments, 'top_posts': top_posts, 'recent_posts': recent_posts}
    
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

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    related_posts = Post.objects.filter(tags=tag)
    top_posts = Post.objects.all().order_by('-view_count')[0:2]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    tags = Tag.objects.all()
    context = {'tag': tag, 'related_posts': related_posts, 'top_posts': top_posts, 'recent_posts': recent_posts, 'tags': tags}

    return render(request, 'app/tag.html', context)

def author_page(request, slug):
    author = Profile.objects.get(slug=slug)
    top_posts = Post.objects.all().filter(author=author.id).order_by('-view_count')[0:2]
    top_authors = User.objects.all().annotate(number=Count('post')).order_by('-number')[0:3]
    return render(request, 'app/author.html', {'author': author, 'top_posts': top_posts, 'top_authors': top_authors})  

def search_posts(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)  
    context = {'posts': posts, 'search_query': search_query}
    return render (request, 'app/search.html', context)

def about_page(request):
    subscribe_form = SubscribeForm()
    subscribe_succsesful = None
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if request.method =='POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_succsesful = 'Subscribed Succsesfully'
            subscribe_form = SubscribeForm()

    context = {
        'subscribe_form': subscribe_form, 
        'subscribe_succsesful': subscribe_succsesful,
        'website_info': website_info
        }
    return render(request, 'app/about.html', context)

def all_posts(request):
    posts = Post.objects.all()[0:9]
    return render(request, 'app/allposts.html', {'posts': posts})

@login_required(login_url='accounts:login')
def create_post(request):
    context = {'form': PostForm()}
    return render(request, 'app/teste.html', context)