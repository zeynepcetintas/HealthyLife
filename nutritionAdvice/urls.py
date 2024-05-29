from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('meal_recommendation/', views.meal_recommendation, name='meal'),
    path('signup/', views.signup, name='signup'),
    path('success/', views.success, name='success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, {'next_page': 'home'}, name='logout'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)