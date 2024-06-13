from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, FileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import File
from django.http import HttpResponse, Http404
import os
from .encryption.encrypt_file import decrypt_file

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
            # Get file
            with open(file_path, 'rb') as f:
                encrypted_file_data = f.read()

            # Decrypt file
            decrypted_file_data = decrypt_file(
                encrypted_file_data,
                instance.encrypted_symmetric_key,
                instance.iv
            )

            # Send decrypted file to client
            response = HttpResponse(decrypted_file_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(instance.file.name)}"'
            return response
        except Exception as e:
            raise Http404(f"File not found or decryption failed: {e}")
    

class CreateUserView(generics.CreateAPIView):
    # Query the set of all user objects to prevent duplicate users
    queryset = User.objects.all()
    # Pass class from serializers.py
    serializer_class = UserSerializer
    # Allow anyone to create new user
    permission_classes = [AllowAny]
