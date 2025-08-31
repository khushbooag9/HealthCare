from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from patients.models import Patient
from .serializers import (
    PatientDoctorMappingSerializer,
    PatientDoctorMappingCreateSerializer,
    PatientDoctorMappingUpdateSerializer
)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mapping_list_create(request):
    """
    GET: List all patient-doctor mappings created by the authenticated user
    POST: Create a new patient-doctor mapping
    """
    if request.method == 'GET':
        # Get only mappings created by the current user
        mappings = PatientDoctorMapping.objects.filter(created_by=request.user)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status', None)
        if status_filter:
            mappings = mappings.filter(status=status_filter)
        
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response({
            'count': mappings.count(),
            'mappings': serializer.data
        })

    elif request.method == 'POST':
        # Create a new mapping
        serializer = PatientDoctorMappingCreateSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            # Set the created_by field to the current user
            mapping = serializer.save(created_by=request.user)
            response_serializer = PatientDoctorMappingSerializer(mapping)
            return Response({
                'message': 'Patient-Doctor mapping created successfully',
                'mapping': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mapping_by_patient(request, patient_id):
    """
    GET: Retrieve all doctors assigned to a specific patient
    """
    # Ensure the patient belongs to the current user
    patient = get_object_or_404(Patient, pk=patient_id, created_by=request.user)
    
    # Get all mappings for this patient
    mappings = PatientDoctorMapping.objects.filter(
        patient=patient,
        created_by=request.user
    )
    
    # Filter by status if provided
    status_filter = request.query_params.get('status', None)
    if status_filter:
        mappings = mappings.filter(status=status_filter)
    
    serializer = PatientDoctorMappingSerializer(mappings, many=True)
    return Response({
        'patient': patient.full_name,
        'count': mappings.count(),
        'doctors': serializer.data
    })


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def mapping_detail(request, pk):
    """
    PUT: Update a specific mapping (e.g., change status)
    DELETE: Delete a specific mapping
    """
    # Get mapping and ensure it belongs to the current user
    mapping = get_object_or_404(PatientDoctorMapping, pk=pk, created_by=request.user)

    if request.method == 'PUT':
        serializer = PatientDoctorMappingUpdateSerializer(
            mapping, 
            data=request.data, 
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            updated_mapping = serializer.save()
            response_serializer = PatientDoctorMappingSerializer(updated_mapping)
            return Response({
                'message': 'Mapping updated successfully',
                'mapping': response_serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient_name = mapping.patient.full_name
        doctor_name = mapping.doctor.full_name
        mapping.delete()
        return Response({
            'message': f'Removed Dr. {doctor_name} from patient {patient_name}'
        }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mapping_status_choices(request):
    """
    Get list of all available status choices.
    """
    status_choices = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in PatientDoctorMapping.STATUS_CHOICES
    ]
    return Response({
        'status_choices': status_choices
    })
