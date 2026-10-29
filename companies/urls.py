from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),

    path('job/add/', views.manage_job, name='job_add'),
    path('job/edit/<int:pk>/', views.manage_job, name='job_edit'),
    path('job/delete/<int:pk>/', views.delete_job, name='job_delete'),
    path('job/detail/<int:pk>', views.job_detail, name='job_detail'),
    path('advertised_jobs', views.advertised_jobs, name='advertised_jobs'),
    path('job/applications', views.job_applications, name='job_applications'),
    path('job/application/detail/<int:pk>/', views.job_applicant_detail, name='job_applicant_detail'),
    path('job/application/accept/<int:pk>/', views.job_app_accept, name='job_app_accept'),
    path('job/application/reject/<int:pk>/', views.job_app_reject, name='job_app_reject'),
]
