from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, \
    SearchPost

urlpatterns = [
    # path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    # path('add/', views.add_blog, name="blog-add"),
    # path('detail/<int:pk>', views.post_detail, name="blog-detail"),
    # path('edit/<int:pk>', views.edit_blog, name="blog-edit"),
    # path('delete/<int:pk>', views.delete_post, name="blog-delete"),
    # path('search/', views.search_post, name="blog-search"),

    # path('add/', views.add_blog, name="blog-add"),
    path('detail/<int:pk>', PostDetailView.as_view(), name="blog-detail"),
    path('', PostListView.as_view(), name="blog-home"),
    path('add/', PostCreateView.as_view(), name="blog-add"),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name="blog-edit"),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name="blog-delete"),
    path('user_post/<str:username>', UserPostListView.as_view(), name="blog-user"),
    path('search/', SearchPost.as_view(), name="blog-search"),
]
