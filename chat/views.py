from django.shortcuts import render

# Create your views here.
def house(request):
    return render(request, 'chat.html')