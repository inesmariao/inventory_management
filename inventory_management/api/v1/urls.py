from django.urls import path, include

urlpatterns = [
    path('identity/', include('apps.identity.urls')),
    path('company/', include('apps.company.urls')),
    path('product/', include('apps.product.urls')),
    path('inventory/', include('apps.inventory.urls')),
]
