from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('desaapp.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # ✅ Tambahkan route login & logout di sini
    path('login/', auth_views.LoginView.as_view(template_name='desaapp/registrations/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
