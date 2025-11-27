from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('profil/', views.profile, name='profile'),
    path('berita/', views.news_list, name='news'),
    path('berita/<int:id>/', views.news_detail, name='news_detail'),

    path("layanan/", views.services_view, name="services"),
    path("layanan/ajukan/<int:service_id>/", views.service_request, name="service_request"),
    path("layanan/riwayat/", views.service_requests, name="service_requests"),

    path("galeri/", views.gallery_view, name="gallery"),
    path("galeri/<int:pk>/", views.gallery_detail, name="gallery_detail"),
    path('kontak/', views.contact_view, name='contact'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),


    # Login & Logout
    path('login-user/', views.login_user, name='login_user'),
    path('login-admin/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register'),

]

