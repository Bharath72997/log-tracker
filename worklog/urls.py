from django.contrib import admin
from django.urls import path
from tracker import views
from django.http import HttpResponse  # ✅ for root response
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: HttpResponse("Server is running ✅")),  # 🔧 Safer for Render health checks
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('all-reports/', views.all_reports, name='all_reports'),
]

# ✅ Append media route handling
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
