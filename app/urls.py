from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    
]