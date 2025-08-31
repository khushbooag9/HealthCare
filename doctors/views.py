from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Doctor
from .serializers import (
    DoctorSerializer, 
    DoctorCreateSerializer, 
    DoctorUpdateSerializer, 
    DoctorListSerializer
)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def doctor_list_create(request):
    """
    GET: List all active doctors (public list for all users)
    POST: Create a new doctor (only authenticated users)
    """
    if request.method == 'GET':
        # Get all active doctors (not filtered by user)
        doctors = Doctor.objects.filter(is_active=True)
        
        # Filter by specialization if provided
        specialization = request.query_params.get('specialization', None)
        if specialization:
            doctors = doctors.filter(specialization=specialization)
            
        # Filter by city if provided
        city = request.query_params.get('city', None)
        if city:
            doctors = doctors.filter(city__icontains=city)
        
        serializer = DoctorListSerializer(doctors, many=True)
        return Response({
            'count': doctors.count(),
            'doctors': serializer.data
        })

    elif request.method == 'POST':
        # Create a new doctor
        serializer = DoctorCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Set the created_by field to the current user
            doctor = serializer.save(created_by=request.user)
            response_serializer = DoctorSerializer(doctor)
            return Response({
                'message': 'Doctor created successfully',
                'doctor': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def doctor_detail(request, pk):
    """
    GET: Retrieve a specific doctor (public access)
    PUT: Update a specific doctor (only creator can update)
    DELETE: Delete a specific doctor (only creator can delete)
    """
    # For GET request, allow access to any active doctor
    if request.method == 'GET':
        doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)
    
    # For PUT and DELETE, only allow access to doctors created by the current user
    else:
        doctor = get_object_or_404(Doctor, pk=pk, created_by=request.user)
        
        if request.method == 'PUT':
            serializer = DoctorUpdateSerializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                updated_doctor = serializer.save()
                response_serializer = DoctorSerializer(updated_doctor)
                return Response({
                    'message': 'Doctor updated successfully',
                    'doctor': response_serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            doctor_name = doctor.full_name
            doctor.delete()
            return Response({
                'message': f'Doctor {doctor_name} deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_specializations(request):
    """
    Get list of all available specializations.
    """
    specializations = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in Doctor.SPECIALIZATION_CHOICES
    ]
    return Response({
        'specializations': specializations
    })
