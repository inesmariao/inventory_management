from django.urls import path
from .views import (
    CompanyCreateView,
    CompanyListView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanySoftDeleteView,
    CompanyRestoreView,
    CompanyPublicListView
)

urlpatterns = [

    # Admin-only endpoints
    path('', CompanyListView.as_view(), name='company-list'),
    path('create/', CompanyCreateView.as_view(), name='company-create'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('<int:pk>/update/', CompanyUpdateView.as_view(), name='company-update'),
    path('<int:pk>/delete/', CompanySoftDeleteView.as_view(), name='company-delete'),
    path('<int:pk>/restore/', CompanyRestoreView.as_view(), name='company-restore'),

    # Internal read-only endpoints
    path('', CompanyListView.as_view(), name='company-list'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    # Public access (no auth required)
    path('public/', CompanyPublicListView.as_view(), name='company-public-list'),

]