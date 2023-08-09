from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/',views.TokenView.as_view(), name='token'),
    path('success2/',views.SuccessView.as_view(), name='success2'),
    path('verify/<auth_token>/', views.VerifyView.as_view(), name='verify'),
    path('error/', views.ErrorView.as_view(), name= 'error'),
    path('mail/', views.SendMailView.as_view(),name='mail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('portfolio/', views.PortFolioView.as_view(), name='portfolio'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('kychoose/', views.KycChoose.as_view(), name='kycchoose'),
    path('kyc/', views.KycView.as_view(), name='kyc'),
    path('kycstatus/', views.KycStatus.as_view(), name='kycstatus'),
    path('successkyc/', views.SuccessKycView.as_view(), name='successkyc'),
    path('kyclists/', views.KycList.as_view(), name='kyclists'),
    path('kyclists/<int:pk>/', views.KycDetail.as_view(), name='kyclist'),
]

