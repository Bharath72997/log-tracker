from django.contrib import admin
from django.urls import path
from tracker import views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('register')),  # ✅ Home goes to registration
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),  # ✅ Register page
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('all-reports/', views.all_reports, name='all_reports'),
]

# ✅ Append media route handling outside the list
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
