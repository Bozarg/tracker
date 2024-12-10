from django.urls import path

from . import views
from .views import  register , CustomLoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_details, name='task_details'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view , name='logout'),
    path('contact_us/', views.contact_us, name='contact us'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('profile_view/', views.profile_view, name='profile'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),

]
