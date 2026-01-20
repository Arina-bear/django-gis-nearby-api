from django.urls import path
from .views import (
    LocationListCreate, 
    CommentCreate, 
    index, 
    register_user, 
    login_user,
    NearbyLocationsAPIView,
)

urlpatterns = [
    path('', index, name='index'),
    path('register/', register_user, name='register_api'),
    path('login/', login_user, name='login_api'),
    path('locations/', LocationListCreate.as_view(), name='location-list'),
    path('nearby/', NearbyLocationsAPIView.as_view(), name='nearby_locations_api'),
    path('comments/', CommentCreate.as_view(), name='comment-create'),
]
