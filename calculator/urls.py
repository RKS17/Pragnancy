from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),


    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),


    path('', views.home, name='home'),
    path('english-date/', views.english_date,
         name='english_date'),
    path('nepali-date/', views.nepali_date,
         name='nepali_date'),
    path('add-patient/', views.add_pregnancy_checkup,
         name='add_pregnancy_checkup'),

    path('checkup-list/', views.checkup_list, name='checkup_list'),
    path('delete/<int:checkup_id>/', views.delete_checkup, name='delete_checkup'),
    path('checkup/<str:patient_id>/', views.checkup_detail,
         name='checkup_detail'),  # Add this line for details
    path('checkup/<int:checkup_id>/record-visit/',
         views.record_visit, name='record_visit'),
    path('checkup/<int:checkup_id>/', views.checkup_detail, name='checkup_detail'),
    path('visit/edit/<int:visit_id>/', views.edit_visit, name='edit_visit'),
    #     path('pregnancy-calculator/', views.pregnancy_calculator,
    #          name='pregnancy_calculator'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
