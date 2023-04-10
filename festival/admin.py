from django.contrib import admin
from .models import Festival, Artist, Sponsor, Song, Ticket, Festival_Artist, Festival_Sponsor
# Register your models here.

admin.site.register(Festival)
admin.site.register(Artist)
admin.site.register(Sponsor)
admin.site.register(Song)
admin.site.register(Ticket)
admin.site.register(Festival_Artist)
admin.site.register(Festival_Sponsor)
