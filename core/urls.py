from django.urls import path, re_path
from core import views

app_name = 'core'

urlpatterns = [
    path('import/<str:filename>', views.ImportJsonView.as_view(), name='import_json'),
    path('endpoints/', views.EndpointsView.as_view(), name='endpoints_list'),
    path('reports/', views.ReportView.as_view(), name='reports_list'),
    path('profiles/', views.ProfileView.as_view(), name='profiles_list'),
    path('profiles/<int:pk>', views.ProfileDetailView.as_view(), name='profiles_detail'),
    path('profile-posts/', views.PostView.as_view(), name='post_list'),
    path('profile-posts/<int:pk>', views.ProfilePostsView.as_view(), name='profile_posts'),
    path('posts-comments/', views.PostCommentView.as_view(), name='comments_list'),
    path('posts-comments/<int:pk>', views.PostCommentDetailView.as_view(), name='post_comments'),
    path('posts/<int:post_id>/comments', views.CommentView.as_view(), name='post_comments_list'),
    path('posts/<int:post_id>/comments/<int:comment_id>', views.CommentDetailView.as_view(), name='post_comment_detail'),
    # re_path(r'profiles/<int:pk>/(?P<filename>[^/]+)$', ProfileDetailView.as_view()),
    # path('profiles/<int:pk>/<str:filename>', ProfileDetailView.as_view()),
    # re_path(r'profiles/(?P<filename>[^/]+)$', ProfileView.as_view()),
]
