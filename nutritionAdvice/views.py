from django.shortcuts import render, redirect
from openai import OpenAI
from .forms import SignUpForm
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .models import User

# OpenAI API anahtarını çevre değişkenlerinden alın veya doğrudan burada tanımlayın
client = OpenAI(api_key="APIKEY")

def home(request: HttpRequest):
    return render(request, 'home.html')

def meal_recommendation(request: HttpRequest):
    meal_recommendations = []

    if request.method == 'POST':
        calorie_goal = request.POST.get('calorie_goal')
        meal_type = request.POST.get('meal_type')
        try:
            completions = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI nutrition assistant, here to help you with meal suggestions."},
                    {"role": "user", "content": f"Recommend me a {meal_type} that fits within {calorie_goal} calories."}
                ],
                n=3
            )
        except Exception as e:
            # Hata durumunda bir hata mesajı gösterme
            error_message = f"An error occurred while fetching meal recommendations: {e}"
            return JsonResponse({'error_message': error_message}, status=500)
       
        if completions.choices:
            meal_recommendations = [completion.message.content for completion in completions.choices]
            print("Meal recommendations:", meal_recommendations)
            return JsonResponse(meal_recommendations, safe=False)
        else:
            # Yanıtların boş olduğunu belirtmek için bir hata mesajı gösterme
            error_message = "No meal recommendations found."
            return JsonResponse({'error_message': error_message}, status=404)
    
    return render(request, 'meal_recommendation.html', {'meal_recommendations': meal_recommendations})

def signup(request: HttpRequest):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=User.email, password=raw_password)
            login(request, user)
            return redirect('success')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request: HttpRequest):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def success(request):
    return render(request, 'success.html')
