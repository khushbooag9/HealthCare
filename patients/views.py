from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Patient
from .serializers import PatientSerializer, PatientCreateSerializer, PatientUpdateSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def patient_list_create(request):
    """
    GET: List all patients created by the authenticated user
    POST: Create a new patient
    """
    if request.method == 'GET':
        # Get only patients created by the current user
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientSerializer(patients, many=True)
        return Response({
            'count': patients.count(),
            'patients': serializer.data
        })

    elif request.method == 'POST':
        # Create a new patient
        serializer = PatientCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Set the created_by field to the current user
            patient = serializer.save(created_by=request.user)
            response_serializer = PatientSerializer(patient)
            return Response({
                'message': 'Patient created successfully',
                'patient': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def patient_detail(request, pk):
    """
    GET: Retrieve a specific patient
    PUT: Update a specific patient
    DELETE: Delete a specific patient
    """
    # Get patient and ensure it belongs to the current user
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientUpdateSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            updated_patient = serializer.save()
            response_serializer = PatientSerializer(updated_patient)
            return Response({
                'message': 'Patient updated successfully',
                'patient': response_serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient_name = patient.full_name
        patient.delete()
        return Response({
            'message': f'Patient {patient_name} deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
