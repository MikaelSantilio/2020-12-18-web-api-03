from django.urls import path, re_path
from core.views import ProfileView, ProfileDetailView

urlpatterns = [
    path('profiles/<int:pk>', ProfileDetailView.as_view()),
    # re_path(r'profiles/<int:pk>/(?P<filename>[^/]+)$', ProfileDetailView.as_view()),
    path('profiles/<int:pk>/<str:filename>', ProfileDetailView.as_view()),
    re_path(r'profiles/(?P<filename>[^/]+)$', ProfileView.as_view()),
    path('profile/', ProfileView.as_view()),
]
