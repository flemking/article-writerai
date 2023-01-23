from django.urls import path
from . import views
from .views import SignUpView


urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload, name="upload"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('blog/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]