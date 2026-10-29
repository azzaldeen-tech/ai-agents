from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    # path('search_skills', views.search_skills, name='search_skills'),
    path('search_jobs', views.search_jobs, name='search_jobs'),
    path('advertised_jobs/', views.advertised_jobs, name='advertised_jobs'),
    # path('jop/applications/', views.applied_jobs, name='applied_jobs'),
    path('jop/applications/', views.job_applications, name='job_applications'),
    path('job/join/<int:pk>', views.job_join, name='job_join'),
    path('job/detail/<int:pk>', views.job_detail, name='job_detail'),
    path('job/cancel/<int:pk>/', views.cancel_job_join, name='job_app_cancel'),
    path('job/cancel/<int:pk>/', views.cancel_job_join, name='job_cancel'),
    path('job/resignation/<int:pk>/', views.cancel_job_join, name='job_resignation'),
]
