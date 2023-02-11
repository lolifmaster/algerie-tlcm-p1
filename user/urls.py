from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.homePage, name="home"),
    path('api/dots/', views.getDotInformations, name="dots_info"),
    path('api/dot/<str:pk>/', views.getDotInformation, name="dot_info"),
    path('api/cmps/', views.getCmpInformations, name="cmps_info"),
    path('api/cmp/<str:pk>/', views.getCmpInformation, name="cmp_info"),
    path('api/region/', views.getCmpsName, name="cmps_name"),
    path('api/region/<str:pk>/', views.getCmpName, name="cmp_name"),
]
