from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.db.models import Sum

from django.shortcuts import get_object_or_404, render, redirect
from .models import Problem


def index(request):
    problems = Problem.objects.all().order_by('-created_at')
    active_problems = problems.exclude(verification_status='Cancelled')
    total_people_affected = active_problems.aggregate(total=Sum('people_affected'))['total'] or 0

    category_map = {
        'Waste': 'Waste Management',
        'Street Light': 'Street Light Issue',
        'Water': 'Water Problem',
    }

    hero_cards = []
    for key, label in category_map.items():
        category_count = active_problems.filter(category=key).aggregate(total=Sum('people_affected'))['total'] or 0
        hero_cards.append({
            'title': label,
            'count': category_count,
            'icon': '🚮' if key == 'Waste' else '💡' if key == 'Street Light' else '💧',
            'key': key,
        })

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        location = request.POST.get('location')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        people_affected = int(request.POST.get('people_affected') or 0)
        latitude = request.POST.get('latitude') or None
        longitude = request.POST.get('longitude') or None

        Problem.objects.create(
            title=title,
            category=category,
            location=location,
            description=description,
            image=image,
            people_affected=max(people_affected, 0),
            verification_status='Pending review',
            latitude=latitude,
            longitude=longitude,
        )
        return redirect('index')

    return render(request, 'index.html', {
        'problems': problems,
        'hero_cards': hero_cards,
        'total_people_affected': total_people_affected,
    })


def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return render(request, 'problem_detail.html', {'problem': problem})

# --- NORMAL USER LOGIN & SIGNUP CODE ---

def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # Account bante hi login ho jayega
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    auth_logout(request)
    return redirect('index')

