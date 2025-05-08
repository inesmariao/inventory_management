from django.urls import path
from .views import (
    ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView,
    ProductSoftDeleteView, ProductRestoreView
)

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductSoftDeleteView.as_view(), name='product-delete'),
    path('<int:pk>/restore/', ProductRestoreView.as_view(), name='product-restore'),
]
