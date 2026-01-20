from django.shortcuts import render,redirect
from rest_framework import generics, status,permissions
from .models import Location, Comment
from .serializers import LocationSerializer, CommentSerializer
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import RegisterForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index') 
    else:
        form = RegisterForm()
    
    return render(request, "registration/register.html", {"form": form})

def index(request):
    return render(request, 'points/index.html')

class LocationListCreate(generics.ListCreateAPIView):
  queryset = Location.objects.all()
  serializer_class = LocationSerializer

@method_decorator(csrf_exempt, name='dispatch')
class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author_name=self.request.user)


class NearbyLocationsAPIView(APIView):
    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        r = request.query_params.get('r', 5)

        if not lat or not lng:
            return Response({"error": "Необходимо передать координаты lat и lng"}, status=400)
        locations=Location.objects.search_in_radius(lat, lng, r)
        serializer = LocationSerializer(locations, many=True)

        return Response(serializer.data)
    
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])


def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email', '')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')
    if not username or not password or not email:
        return Response({'error': 'Fill in all fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    if password != password_confirm:
        return Response({'error': 'The passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    
    try: 
        validate_password(password, user=User(username=username))
    except ValidationError as e:
        return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'This user already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.create_user(username=username, password=password,email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=201)##изменить стиль
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
    