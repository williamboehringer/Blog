from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('author/<slug:slug>', views.author_page, name='author_page'),
    path('search/', views.search_posts, name='search'),
    path('about/', views.about_page, name='about'),
    path('all-posts/', views.all_posts, name='all_posts'),
    path('create-post/', views.create_post, name='create_post'),
]