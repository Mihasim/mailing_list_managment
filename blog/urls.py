from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>/', cache_page(180)(BlogDetailView.as_view()), name='blog_detail'),
    path('blog/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),
]