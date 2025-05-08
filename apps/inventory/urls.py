from django.urls import path
from .views import (
    InventoryItemCreateView,
    InventoryItemListView,
    InventoryItemDetailView,
    InventoryItemUpdateView,
    InventoryItemDeleteView
)

urlpatterns = [
    path('item/create/', InventoryItemCreateView.as_view(), name='inventory-create'),
    path('items/', InventoryItemListView.as_view(), name='inventory-list'),
    path('item/<int:pk>/', InventoryItemDetailView.as_view(), name='inventory-detail'),
    path('item/<int:pk>/update/', InventoryItemUpdateView.as_view(), name='inventory-update'),
    path('item/<int:pk>/delete/', InventoryItemDeleteView.as_view(), name='inventory-delete'),
]
