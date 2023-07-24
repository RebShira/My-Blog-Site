from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about_me, name='about'),
    path('', views.StartingPageView.as_view(), name='starting_page'),
    path('posts/', views.AllPostsView.as_view(), name='posts_page'),
    path('posts/<slug:slug>', views.SinglePostView.as_view(), name='post_detail'),
    path('read_later', views.ReadLaterView.as_view(), name='read-later'),
]
