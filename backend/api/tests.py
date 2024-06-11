import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from api.encryption.encrypt_file import encrypt_file, decrypt_file
from api.models import File
from django.db.models.signals import post_save
from api.signals import encrypt_file_post_save

class EncryptionDecryptionTestCase(TestCase):
    def setUp(self):
        # Disconnect the signal to prevent it from running during the setup
        post_save.disconnect(encrypt_file_post_save, sender=File)

        # Setup code to create a test user and file
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a dummy file to simulate uploading
        self.uploaded_file = SimpleUploadedFile(
            "testfile.txt",
            b"This is some test data.",
            content_type="text/plain"
        )

        self.file = File.objects.create(
            title="Test File",
            content="This is a test file.",
            uploaded_by=self.user,
            file=self.uploaded_file
        )

        with open(self.file.file.path, 'wb') as f:
            f.write(b'This is some test data.')

        # Reconnect the signal after setting up
        post_save.connect(encrypt_file_post_save, sender=File)

    def test_encryption_decryption(self):
        # Read the file data
        file_path = self.file.file.path
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Encrypt the file data
        encrypted_file_data, encrypted_symmetric_key, iv = encrypt_file(file_data)
        
        # Decrypt the file data
        decrypted_file_data = decrypt_file(encrypted_file_data, encrypted_symmetric_key, iv)

        # Check if the original data matches the decrypted data
        self.assertEqual(file_data, decrypted_file_data, "Decryption failed!")
        print("Encryption and decryption are working correctly.")

    def tearDown(self):
        # Clean up the created file
        if os.path.exists(self.file.file.path):
            os.remove(self.file.file.path)
