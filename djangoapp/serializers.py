from rest_framework import serializers
from .models import *

class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = '__all__'


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)


class LandingPage_Top_DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage_Top_Destination
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     request = self.context.get('request', None)
    #     if request is not None:
    #         representation['image'] = request.build_absolute_uri(instance.image.url)
    #     return representation


class LandingPage_Flight_OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage_Flight_Offer
        fields = '__all__'


class LandingPage_Hotel_OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage_Hotel_Offer
        fields = '__all__'


class LandingPage_Car_Booking_OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage_Car_Booking_Offer
        fields = '__all__'


class LandingPage_Travel_By_Activity_EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage_Travel_By_Activity_Event
        fields = '__all__'


class LandingPage_Travel_By_Activity_CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage_Travel_By_Activity_Card
        fields = '__all__'


class LandingPage_Advertise_card1Serializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage_Advertise_card1
        fields = '__all__'


class LandingPage_StoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage_Stories
        fields = '__all__'


class AboutPage_About_UsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage_About_Us
        fields = '__all__'


class AboutPage_Know_MoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage_Know_More
        fields = '__all__'


class AboutPage_FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage_Form
        fields = '__all__'


class ContactPage_ContactdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage_Contactdetail
        fields = '__all__'


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'


class CareerPage_HeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPage_Head
        fields = '__all__'


class CareerPage_BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPage_Benefit
        fields = '__all__'


class CareerPage_JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPage_Job
        fields = '__all__'


class CareerPage_Apply_FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPage_Apply_Form
        fields = '__all__'


class PrivacyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPage
        fields = '__all__'


class TermsPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsPage
        fields = '__all__'


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = '__all__'


class Footer_FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer_Form
        fields = '__all__'