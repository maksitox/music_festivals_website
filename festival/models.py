from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import F



# Create your models here.

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255, unique=True)
    
class Artist(models.Model):
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    img = models.ImageField(upload_to='pics')
    contact = models.CharField(max_length=255, unique=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

class Song(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

class Festival(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=20)
    place = models.CharField(max_length=100)

class Festival_Artist(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    artist =  models.ForeignKey(Artist, on_delete=models.CASCADE)

class Festival_Sponsor(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    sponsor =  models.ForeignKey(Sponsor, on_delete=models.CASCADE)

class Ticket(models.Model):
    TICKET_TYPES = (
        ('Student', 'Student'),
        ('Adult', 'Adult'),
        ('VIP', 'VIP'),
    )
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField()
    amount_sold = models.PositiveIntegerField(default=0)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.amount_sold > self.amount:
            raise ValidationError('Amount sold cannot be greater than amount.')
        

