from django.urls import path, re_path
from . import views


app_name = 'page'
urlpatterns = [
    path('/', views.IndexView.as_view(), name = 'index'),
    path('/add_food/<int:user_id>', views.AddFood.as_view(), name = 'add_food'),
    path('/foods/<int:user_id>', views.FoodView.as_view(), name = 'foods'),
]