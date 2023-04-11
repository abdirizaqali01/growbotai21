import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

openai.api_key = "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"

# Create your views here.
def index (request, *args, **kwargs):
    return render(request, 'frontend/index.html')


@csrf_exempt
def chat(request):
    if request.method == "POST":
        message = request.POST.get("message", "")
        print(f"Message: {message}")
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Imagine you are a curious naturalist with a soothing voice, a deep love for the natural world, and a knack for observing and describing its beauty and wonder. Your goal is to inspire others to care for and protect the earth's biodiversity through education and a sense of awe and reverence. Conversation:\nUser: {message}\nYou:",
            max_tokens=1000,
            n=1,
            stop=["\nUser:"],
            temperature=0.5,
        )
        result = response.choices[0].text.strip()
        return render(request, 'chat_page.html', {'result': result})
    else:
        return render(request, 'chat_page.html')


def signup(request):
    if request.method == 'POST':
        # Get the form data from the request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        region = request.POST.get('region')

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            error_message = 'Username already taken. Please choose a different one.'
            return render(request, 'user_create.html', {'error_message': error_message})

        # Create a new User object and save it to the database
        user = User.objects.create_user(username, email, password)
        user.region = region
        user.save()

        # Redirect the user to the login page
        return redirect('login')
    else:
        return render(request, 'user_create.html')


def login_view(request):
    if request.method == 'POST':
        # Get the username or email and password from the request
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        # Try to authenticate the user using the username or email and password
        user = authenticate(request, username=username_or_email, password=password)

        # If the user is authenticated, log them in and create a session
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id  # Create a session with the user ID
            return redirect('chat')
        else:
            # If the user is not authenticated, return an error message
            error_message = 'Invalid username/email or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
