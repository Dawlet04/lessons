from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Course, Category, Teacher, Users, Enrollment
from django.contrib.auth.decorators import login_required
def home(request):
    popular_courses = Course.objects.filter(is_published=True).order_by('-created_at')[:6]
    categories = Category.objects.all()
    top_teachers = Teacher.objects.all()[:4]
    
    context = {
        'popular_courses': popular_courses,
        'categories': categories,
        'top_teachers': top_teachers,
    }
    
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_num = request.POST.get('phone_num')
        
     
        if password != password2:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('register')
        
        if Users.objects.filter(username=username).exists():
            messages.error(request, 'Имя пользователя уже занято!')
            return redirect('register')
        
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email уже зарегистрирован!')
            return redirect('register')
        

        user = Users.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_num=phone_num,
            role='student'
        )
        
        messages.success(request, 'Регистрация прошла успешно! Теперь войдите в систему.')
        return redirect('login')
    
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')
            return redirect('login')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')


def courses(request):
  
    all_courses = Course.objects.filter(is_published=True).order_by('-created_at')
    categories = Category.objects.all()
    

    category_id = request.GET.get('category')
    if category_id:
        all_courses = all_courses.filter(category_id=category_id)
    
    context = {
        'courses': all_courses,
        'categories': categories,
    }
    
    return render(request, 'courses.html', context)



def teachers(request):
  
    all_teachers = Teacher.objects.all().order_by('-rating')
    
    context = {
        'teachers': all_teachers,
    }
    
    return render(request, 'teachers.html', context)


@login_required
def profile(request):
 
    user = request.user

    enrollments = Enrollment.objects.filter(user=user).select_related('course')
    
    teacher_courses = None
    if hasattr(user, 'teacher_profile'):
        teacher_courses = Course.objects.filter(teacher=user.teacher_profile)
    
    context = {
        'enrollments': enrollments,
        'teacher_courses': teacher_courses,
    }
    
    return render(request, 'profile.html', context)

def about(request):
    return render(request, 'about.html')

def about(request):
  
    total_courses = Course.objects.filter(is_published=True).count()
    total_teachers = Teacher.objects.count()
    total_students = Users.objects.filter(role='student').count()
    
    context = {
        'total_courses': total_courses,
        'total_teachers': total_teachers,
        'total_students': total_students,
    }
    
    return render(request, 'about.html', context)

