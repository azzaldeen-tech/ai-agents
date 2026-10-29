from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _
app_name = 'core'

# تأكد أن الاسم urlpatterns بالجمع (s في النهاية) وكل الحروف small
urlpatterns = [
    path('', views.home, name='home'),
    path('labor_market_trends/', views.labor_market_trends, name='labor_market_trends'),
    path('predictive_analytics/', views.predictive_analytics, name='predictive_analytics'),
    path('student_guidance_analytics/', views.student_guidance_analytics, name='student_guidance_analytics'),
    path('jobs_explore/', views.explore_jobs_view, name='jobs_explore'),
    path('companies/explore/', views.companies_explore_view, name='companies_explore'),
    path('waiting-approval/', views.waiting_approval_view, name='waiting_approval'),

    path('company/profile/<int:pk>', views.company_profile, name='company_profile'),


    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('search/', views.search_users, name='search_users'),
    # path('live_jobs_view/', views.live_jobs_view, name='live_jobs_view'),
    path('search_skills', views.search_skills, name='search_skills'),
    path('search_jobs', views.search_jobs, name='search_jobs'),
]