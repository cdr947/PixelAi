from django.db import models

# Create your models here.

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    results = models.JSONField(null=True, blank=True)  # Store inference results as JSON
    predicted = models.ImageField(upload_to='predicted/', null=True, blank=True)  # Store predicted image with bounding boxes

    def __str__(self):
        return f"ImageUpload {self.id} - {self.image.name}"