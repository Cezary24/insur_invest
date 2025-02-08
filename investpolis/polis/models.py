import hashlib
from django.db import models

class PolicyFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='policy_files/')
    file_hash = models.CharField(max_length=64, unique=True)

    def save(self,*args, **kwargs):

        if self.file and not self.file_hash:
            sha = hashlib.sha256()
            for chunk in self.file.chunks():
                sha.update(chunk)
            self.file_hash =    sha.hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.file_hash})"
    


