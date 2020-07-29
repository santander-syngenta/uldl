from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/',views.logoutUser, name = 'logout'),
    path('upload/', views.upload, name = "Upload"),
    path('download/', views.download, name = "Download"),
	path('export/', views.export_xls, name='Export'),
	path('ZIP/', views.getfiles, name = 'ZIP'),
]
