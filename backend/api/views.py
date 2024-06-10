from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, FileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import File
from django.http import HttpResponse
import os

class FileListCreate(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get all files belonging to user
        return File.objects.filter(uploaded_by=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(uploaded_by=self.request.user)
        else:
            print(serializer.errors)

class FileDelete(generics.DestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(uploaded_by=user)
    
class FileDownload(generics.RetrieveAPIView):
    queryset = File.objects.all()
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.file.path
        
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            response = HttpResponse(file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(instance.file.name)}"'
            return response
        except FileNotFoundError:
            return HttpResponse(status=404)
    

class CreateUserView(generics.CreateAPIView):
    # Query the set of all user objects to prevent duplicate users
    queryset = User.objects.all()
    # Pass class from serializers.py
    serializer_class = UserSerializer
    # Allow anyone to create new user
    permission_classes = [AllowAny]