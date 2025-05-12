"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from djangoapp.views import *



urlpatterns = [

    # admin url
    path('admin/', admin.site.urls),

    # cms api
    path('api/LandingPage-content/', LandingPage.as_view(), name='LandingPage-content'),
    path('api/AboutPage-content/', AboutPage.as_view(), name='AboutPage-content'),
    path('api/AboutPage_Form/', AboutFm.as_view(), name='AboutPage_Form'),
    path('api/ContactPage-content/', ContactPage.as_view(), name='ContactPage-content'),
    path('api/ContactForm/', ContactFm.as_view(), name='ContactForm'),
    path('api/CareerPage-content/', CareerPage.as_view(), name='CareerPage-content'),
    path('api/CareerPage-ApplyForm/', CareerPage_Apply_Fm.as_view(), name='CareerPage-ApplyForm'),
    path('api/Privacy_and_terms-content/', Privacy_and_Terms.as_view(), name='Privacy_and_terms-content'),
    path('api/Footer/', Footer_Base.as_view(), name='Footer'),
    path('api/FooterForm/', FooterFm.as_view(), name='FooterForm'),

    # login api
    path('api/send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('api/complete-registration/', CompleteRegistrationView.as_view(), name='complete-registration'),
    path('api/user-details/', UserDetailsView.as_view(), name='user_detail'),
    path('api/logout/', logout_view, name='logout'),

    # travel api
    path('api/search-flights/', FlightSearchView.as_view(), name='search_flights'),
    path('api/search-hotels/', HotelSearchView.as_view(), name='search-hotels'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)