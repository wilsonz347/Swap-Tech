#sustainability/urls.py - manages all urls for project

from django.contrib import admin  # Django admin module
from django.urls import path       # URL routing
from . import views
from django.conf import settings   # Application settings
from django.conf.urls.static import static  # Static files serving
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # Static files serving


urlpatterns = [
    path("landing/", views.landing, name="landing"), #temp landing page
    path('login/', views.login_page, name='login'),    # Login page
    path('register/', views.register_page, name='register'),  # Registration page
    path('logout/', views.logout_page, name='logout'), # Logout page
    path('recyclerhome/', views.recycler_home, name='recyclerhome'), #Recycler home
    path('home/', views.refurbisher_home, name='home') #new, refurbisher home
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Directory added in settings

# Serve static files using staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
