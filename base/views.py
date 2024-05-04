from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, UserCreationForm

# Create your views here.


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not found!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Passwords do not match!')

    context = {'page': page}

    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!')
            form = UserCreationForm(request.POST, request.FILES)

    context = {'form': form,}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    print(q)
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()[:5]
    room_count = rooms.count()

    room_messages = Message.objects.filter(Q(room__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.message.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)
        
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants,}
    return render(request, 'base/room.html', context)


def profile(request, pk):
    profile = User.objects.get(id=pk)
    rooms = profile.room_set.all()
    room_messages = profile.message_set.all()
    topics = Topic.objects.all()

    context = {'profile': profile, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics,}

    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def editProfile(request):
    user = request.user
    form = UserForm(instance=user)

    context = {'user': user, 'form': form,}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    return render(request, 'base/edit-user.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    topics = Topic.objects.all()

    if request.method == 'POST':
        topics_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topics_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'update_or_create': 'CREATE'}
    return render(request, 'base/form_room.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)

    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topics_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topics_name)
        form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room, 'update_or_create': 'UPDATE'}
    return render(request, 'base/form_room.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(pk=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(pk=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})


def topics(request):
    topics = Topic.objects.all()
    context = {'topics': topics}

    return render(request, 'base/topics.html', context)


def activities(request):
    messages = Message.objects.all()
    context = {'room_messages': messages}

    return render(request, 'base/activity.html', context)
