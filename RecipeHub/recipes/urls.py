from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recipes/', views.dashboard_recipe_list, name='dashboard_recipe_list'),
    path('dashboard/recipes/new/', views.recipe_create, name='recipe_create'),
    path('dashboard/recipes/<int:pk>/', views.dashboard_recipe_detail, name='dashboard_recipe_detail'),
    path('dashboard/recipes/<int:pk>/edit/', views.recipe_update, name='recipe_update'),
    path('dashboard/recipes/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
]