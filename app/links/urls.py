from django.urls import path

from links import views


app_name = 'links'
urlpatterns = [
    path('', views.LinkListView.as_view(), name='links-list'),
    path('add/', views.LinkAddFormView.as_view(), name='links-add'),
    path('delete/<int:pk>/', views.LinkDeleteFormView.as_view(), name='links-delete'),

    path('check/<int:pk>/', views.check, name='links-check')
]