from django.contrib import admin
from .models import *

# Define a common admin class for both all models
class CustomPageAdmin(admin.ModelAdmin):
    pass

# Function to register models with the common admin class
def register_models(admin_class, *models):
    for model in models:
        admin.site.register(model, admin_class)


register_models(CustomPageAdmin, RegisteredUser)

# Register Footer models
register_models(CustomPageAdmin, Footer, Footer_Form)

# Register LandingPage models
register_models(CustomPageAdmin, LandingPage_Top_Destination, LandingPage_Flight_Offer, 
                LandingPage_Hotel_Offer, LandingPage_Car_Booking_Offer, LandingPage_Travel_By_Activity_Event, 
                LandingPage_Travel_By_Activity_Card, LandingPage_Advertise_card1, LandingPage_Stories)


# Register AboutPage models
register_models(CustomPageAdmin, AboutPage_About_Us, AboutPage_Know_More, AboutPage_Form)


# Register ContactPage models
register_models(CustomPageAdmin, ContactPage_Contactdetail, ContactForm)


# Register CareerPage models
register_models(CustomPageAdmin, CareerPage_Head, CareerPage_Benefit, CareerPage_Job, CareerPage_Apply_Form)


# Register PrivacyPage and TermsPage models
register_models(CustomPageAdmin, PrivacyPage, TermsPage)