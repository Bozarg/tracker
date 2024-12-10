
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]

    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    deadline = models.DateField()

    def __str__(self):
        return self.title


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
