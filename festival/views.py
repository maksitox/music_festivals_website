from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import Festival, Artist, Song, Festival_Artist, Festival_Sponsor, Ticket
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from jinja2 import Environment
from jinja2.filters import FILTERS


def index(request, *message):

    messages.warning(request, message)
    num_artists = len(Artist.objects.all())
    festivals = Festival.objects.all()
    amount_fst = len(festivals)
    amount_clients = len(User.objects.all())
    descs = [f.desc for f in festivals]
    descss = [d.split(".")[0] for d in descs]
    manager = False

    def price(fest_id):
        tickets = Ticket.objects.filter(festival=fest_id)
        t = [ticket.price for ticket in tickets]
        return t

    env = Environment()

    env.filters['price'] = price

    context = {"festivals": festivals,
               "amount_fst": amount_fst,
               "amount_clients": amount_clients,
               "num_artists": num_artists,
               "descss": descss,
               "manager": manager,
               }

    return render(request, 'public/index.html', context)


def festival(request, festival_id):

    is_manager = False
    names = (grou.name for grou in request.user.groups.all())
    if "manager" in names:
        is_manager = True
    festival = get_object_or_404(Festival, pk=festival_id)
    festival_artists = Festival_Artist.objects.filter(festival=festival)
    artists = [fa.artist for fa in festival_artists]
    num_tickets = festival.ticket_set.aggregate(
        total_tickets=Sum('amount'))['total_tickets']
    num_sold_tickets = festival.ticket_set.aggregate(
        total_sold_tickets=Sum('amount_sold'))['total_sold_tickets']
    if num_tickets != None and num_sold_tickets != None:
        num_free_tickets = num_tickets - num_sold_tickets
    else:
        num_free_tickets = 0
    tickets = Ticket.objects.filter(festival=festival_id)
    names = (grou.name for grou in request.user.groups.all())
    context = {'festival': festival,
               'num_tickets': num_tickets,
               "num_sold_tickets": num_sold_tickets,
               "num_free_tickets": num_free_tickets,
               "artists": artists,
               "tickets": tickets,
               "is_manager": is_manager,
               }
    return render(request, 'public/festival.html', context)


def artist(request, artist_id):
    songs = Song.objects.filter(artist=artist_id)
    artist = get_object_or_404(Artist, pk=artist_id)
    ticket_types = ["Student", "Adult", "VIP"]

    context = {'festival': festival,
               "artist": artist,
               "ticket_types": ticket_types,
               "songs": songs,
               }
    return render(request, 'public/artist.html', context)


def test(request):
    return render(request, 'public/template/public_template.html')


def buy(request, ticket_id):
    if User.is_authenticated:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        ticket.amount_sold = ticket.amount_sold + 1
        ticket.save()
        message = "You succefully buy a ticket."
        return index(request, message)
    else:
        message = "You are not loggined in."
        return index(request, message)
