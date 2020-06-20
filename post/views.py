import pytz
from datetime import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json

from film.models import Film
from post.models import Post, UserCommentPost, UserLikePost
from post.serializers import PostSerializer
from user.models import ManagerUserPost


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    post: dict = request.POST
    if 'nameFilm' not in post.keys():
        return JsonResponse(data={'message': 'NAME_FILM_REQUIRE'}, status=400)
    if 'filmType' not in post.keys():
        return JsonResponse(data={'message': 'TYPE_OF_FILM_REQUIRE'}, status=400)
    if 'title' not in post.keys():
        return JsonResponse(data={'message': 'POST_TITLE_REQUIRE'}, status=400)
    if 'content' not in post.keys():
        return JsonResponse(data={'message': 'POST_CONTENT_REQUIRE'}, status=400)
    if 'picture' not in request.FILES:
        return JsonResponse(data={'message': 'POST_PICTURE_REQUIRE'}, status=400)
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    try:
        managerUserPost = ManagerUserPost.objects.get(user_id=user.id, deleted_at=None)
    except ManagerUserPost.DoesNotExist:
        return JsonResponse(dict(message='USER_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    picture = request.FILES['picture']
    try:
        if not isinstance(int(post['filmType']), int):
            return JsonResponse(data={'message': 'TYPE_OF_FILM_NOT_VALID'}, status=400)
    except:
        return JsonResponse(data={'message': 'TYPE_OF_FILM_NOT_VALID'}, status=400)
    managerUserPost.numberPost = managerUserPost.numberPost + 1
    managerUserPost.save()
    newPost = Post.objects.create(
        user_id=user.id,
        title=post['title'],
        film_type = int(post['filmType']),
        name_film=post['nameFilm'],
        content=post['content'],
        picture=picture
    )
    newPost.save()
    return JsonResponse(dict(id=newPost.id,
                             userId=newPost.user_id,
                             title=newPost.title,
                             nameFilm=newPost.name_film,
                             filmType = newPost.film_type,
                             content=newPost.content,
                             picture=json.dumps(str(newPost.picture)),
                             ), status=status.HTTP_200_OK
                        )


@api_view(['GET'])
def getPosts(request):
    posts: list = []
    for e in Post.objects.filter(deleted_at=None).select_related('user'):
        post: dict = {
            'id': str(e.id),
            'title': e.title,
            'nameFilm': e.name_film,
            'filmType': e.film_type,
            'content': e.content,
            'picture': json.dumps(str(e.picture)),
            'like': e.like,
            'commentCount': e.comment_count,
            'createdAt': e.created_at,
            'user': {
                'username': e.user.username,
                'firstName': e.user.first_name,
                'lastName': e.user.last_name
            }
        }
        posts.append(post)
    response = dict(data=posts)
    return JsonResponse(data=response, content_type='application/json')

@api_view(['GET'])
def getPostByUser(request,userId):
    posts: list = []
    for e in Post.objects.filter(user_id=userId, deleted_at=None).select_related('user'):
        post: dict = {
            'id': str(e.id),
            'title': e.title,
            'nameFilm': e.name_film,
            'filmType': e.film_type,
            'content': e.content,
            'picture': json.dumps(str(e.picture)),
            'like': e.like,
            'commentCount': e.comment_count,
            'createdAt': e.created_at,
            'user': {
                'username': e.user.username,
                'firstName': e.user.first_name,
                'lastName': e.user.last_name
            }
        }
        posts.append(post)
    response = dict(data=posts)
    return JsonResponse(data=response, content_type='application/json')


@api_view(['GET'])
def getPost(request, postId):
    comments: list = []
    try:
        post = Post.objects.select_related('user').get(id=postId, deleted_at=None)
        commentsQuery = UserCommentPost.objects.select_related('user').filter(post_id=postId, deleted_at=None)
        for value in commentsQuery:
            comment: dict = {
                'id': value.id,
                'content': value.content,
                'user': value.user.username
            }
            print(comment)
            comments.append(comment)
            print(comments)
        likes = UserLikePost.objects.filter(post_id=postId, deleted_at=None)
        userLikes: list = []
        for like in likes:
            userLikes.append(like.user_id)
        response: dict = {
            'id': post.id,
            'title': post.title,
            'nameFilm': post.name_film,
            'content': post.content,
            'filmType': post.film_type,
            'picture': json.dumps(str(post.picture)),
            'like': post.like,
            'commentCount': post.comment_count,
            'createdAt': post.created_at,
            'user': {
                'username': post.user.username,
                'firstName': post.user.first_name,
                'lastName': post.user.last_name
            },
            'comments': comments,
            'userLikes':userLikes
        }
        return JsonResponse(data=dict(data=response), content_type='application/json')
    except Post.DoesNotExist:
        return JsonResponse(dict(message='POST_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePost(request, postId):
    try:
        post = Post.objects.get(id=postId, deleted_at=None)
    except Post.DoesNotExist:
        return JsonResponse(dict(message='POST_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    if user.id != post.user.id:
        return JsonResponse(dict(message='USER_NOT_VALID'), status=status.HTTP_404_NOT_FOUND)
    if 'title' in request.data.keys():
        post.title = request.data['title']
    if 'nameFilm' in request.data.keys():
        post.name_film = request.data['nameFilm']
    if 'filmType' in request.data.keys():
        try:
            if not isinstance(int(request.data['filmType']), int):
                return JsonResponse(data={'message': 'TYPE_OF_FILM_NOT_VALID'}, status=400)
        except:
            return JsonResponse(data={'message': 'TYPE_OF_FILM_NOT_VALID'}, status=400)
        post.film_type = int(request.data['filmType'])
    if 'content' in request.data.keys():
        post.content = request.data['content']
    if 'picture' in request.FILES.keys():
        post.picture = request.FILES['picture']
    post.save()
    return JsonResponse(dict(id=post.id,
                             nameFilm=post.name_film,
                             filmType = post.film_type,
                             title=post.title,
                             content=post.content,
                             like=post.like,
                             commentCount=post.comment_count,
                             picture=json.dumps(str(post.picture)),
                             user=post.user.id
                             ), status=status.HTTP_200_OK
                        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePost(request, postId):
    try:
        post = Post.objects.get(id=postId, deleted_at=None)
    except Post.DoesNotExist:
        return JsonResponse(dict(message='POST_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    if user.id != post.user.id:
        return JsonResponse(dict(message='USER_NOT_VALID'), status=status.HTTP_404_NOT_FOUND)
    deletedAt = datetime.utcnow().replace(tzinfo=pytz.utc)
    post.deleted_at = deletedAt
    post.save()
    return JsonResponse(dict(status=True), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def commentPost(request):
    commentInput: dict = request.data
    if 'postId' not in commentInput.keys():
        return JsonResponse(data={'message': 'POST_ID_REQUIRE'}, status=400)
    if 'content' not in commentInput.keys():
        return JsonResponse(data={'message': 'CONTENT_REQUIRE'}, status=400)
    try:
        post = Post.objects.get(id=commentInput['postId'], deleted_at=None)
    except Post.DoesNotExist:
        return JsonResponse(dict(message='POST_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    newComment = UserCommentPost.objects.create(
        user_id=user.id,
        post_id=commentInput['postId'],
        content=commentInput['content']
    )
    newComment.save()
    post.comment_count += 1
    post.save()
    return JsonResponse(dict(id=newComment.id,
                             userId=newComment.user_id,
                             postId=newComment.post_id,
                             content=newComment.content
                             ), status=status.HTTP_200_OK
                        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateComment(request, commentId):
    try:
        comment = UserCommentPost.objects.get(id=commentId, deleted_at=None)
    except UserCommentPost.DoesNotExist:
        return JsonResponse(dict(message='COMMENT_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    if user.id != comment.user.id:
        return JsonResponse(dict(message='USER_NOT_VALID'), status=status.HTTP_404_NOT_FOUND)
    if 'content' in request.data.keys():
        comment.content = request.data['content']
    comment.save()
    return JsonResponse(dict(id=comment.id,
                             content=comment.content,
                             user=comment.user.id
                             ), status=status.HTTP_200_OK
                        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteComment(request, commentId):
    try:
        comment = UserCommentPost.objects.get(id=commentId, deleted_at=None)
    except UserCommentPost.DoesNotExist:
        return JsonResponse(dict(message='COMMENT_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    if user.id != comment.user.id:
        return JsonResponse(dict(message='USER_NOT_VALID'), status=status.HTTP_404_NOT_FOUND)
    try:
        post = Post.objects.get(id=comment.post.id, deleted_at=None)
    except Post.DoesNotExist:
        return JsonResponse(dict(message='POST_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    deletedAt = datetime.utcnow().replace(tzinfo=pytz.utc)
    comment.deleted_at = deletedAt
    comment.save()
    post.comment_count = post.comment_count - 1
    post.save()
    return JsonResponse(dict(status=True), status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likePost(request):
    likeInput: dict = request.data
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    if 'postId' not in likeInput.keys():
        return JsonResponse(data={'message': 'POST_ID_REQUIRE'}, status=400)
    try:
        post = Post.objects.get(id=likeInput['postId'], deleted_at=None)
    except Post.DoesNotExist:
        return JsonResponse(dict(message='POST_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)

    try:
        managerUserPost = ManagerUserPost.objects.get(user_id=post.user_id, deleted_at=None)
    except ManagerUserPost.DoesNotExist:
        return JsonResponse(dict(message='USER_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)

    like = UserLikePost.objects.filter(post_id=likeInput['postId'], user_id=user.id, deleted_at=None)
    if len(like) > 0:
        return JsonResponse(dict(message='LIKE_EXISTED'), status=status.HTTP_409_CONFLICT)
    else:
        newLike = UserLikePost.objects.create(
            user_id=user.id,
            post_id=likeInput['postId']
        )
        newLike.save()
        post.like += 1
        post.save()
        managerUserPost.numberLike = managerUserPost.numberLike + 1
        managerUserPost.save()
        return JsonResponse(dict(id=newLike.id,
                                 userId=newLike.user_id,
                                 postId=newLike.post_id,
                                 ), status=status.HTTP_200_OK
                            )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancelLike(request):
    likeInput: dict = request.data
    if 'postId' not in likeInput.keys():
        return JsonResponse(data={'message': 'POST_ID_REQUIRE'}, status=400)
    try:
        post = Post.objects.get(id=likeInput['postId'], deleted_at=None)
    except Post.DoesNotExist:
        return JsonResponse(dict(message='POST_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    try:
        like = UserLikePost.objects.get(post_id=likeInput['postId'], user_id=user.id, deleted_at=None)
    except UserLikePost.DoesNotExist:
        return JsonResponse(dict(message='LIKE_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    try:
        managerUserPost = ManagerUserPost.objects.get(user_id=post.user_id, deleted_at=None)
    except ManagerUserPost.DoesNotExist:
        return JsonResponse(dict(message='USER_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)

    deletedAt = datetime.utcnow().replace(tzinfo=pytz.utc)
    like.deleted_at = deletedAt
    like.save()
    post.like = post.like - 1
    post.save()
    managerUserPost.numberLike = managerUserPost.numberLike - 1
    managerUserPost.save()
    return JsonResponse(dict(status=True), status=status.HTTP_200_OK)
