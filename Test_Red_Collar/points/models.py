from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.models import User

class LocationManager(models.Manager):
     def search_in_radius(self, lat, lng, r):
        user_point = Point(float(lng), float(lat), srid=4326)

        return self.filter(
            location__distance_lte=(user_point, D(km=r))
        ).annotate(
            dist=Distance('location', user_point)
        ).order_by('dist')

class Location(models.Model):
 name = models.CharField(max_length=255)
 location=models.PointField()
 created_at = models.DateTimeField(auto_now_add=True)
 objects = LocationManager()

 def __str__(self):
        return self.name
 class Meta:
        verbose_name = "Точка"
        verbose_name_plural = "Точки"

class Comment(models.Model):
 location = models.ForeignKey(Location,
                              on_delete=models.CASCADE,
                              related_name='comments',
                              verbose_name="Точка")
 
 text = models.TextField(verbose_name="Комментарий")
 author_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
 created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

 def __str__(self):
        return f"Комментарий к {self.location.name} от {self.author_name}"

 class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"