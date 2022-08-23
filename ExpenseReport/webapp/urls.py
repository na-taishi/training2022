from django.urls import path

from . import views

app_name='webapp'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('top/', views.TopView.as_view(), name='top'),
    path('route/', views.RouteView.as_view(), name='route'),
    path('route/delete/', views.RouteDeleteView.as_view(), name='route_delete'),
    path('route-list/', views.RouteListView.as_view(), name='route_list'),
    path('', views.ExpenseReportView.as_view()),
    path('expense-report/', views.ExpenseReportView.as_view(), name='expense_report'),
]