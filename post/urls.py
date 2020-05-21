from django.urls import path

from post.views import createPost, getPosts, getPost, updatePost, deletePost, commentPost, updateComment, deleteComment, likePost, cancelLike, dislikePost, cancelDislike

urlpatterns = [
    path('', getPosts, name='get_posts'),
    path('<str:postId>', getPost, name='get_post'),
    path('create/', createPost, name='create_post'),
    path('update/<str:postId>', updatePost, name='update_post'),
    path('delete/<str:postId>', deletePost, name='delete_post'),
    path('create-comment/', commentPost, name='comment_post'),
    path('update-comment/<str:commentId>', updateComment, name='update_comment'),
    path('delete-comment/<str:commentId>', deleteComment, name='delete_comment'),
    path('create-like/', likePost, name='like_post'),
    path('cancel-like/', cancelLike, name='cancel_like'),
    path('create-dislike/', dislikePost, name='dislike_post'),
    path('cancel-dislike/', cancelDislike, name='cancel_dislike'),
]