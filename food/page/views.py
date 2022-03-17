from django.shortcuts import render
from django.http import (
    HttpResponseRedirect
)

from django.urls import (
    reverse,
    reverse_lazy
)

from django.views.generic import (
    FormView
)

from .models import *
from .forms import UserForm, FoodForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        
        if userForm.is_valid():
            data = userForm.cleaned_data
            print(data)
            username = data['username']
            email = data['email'].lower()
            
            user = User.objects.filter(email=email)
            
            if len(user) == 0:
                user = User(username=username, email=email)
                user.save()
            else:
                user = user[0]
                user.username = username
                user.save()
            
            user = User.objects.filter(email=email)[0]
            
            return HttpResponseRedirect(reverse('page:foods', args=(user.id,)))
        else:
            context = {
                'title': 'Error'
            }
            return render(request, 'page/index.html', context = context)
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


"""def add_food(request, user_id):
    user = User.objects.filter(id = user_id)[0]
    context = {
        'user': user
    }
    if request.method == 'POST':
        foodForm = FoodForm(request.POST)
        if foodForm.is_valid():
            data = foodForm.cleaned_data
            food = data['food']
            user_id = data['user_id']
            food = Food(user = user, food = food)
            food.save()
            context['message'] = f"Se agrego {food.food} a las comidas de {user.username}"
        else:
            context = {
                'title': 'Error'
            }
            return render(request, 'page/add_food.html', context = context)
    return render(request, 'page/add_food.html', context = context)
"""

class AddFood(FormView):
    template_name = 'page/add_food.html'
    form_class = FoodForm
    success_url = ''
    message = {
        'message': None
    }

    def form_valid(self, form, **kwargs):
        data = form.cleaned_data
        food = data['food']
        user_id = data['user_id']
        self.success_url = reverse_lazy('page:add_food', args=(user_id,))
        user = User.objects.filter(id = user_id)[0]
        food = Food(user = user, food = food)
        food.save()
        self.message['message'] = f"Se agrego {food.food} a las comidas de {user.username}"
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        context['user'] = User.objects.filter(id = user_id)[0]
        if self.message['message']:
            context['message'] = self.message['message']
        return context
