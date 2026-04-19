from django.urls import path
from .views import ProfileCollectionView, ProfileDetailView

urlpatterns = [
    path("profiles", ProfileCollectionView.as_view(), name="profile-collection"),
    path("profiles/<int:profile_id>", ProfileDetailView.as_view(), name="profile-detail"),
]