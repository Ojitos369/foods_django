from django.shortcuts import render
from django.http import (
    HttpResponseRedirect
)
from django.urls import (
    reverse
)

from .models import *
from .forms import UserForm

# Create your views here.
def index(request):
    if request.method == 'POST':
            
        data = dict(request.POST)
        print(data)
        username = data['username'][0]
        email = data['email'][0].lower()
        
        user = User.objects.filter(email=email)
        
        if len(user) == 0:
            user = User(username=username, email=email)
            user.save()
        else:
            user = user[0]
            user.username = username
            user.save()
        
        user = User.objects.filter(email=email)
        user = user[0]
        
        return HttpResponseRedirect(reverse('page:foods', args=(user.id,)))
    return render(request, 'page/index.html')


def foods(request, user_id):
    user = User.objects.filter(id = user_id)[0]
    context = {
        'user': user
    }
    if request.method == 'POST':
        data = dict(request.POST)
        print(data)
        food_id = data['food_id'][0]
        food = Food.objects.filter(id = food_id)[0]
        food.delete()
        message = f"Se elimino {food.food} de las comidas de {user.username}"
        context['message'] = message
    foods = Food.objects.filter(user = user_id)
    context['foods'] = foods
    return render(request, 'page/foods.html', context = context)


def add_food(request, user_id):
    user = User.objects.filter(id = user_id)[0]
    context = {
        'user': user
    }
    if request.method == 'POST':
        data = dict(request.POST)
        print(data)
        food = data['food'][0]
        user_id = data['user_id'][0]
        food = Food(user = user, food = food)
        food.save()
        context['message'] = f"Se agrego {food.food} a las comidas de {user.username}"
    return render(request, 'page/add_food.html', context = context)
