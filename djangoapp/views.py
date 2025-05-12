from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.authtoken.models import Token
import requests
from myproject import settings
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.http import JsonResponse


class SendOTPView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user, created = User.objects.get_or_create(email=email, defaults={'username': email, 'is_active': False})
            otp_code = f"{random.randint(100000, 999999)}"
            OTP.objects.update_or_create(user=user, defaults={'otp_code': otp_code, 'created_at': timezone.now()})
            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp_code}',
                    'notification@dgtlinnovations.in',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({'message': f'Failed to send OTP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'message': 'OTP sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            
            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.get(user=user)
                
                if otp.is_expired():
                    return Response({'message': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
                
                if otp.otp_code == otp_code:
                    # OTP is valid
                    try:
                        user_profile = RegisteredUser.objects.get(user=user)
                        if user_profile.is_verified:
                            # User profile is complete, activate the user and generate token
                            user.is_active = True
                            user.save()
                            
                            refresh = RefreshToken.for_user(user)
                            return Response({
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }, status=status.HTTP_200_OK)
                        else:
                            # User profile is incomplete, activate the user and prompt for additional details
                            user.is_active = True
                            user.save()
                            
                            refresh = RefreshToken.for_user(user)
                            return Response({
                                'message': 'OTP verified, complete your registration.',
                                'requires_completion': True,
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }, status=status.HTTP_200_OK)
                    except RegisteredUser.DoesNotExist:
                        # Handle new user scenario
                        user_profile = RegisteredUser.objects.create(user=user, is_verified=False)
                        user.is_active = True
                        user.save()
                        
                        refresh = RefreshToken.for_user(user)
                        return Response({
                            'message': 'OTP verified, complete your registration.',
                            'requires_completion': True,
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }, status=status.HTTP_200_OK)
                
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            except User.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            except OTP.DoesNotExist:
                return Response({'message': 'OTP not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # Authenticated user
        
        # Get or create a profile for the user
        user_profile, created = RegisteredUser.objects.get_or_create(user=user)
        
        if user_profile.is_verified:
            return Response({'message': 'Profile is already complete.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update profile details
        user_profile.first_name = request.data.get('first_name')
        user_profile.last_name = request.data.get('last_name')
        user_profile.phone_number = request.data.get('phone_number')
        user_profile.user_address = request.data.get('user_address')
        
        user_profile.is_verified = True  # Mark profile as complete
        user_profile.save()

        # Ensure the user is marked as active
        user.is_active = True
        user.save()
        
        return Response({'message': 'Registration complete. You are now fully registered.'}, status=status.HTTP_200_OK)




# class UserDetail(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         try:
#             ProfileObj = RegisteredUser.objects.all()
#         except RegisteredUser.DoesNotExist:
#             ProfileObj = None
        
#         Profile_serializer = RegisteredUserSerializer(ProfileObj, many=True, context={'request': request})
        
#         data = {
#             "ProfileObj": Profile_serializer.data,
#             }
        
#         return Response(data)
    
class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = RegisteredUser.objects.filter(user=user).first()

        if profile:
            return Response({
                'ProfileObj': {
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'email': user.email,
                }
            })
        return Response({'message': 'Profile not found'}, status=404)


def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})


class LandingPage(APIView):
    def get(self, request, *args, **kwargs):
        try:
            Top_DestinationObj = LandingPage_Top_Destination.objects.all()
        except LandingPage_Top_Destination.DoesNotExist:
            Top_DestinationObj = None
        try:
            Flight_OfferObj = LandingPage_Flight_Offer.objects.all()
        except LandingPage_Flight_Offer.DoesNotExist:
            Flight_OfferObj = None
        try:
            Hotel_OfferObj = LandingPage_Hotel_Offer.objects.all()
        except LandingPage_Hotel_Offer.DoesNotExist:
            Hotel_OfferObj = None
        try:
            Car_Booking_OfferObj = LandingPage_Car_Booking_Offer.objects.all()
        except LandingPage_Car_Booking_Offer.DoesNotExist:
            Car_Booking_OfferObj = None
        try:
            Travel_By_Activity_EventObj = LandingPage_Travel_By_Activity_Event.objects.all()
        except LandingPage_Travel_By_Activity_Event.DoesNotExist:
            Travel_By_Activity_EventObj = None
        try:
            Travel_By_Activity_CardObj = LandingPage_Travel_By_Activity_Card.objects.all()
        except LandingPage_Travel_By_Activity_Card.DoesNotExist:
            Travel_By_Activity_CardObj = None
        try:
            Advertise_card1Obj = LandingPage_Advertise_card1.objects.all()
        except LandingPage_Advertise_card1.DoesNotExist:
            Advertise_card1Obj = None
        try:
            StoriesObj = LandingPage_Stories.objects.all()
        except LandingPage_Stories.DoesNotExist:
            StoriesObj = None

        Top_Destination_serializer = LandingPage_Top_DestinationSerializer(Top_DestinationObj, many=True, context={'request': request})
        Flight_Offer_serializer = LandingPage_Flight_OfferSerializer(Flight_OfferObj, many=True, context={'request': request})
        Hotel_Offer_serializer = LandingPage_Hotel_OfferSerializer(Hotel_OfferObj, many=True, context={'request': request})
        Car_Booking_Offer_serializer = LandingPage_Car_Booking_OfferSerializer(Car_Booking_OfferObj, many=True, context={'request': request})
        Travel_By_Activity_Event_serializer = LandingPage_Travel_By_Activity_EventSerializer(Travel_By_Activity_EventObj, many=True, context={'request': request})
        Travel_By_Activity_Card_serializer = LandingPage_Travel_By_Activity_CardSerializer(Travel_By_Activity_CardObj, many=True, context={'request': request})
        Advertise_card1_serializer = LandingPage_Advertise_card1Serializer(Advertise_card1Obj, many=True, context={'request': request})
        Stories_serializer = LandingPage_StoriesSerializer(StoriesObj, many=True, context={'request': request})

        data = {
            "Top_DestinationObj": Top_Destination_serializer.data,
            "Flight_OfferObj": Flight_Offer_serializer.data,
            "Hotel_OfferObj": Hotel_Offer_serializer.data,
            "Car_Booking_OfferObj": Car_Booking_Offer_serializer.data,
            "Travel_By_Activity_EventObj": Travel_By_Activity_Event_serializer.data,
            "Travel_By_Activity_CardObj": Travel_By_Activity_Card_serializer.data,
            "Advertise_card1Obj": Advertise_card1_serializer.data,
            "StoriesObj": Stories_serializer.data,
        }

        return Response(data)


class AboutPage(APIView):
    def get(self, request, *args, **kwargs):
        try:
            AboutUsObj = AboutPage_About_Us.objects.all()
        except AboutPage_About_Us.DoesNotExist:
            AboutUsObj = None
        try:
            KnowMoreObj = AboutPage_Know_More.objects.all()
        except AboutPage_Know_More.DoesNotExist:
            KnowMoreObj = None
        
        AboutUs_serializer = AboutPage_About_UsSerializer(AboutUsObj, many=True, context={'request': request})
        KnowMore_serializer = AboutPage_Know_MoreSerializer(KnowMoreObj, many=True, context={'request': request})
        
        data = {
            "AboutUsObj": AboutUs_serializer.data,
            "KnowMoreObj": KnowMore_serializer.data,
            }
        
        return Response(data)
    

class AboutFm(APIView):
    def post(self, request):
        serializer = AboutPage_FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactPage(APIView):
    def get(self, request, *args, **kwargs):
        try:
            ContactdetailObj = ContactPage_Contactdetail.objects.all()
        except ContactPage_Contactdetail.DoesNotExist:
            ContactdetailObj = None
        
        ContactPage_serializer = ContactPage_ContactdetailSerializer(ContactdetailObj, many=True)

        data = {
            "ContactdetailObj": ContactPage_serializer.data,
            }
        
        return Response(data)
    

class ContactFm(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CareerPage(APIView):
    def get(self, request, *args, **kwargs):
        try:
            CareerheadObj = CareerPage_Head.objects.all()
        except CareerPage_Head.DoesNotExist:
            CareerheadObj = None
        try:
            CareerbenefitObj = CareerPage_Benefit.objects.all()
        except CareerPage_Benefit.DoesNotExist:
            CareerbenefitObj = None
        try:
            CareerjobObj = CareerPage_Job.objects.all()
        except CareerPage_Job.DoesNotExist:
            CareerjobObj = None
        
        Careerhead_serializer = CareerPage_HeadSerializer(CareerheadObj, many=True, context={'request': request})
        Careerbenefit_serializer = CareerPage_BenefitSerializer(CareerbenefitObj, many=True, context={'request': request})
        Careerjob_serializer = CareerPage_JobSerializer(CareerjobObj, many=True)

        data = {
            "CareerheadObj": Careerhead_serializer.data,
            "CareerbenefitObj": Careerbenefit_serializer.data,
            "CareerjobObj": Careerjob_serializer.data,
            }
        
        return Response(data)    


class CareerPage_Apply_Fm(APIView):
    def post(self, request):
        serializer = CareerPage_Apply_FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Privacy_and_Terms(APIView):
    def get(self, request, *args, **kwargs):
        try:
            PrivacyObj = PrivacyPage.objects.all()
        except PrivacyPage.DoesNotExist:
            PrivacyObj = None
        try:
            TermsObj = TermsPage.objects.all()
        except TermsPage.DoesNotExist:
            TermsObj = None

        Privacy_serializer = PrivacyPageSerializer(PrivacyObj, many=True)
        Terms_serializer = TermsPageSerializer(TermsObj, many=True)
        
        data = {
            "PrivacyObj": Privacy_serializer.data,
            "TermsObj": Terms_serializer.data,
            }
        
        return Response(data)
    

class Footer_Base(APIView):
    def get(self, request, *args, **kwargs):
        try:
            FooterObj = Footer.objects.all()
        except Footer.DoesNotExist:
            FooterObj = None

        Footer_serializer = FooterSerializer(FooterObj, many=True, context={'request': request})
        
        data = {
            "FooterObj": Footer_serializer.data,
            }
        
        return Response(data)
    

class FooterFm(APIView):
    def post(self, request):
        serializer = Footer_FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# views.py



class FlightSearchView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        departure_date = request.POST.get('departure_date')
        return_date = request.POST.get('return_date', None)
        passenger_type = request.POST.get('passenger_type')

        headers = {
            'Authorization': f'Bearer {settings.DUFFEL_ACCESS_TOKEN}',
            'Duffel-Version': 'v2',
            'Content-Type': 'application/json',
        }

        data = {
            "data": {
                "slices": [
                    {
                        "origin": origin,
                        "destination": destination,
                        "departure_date": departure_date
                    }
                ],
                "passengers": [
                    {
                        "type": passenger_type
                    }
                ]
            }
        }

        if return_date:
            data["data"]["slices"].append({
                "origin": destination,
                "destination": origin,
                "departure_date": return_date
            })

        response = requests.post(
            'https://api.duffel.com/air/offer_requests',
            headers=headers,
            json=data
        )

        return JsonResponse(response.json())
    


class HotelSearchView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        # Extract user-defined parameters from the request
        location_longitude = request.POST.get('longitude')
        location_latitude = request.POST.get('latitude')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        guests = int(request.POST.get('guests', 1))
        rooms = int(request.POST.get('rooms', 1))
        guest_type = request.POST.get('guest_type', 'adult')

        headers = {
            'Authorization': f'Bearer {settings.DUFFEL_ACCESS_TOKEN}',
            'Duffel-Version': 'v2',
            'Content-Type': 'application/json',
        }

        data = {
            "data": {
                "location": {
                    "geographic_coordinates": {
                        "longitude": float(location_longitude),
                        "latitude": float(location_latitude)
                    }
                },
                "check_out_date": check_out_date,
                "check_in_date": check_in_date,
                "guests": [{"type": guest_type}] * guests,
                "rooms": rooms
            }
        }

        response = requests.post(
            'https://api.duffel.com/stays/search',
            headers=headers,
            json=data
        )

        return JsonResponse(response.json(), safe=False)
