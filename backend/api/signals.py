from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import File
from .encryption.encrypt_file import encrypt_file

# Use a flag to prevent recursive calls
processing_encryption = False

@receiver(post_save, sender=File)
def encrypt_file_post_save(sender, instance, **kwargs):
    global processing_encryption
    if not processing_encryption:
        processing_encryption = True
        try:
            # Encrypt the file content before it has been saved
            file_path = instance.file.path
            with open(file_path, "rb") as f:
                file_data = f.read()

            encrypted_file_data, encrypted_symmetric_key, iv = encrypt_file(file_data)

            # Save the encrypted file data
            with open(file_path, "wb") as f:
                f.write(encrypted_file_data)

            # Update the instance with the encrypted symmetric key and IV
            instance.encrypted_symmetric_key = encrypted_symmetric_key
            instance.iv = iv
            instance.save()
        finally:
            processing_encryption = False
