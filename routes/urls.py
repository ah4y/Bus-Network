from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('route/<int:route_id>/', views.route_detail, name='route_detail'),
    path('route/<int:route_id>/book/', views.book, name='book'),
    path('route/<int:route_id>/unbook/', views.unbook, name='unbook'),
    path('station/<int:station_id>/', views.station_detail, name='station_detail'),
    path('my-routes/', views.my_routes, name='my_routes'),
    path('register/', views.register_view, name='register'),
]
