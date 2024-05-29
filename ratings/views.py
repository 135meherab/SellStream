from django.shortcuts import render
from .models import Ratings
from .serializers import RatingSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

from rest_framework import generics
class RatingGetPost(generics.ListCreateAPIView): # get, post request
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        '''
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()  # Admin can see all users
        return User.objects.filter(username=user.username)
    '''
    
class RatingUpdate(APIView): # update, Retrieve
    def get_object(self, pk):
        try:
            return Ratings.objects.get(pk=pk)
        except Ratings.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RatingSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RatingSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
'''