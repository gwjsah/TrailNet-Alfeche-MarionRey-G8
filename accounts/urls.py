from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect_view, name='dashboard_redirect'),
    path('dashboard/rider/', views.rider_dashboard_view, name='rider_dashboard'),
    path('dashboard/admin/', views.admin_dashboard_view, name='admin_dashboard'),
]
