from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.otp_code}"

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=2)



class RegisteredUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    user_address = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email



class LandingPage_Top_Destination(models.Model):

    image = models.ImageField(upload_to='home_Top_Destination')
    Destination_name = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.Destination_name


class LandingPage_Flight_Offer(models.Model):

    flight_image = models.ImageField(upload_to='home_Flight_Offer')
    flight_travel_type = models.CharField(max_length=500)
    catchline = RichTextField()
    offered_dealprice = models.TextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.flight_travel_type


class LandingPage_Hotel_Offer(models.Model): 

    hotel_image = models.ImageField(upload_to='home_Hotel_Offer')
    hotel_rating = models.CharField(max_length=200)
    hotel_name = models.CharField(max_length=200)
    hotel_location = models.CharField(max_length=200)
    hotel_price = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.hotel_name


class LandingPage_Car_Booking_Offer(models.Model):

    car_image = models.ImageField(upload_to='home_Car_Booking_Offer')
    car_rating = models.CharField(max_length=500)
    car_model_name = models.CharField(max_length=200)
    car_rent_location = models.CharField(max_length=200)
    car_odometer_reading = models.CharField(max_length=500)
    car_model_type = models.CharField(max_length=500)
    car_fuel_type = models.CharField(max_length=500)
    car_seat_count = models.CharField(max_length=500)
    car_booking_price = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.car_model_name


class LandingPage_Travel_By_Activity_Event(models.Model):

    activity_image = models.ImageField(upload_to='home_Travel_By_Activity_Event')
    activity_name = models.CharField(max_length=200)
    tour_count = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.activity_name
    

class LandingPage_Travel_By_Activity_Card(models.Model):

    activity_card_image = models.ImageField(upload_to='home_Travel_By_Activity_Card')
    activity_card_tour_count = models.CharField(max_length=200)
    activity_card_name = models.CharField(max_length=200)
    activity_list_col1 = RichTextField()
    activity_list_col2 = RichTextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.activity_card_name
    

class LandingPage_Advertise_card1(models.Model):

    advertise_card_catchline = RichTextField()
    advertise_card_image = models.ImageField(upload_to='home_Advertise_card1')

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "Advertise_Card"
    

class LandingPage_Stories(models.Model):

    story1_image = models.ImageField(upload_to='home_Stories')
    story1_name = RichTextField()
    story2_image = models.ImageField(upload_to='home_Stories')
    story2_name = RichTextField()
    story3_image = models.ImageField(upload_to='home_Stories')
    story3_name = RichTextField()
    story4_image = models.ImageField(upload_to='home_Stories')
    story4_name = RichTextField()
    story5_image = models.ImageField(upload_to='home_Stories')
    story5_name = RichTextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "Stories"


class AboutPage_About_Us(models.Model):

    about_us_title1 = RichTextField()
    about_us_content1 = RichTextField()
    about_us_image1 = models.ImageField(upload_to='About_Us')
    about_us_title2 = RichTextField()
    about_us_content2 = RichTextField()
    about_us_image2 = models.ImageField(upload_to='About_Us')

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "About_Us"
    

class AboutPage_Know_More(models.Model):

    card_image = models.ImageField(upload_to="About_Know_More")
    card_text = RichTextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.id} Know_More"
    

class AboutPage_Form(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add = True)


class ContactPage_Contactdetail(models.Model):

    contactdetail1_title = models.CharField(max_length=200, null=True)
    contactdetail2_subtitle = models.CharField(max_length=200)
    contactdetail3_phone = models.CharField(max_length=200)
    contactdetail4_email = models.CharField(max_length=200)
    contactdetail5_address = models.CharField(max_length=200)
    contactdetail6_weblink = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.contactdetail1_title
    

class ContactForm(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add = True)


class CareerPage_Head(models.Model):

    career_headimage = models.ImageField(upload_to="Career_Head")
    career_headtitle = RichTextField()
    career_headcontent = models.TextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "Career Head"
    

class CareerPage_Benefit(models.Model):

    benefits_image = models.ImageField(upload_to="Career_Benefits")
    benefits_content = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.benefits_content
    

class CareerPage_Job(models.Model):

    Designation = models.CharField(max_length=50)
    Job_Location = models.CharField(max_length=100)
    Experience_Required = models.CharField(max_length=50)
    Job_Position = models.CharField(max_length=50)
    Salary = models.CharField(max_length=50)
    Qualification_Required = models.TextField()
    Job_Type = models.CharField(max_length=100)
    Job_Description = RichTextField()
    Post_status = models.CharField(max_length=10,default="show")

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.Designation
    

class CareerPage_Apply_Form(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    education = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    LinkedIn = models.CharField(max_length=100)
    message = models.CharField(max_length=150)
    pdf = models.FileField(upload_to="resume-pdf")

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.name}"


class PrivacyPage(models.Model):

    privacy_content = RichTextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "Privacy Policy"
    
class TermsPage(models.Model):

    terms_content = RichTextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "Terms"
    

class Footer(models.Model):

    footer_logo = models.ImageField(upload_to='footer-logo')
    footer_catchline = models.CharField(max_length=50)
    footer_facebook_link = models.CharField(max_length=100, default = "none", null= True)
    footer_twitter_link = models.CharField(max_length=100, default = "none", null= True)
    footer_instagram_link = models.CharField(max_length=100, default = "none", null= True)
    footer_address = models.CharField(max_length=50)
    footer_phone_number = models.CharField(max_length=15)
    footer_email = models.CharField(max_length=50)
    footer_copyright_line = RichTextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "Footer"
    

class Footer_Form(models.Model):

    subscriber_email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add = True)