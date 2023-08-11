from django.urls import path
from announcement import views




urlpatterns = [
    path('annlist/', views.AnnList.as_view(),name='annlist'),
    path('anndetail/<int:pk>/', views.AnnDetail.as_view(),name='anndetail'),
    path('anncreate/', views.AnnCreate.as_view(),name='anncreate'),
    path('annupdate/<int:pk>/', views.AnnUpdate.as_view(),name='annupdate'),
    path('annudelete/<int:pk>/', views.AnnDelete.as_view(),name='anndelete'),
]