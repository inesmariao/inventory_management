from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Company
from .serializers import (
    CompanySerializer,
    CompanyReadSerializer,
    CompanyPublicSerializer
)
from apps.identity.role_permissions import IsAdmin
from drf_spectacular.utils import extend_schema, OpenApiResponse


class CompanyCreateView(generics.CreateAPIView):
    """
    Allows an admin user to create a new company.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class CompanyListView(generics.ListAPIView):
    """
    Returns a list of all active companies (internal use).
    """
    serializer_class = CompanyReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(is_active=True)


class CompanyDetailView(generics.RetrieveAPIView):
    """
    Returns detailed information about a specific company.
    """
    queryset = Company.objects.all()
    serializer_class = CompanyReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'


class CompanyUpdateView(generics.UpdateAPIView):
    """
    Allows an admin to update a specific company's details.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'pk'


@extend_schema(
    description="Soft deletes a company by marking it as inactive.",
    responses={
        200: OpenApiResponse(description="Company deactivated."),
        404: OpenApiResponse(description="Company not found.")
    }
)
class CompanySoftDeleteView(APIView):
    """
    Performs soft deletion of a company by setting is_active=False and storing the deletion timestamp.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def delete(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            company.is_active = False
            company.deleted_at = timezone.now()
            company.save()
            return Response({"message": "Company deactivated successfully."}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    description="Restores a previously deactivated company.",
    responses={
        200: OpenApiResponse(description="Company restored."),
        400: OpenApiResponse(description="Company is already active."),
        404: OpenApiResponse(description="Company not found.")
    }
)
class CompanyRestoreView(APIView):
    """
    Allows an admin to reactivate a previously soft-deleted company.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            if company.is_active:
                return Response({"message": "Company is already active."}, status=status.HTTP_400_BAD_REQUEST)
            company.is_active = True
            company.deleted_at = None
            company.save()
            return Response({"message": "Company restored successfully."}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    description="Public list of active companies. No authentication required.",
    responses={200: OpenApiResponse(description="List of active companies")}
)
class CompanyPublicListView(generics.ListAPIView):
    """
    Publicly accessible list of all active companies, with readable location names.
    """
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanyPublicSerializer
    permission_classes = []
