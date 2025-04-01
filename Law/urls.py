"""
URL configuration for Law project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout'),
    path('update_user/<int:id>/',views.update_user,name='update_user'),
    path('profile/<int:id>/',views.update_user,name='profile'),
    path('lawyer/',views.lawyer_list,name='lawyer_list'),
    path('register_case/',views.register_case,name='register_case'),
    path('emergency_numbers/', views.emergency_numbers, name='emergency_numbers'),
    path('book_lawyer/',views.book_lawyer1,name='book_lawyer1'),
    path('book_lawyer/<int:id>/', views.book_lawyer2, name='book_lawyer2'),
    path('book_lawyer/third/<int:Book_Id>/', views.book_lawyer3, name='book_lawyer3'),
    path('basic_laws/',views.basiclaws,name='basic_laws'),
    path('payment/<int:Book_Id>/',views.payment,name='payment'),
    path('booking_history/',views.booking_history,name='booking_history'),
    path('case_history/',views.case_history,name='case_history'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
