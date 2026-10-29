
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('register/', views.signup, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    # path('logout/', auth_views.Con.as_view(), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('select_account_type/', views.select_account_type, name='select_account_type'),
    # path('signup/', views.signup, name='signup'),
    path('signup_company/', views.signup_company, name='signup_company'),
    path('signup_member/', views.signup_member, name='signup_member'),
    path('redirect-by-role/', views.redirect_by_role, name='redirect_by_role'),
]