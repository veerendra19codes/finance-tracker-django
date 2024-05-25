from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  
    path('profile/', views.profile, name='profile'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('edit_income/<int:id>/', views.edit_income, name='edit_income'),
    path('edit_expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete_income/<int:id>/', views.delete_income, name='delete_income'),
    path('delete_expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('report/', views.report, name='report'),
    path('add_budget/', views.add_budget, name='add_budget'),
    path('budget_progress/', views.budget_progress, name='budget_progress'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('all-incomes/', views.all_incomes, name='all_incomes'),
    path('all-expenses/', views.all_expenses, name='all_expenses'),
    path('api/chart-data/', views.chart_data, name='chart_data'),
]
