from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='problem_images/', blank=True, null=True)
    people_affected = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=1)
    status = models.CharField(max_length=50, default='Unresolved')
    VERIFICATION_STATUS_CHOICES = [
        ('Pending review', 'Pending review'),
        ('Verified', 'Verified'),
        ('Cancelled', 'Cancelled'),
    ]
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='Pending review',
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title