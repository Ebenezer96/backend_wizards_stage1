from django.urls import path
from .views import ProfileCollectionView, ProfileDetailView

urlpatterns = [
    path("profiles", ProfileCollectionView.as_view()),
    path("profiles/<uuid:profile_id>", ProfileDetailView.as_view()),
]