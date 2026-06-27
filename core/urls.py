from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_post, name='create_post'),
    path('review-list/', views.review_list, name='review_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('panel/', views.user_panel, name='user_panel'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('status/', views.system_status, name='system_status'),
    path('about/', views.about, name='about'),
]
