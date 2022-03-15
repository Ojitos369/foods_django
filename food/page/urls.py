from django.urls import path
from . import views


app_name = 'page'
urlpatterns = [
    path('/', views.index, name = 'index'),
    path('/add_food/<int:user_id>', views.add_food, name = 'add_food'),
    path('/foods/<int:user_id>', views.foods, name = 'foods'),
]