from django.urls import path
from .views import (
    InventoryItemCreateView,
    InventoryItemListView,
    InventoryItemDetailView,
    InventoryItemUpdateView,
    InventoryItemDeleteView,
    generate_inventory_pdf,
    send_inventory_pdf_email
)

urlpatterns = [
    path('item/create/', InventoryItemCreateView.as_view(), name='inventory-create'),
    path('items/', InventoryItemListView.as_view(), name='inventory-list'),
    path('item/<int:pk>/', InventoryItemDetailView.as_view(), name='inventory-detail'),
    path('item/<int:pk>/update/', InventoryItemUpdateView.as_view(), name='inventory-update'),
    path('item/<int:pk>/delete/', InventoryItemDeleteView.as_view(), name='inventory-delete'),
    path('generate_pdf/', generate_inventory_pdf, name='generate_inventory_pdf'),
    path('send_pdf/', send_inventory_pdf_email, name='send_inventory_pdf_email'),
]
