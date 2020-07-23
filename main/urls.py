from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('cart/', views.cart_view, name='cart'),
    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('dish_delete/<int:question_id>/', views.dish_delete, name='deletedish'),
    path('dish_edit/<int:pk>/', views.DishUpdateView.as_view(), name='updatedish'),
    path('search_dish/', views.search_dish, name='search_dish'),
    path('createdish/', views.DishCreate.as_view(), name='createdish'),
    path('<int:pk>/', views.DishDetailView.as_view(), name='detail'),
]
