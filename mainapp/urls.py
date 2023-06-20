from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('rename/<int:file_id>/', views.rename_file, name='rename_file'),
    path('register', views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout")
]
