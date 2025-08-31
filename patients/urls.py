from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.patient_list_create, name='patient-list-create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient-detail'),
]
