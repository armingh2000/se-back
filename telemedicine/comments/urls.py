from django.urls import path
from .views import *


urlpatterns = [
    # Comment
    path('create_comment/', CreateCommentView.as_view(), name='rest_create_comment'),
    path('get_comment_list/', CommentListView.as_view(), name='rest_comment_list'),
]
