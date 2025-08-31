from django.urls import path
from . import views

urlpatterns = [
    path('mappings/', views.mapping_list_create, name='mapping-list-create'),
    path('mappings/<int:patient_id>/', views.mapping_by_patient, name='mapping-by-patient'),
    path('mappings/detail/<int:pk>/', views.mapping_detail, name='mapping-detail'),
    path('mappings/status-choices/', views.mapping_status_choices, name='mapping-status-choices'),
]
