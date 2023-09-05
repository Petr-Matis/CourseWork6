from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from blog import views
from users.apps import UsersConfig
from users.views import *
from blog.views import *

app_name = 'blog'

urlpatterns = ([
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('createblog/', BlogCreateView.as_view(), name='createblog'),
    path('viewblog/<int:pk>/', BlogDetailView.as_view(extra_context={'title': 'Dinnstore'}), name='viewblog'),
    path('editblog/<int:pk>/', BlogUpdateView.as_view(), name='editblog'),
    path('deleteblog/<int:pk>/', BlogDeleteView.as_view(), name='deleteblog'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

