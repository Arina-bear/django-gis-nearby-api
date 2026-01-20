from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Location, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author_name.username')
    class Meta:
        model = Comment
        fields = ['id', 'location', 'author_name', 'text', 'created_at']
        read_only_fields = ['author_name']

class LocationSerializer(GeoFeatureModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        geo_field = "location"  
        fields = ['id', 'name', 'location', 'comments', 'created_at']