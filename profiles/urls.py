from django.urls import re_path
from .views import ProfileCollectionView, ProfileDetailView

urlpatterns = [
    re_path(r"^profiles/?$", ProfileCollectionView.as_view(), name="profile-collection"),
    re_path(r"^profiles/(?P<pk>[0-9a-fA-F-]+)/?$", ProfileDetailView.as_view(), name="profile-detail"),
]