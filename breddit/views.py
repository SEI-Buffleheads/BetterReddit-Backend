from django.shortcuts import render, get_object_or_404
from .serializers import PostSerializer, CommentSerializer, UserSerializer, LoginSerializer, RegisterSerializer, ChangePasswordSerializer
from .models import Post, Comment, User
from .form import *
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
# from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
# from rest_framework.decorators import api_view, permission_classes
# import os

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
      serializer.save(owner=self.request.user)
      
    def perform_update(self, serializer):
      serializer.save(owner=self.request.user)    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
      serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
      serializer.save(owner=self.request.user)   
      
class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    filter_backends = [filters.OrderingFilter]

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return User.objects.all()
    
    def get_queryset(self):
        if self.request.user:
            return User.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]

        obj = User.objects.get(id=lookup_field_value)
        self.check_object_permissions(self.request, obj)

        return obj

class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "access": res["access"]
        }, status=status.HTTP_201_CREATED)


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
      
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikedPostView(APIView):
    bad_request_message = 'An error has occurred'

    def post(self, request):
        post = get_object_or_404(Post, id=request.data.get('id'))
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            return Response({'detail': 'User liked the post'}, status=status.HTTP_200_OK)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        post = get_object_or_404(Post, id=request.data.get('id'))
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'detail': 'User unliked the post'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

class FavoriteView(APIView):
    bad_request_message = 'An error has occurred'

    def post(self, request):
        post = get_object_or_404(Post, id=request.data.get('id'))
        user = request.user
        if  post not in user.favorites.all():
            user.favorites.add(post)
            return Response({'detail': 'User favorited the post'}, status=status.HTTP_200_OK)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        post = get_object_or_404(Post, id=request.data.get('id'))
        user = request.user
        if  post in user.favorites.all():
            user.favorites.remove(post)
            return Response({'detail': 'User unfavorited the post'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

# class UpdateView(APIView):  
#     bad_request_message = 'An error has occurred'
  
#     def post(self, request):
#         user = request.user
#         form = ImageForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#           avatar = user.avatar.path
#           if os.path.exists(avatar):
#               os.remove(avatar)
#           form.save()
#         return Response({'detail': "okie"})


# @ensure_csrf_cookie
# def edit(request):
#     if request.method == "POST":
#         user = request.user
#         form = ImageForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#         return Response({'detail': "okie"})
#     else:
#       return Response({'detail': "NOPE"})


