from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from .models import UserFav
from .serializer import UserFavSerializer

class UserFavViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = UserFav.objects.all()
    serializer_class =UserFavSerializer
