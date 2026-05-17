from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Student, Instructor, Vehicle, Course, Enrollment, Lesson
from .serializers import (
    StudentSerializer, StudentPictureSerializer, InstructorSerializer, VehicleSerializer,
    CourseSerializer, EnrollmentSerializer, LessonSerializer
)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'first_name', 'last_name']

    @action(
        detail=True,
        methods=['post'],
        url_path='upload-picture',
        parser_classes=[MultiPartParser, FormParser]
    )
    def upload_picture(self, request, pk=None):
        student = self.get_object()

        incoming_file = request.FILES.get('profile_picture')

        if not incoming_file:
            return Response(
                {'detail': 'Debes enviar el archivo en el campo "profile_picture".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        allowed_types = ['image/jpeg', 'image/png']
        max_size = 2 * 1024 * 1024  # 2MB

        if incoming_file.content_type not in allowed_types:
            return Response(
                {'detail': 'Solo se permiten imagenes JPG o PNG.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if incoming_file.size > max_size:
            return Response(
                {'detail': 'La imagen no puede superar 2MB.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = StudentPictureSerializer(
            student,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                StudentSerializer(
                    student,
                    context={"request": request}
                ).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
