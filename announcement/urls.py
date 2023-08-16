from django.urls import path
from announcement import views




urlpatterns = [
    path('annlist/', views.AnnList.as_view(),name='annlist'),
    path('anndetail/<int:pk>/', views.AnnDetail.as_view(),name='anndetail'),
    path('anncreate/', views.AnnCreate.as_view(),name='anncreate'),
    path('annupdate/<int:pk>/', views.AnnUpdate.as_view(),name='annupdate'),
    path('annudelete/<int:pk>/', views.AnnDelete.as_view(),name='anndelete'),
    path('annmarklist/', views.AnnMarkReadList.as_view(),name='annmarklist'),
    path('annmarkdetail/<int:pk>/', views.AnnMarReadDetail.as_view(),name='annmarkdetail'),
    path('annmarkcreate/', views.AnnMarkReadCreate.as_view(),name='annmarkcreate'),
    path('annmarkupdate/<int:pk>', views.AnnMarkReadUpdate.as_view(),name='annmarkupdate'),
    path('annviews/', views.AnnUserView.as_view(),name='annviews'),
    path('annhistory/', views.AnnHistory.as_view(),name='annhistory'),
]