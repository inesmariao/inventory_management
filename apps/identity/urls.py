from django.urls import path
from .views import (
    LoginView,
    UserCreateView, UserListView, UserDetailView, UserUpdateView, UserSoftDeleteView, UserRestoreView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserSoftDeleteView.as_view(), name='user-soft-delete'),
    path('users/<int:pk>/restore/', UserRestoreView.as_view(), name='user-restore'),
]
