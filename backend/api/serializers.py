from django.contrib.auth.models import User
from rest_framework import serializers
from .models import File

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields to be serialized (turned into JSON)
        fields = ["id", "username", "password"]
        # Accept password when creating new user, but do not return password when giving information about user
        extra_kwargs = { "password": { "write_only": True } }

    # validated_data is data that has been validated by the serializer (valid usernamem and valid password based on whatever the criteria is ex. certain length)
    def create(self, validated_data):
        # validated_data is a list of key value pairs (dictionary) so destructure it with **validated_data
        user = User.objects.create_user(**validated_data)
        return user
    
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        # Don't include encrypted_symmetric_key and iv because it is not good to expose them to the API the client will use
        fields = ["id", "title", "content", "created_at", "updated_at", "uploaded_by", "file", "shared_with"]
        # Can read who uploaded_by is, cannot write who uploaded_by is (prevents files from accidently unlinking from users)
        read_only_fields = ['uploaded_by', 'created_at', 'updated_at']