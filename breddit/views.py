from django.shortcuts import render, get_object_or_404
from .serializers import PostSerializer, CommentSerializer, UserSerializer, LoginSerializer, RegisterSerializer, ChangePasswordSerializer
from .models import Post, Comment, User
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
      serializer.save(owner=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
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
        print(lookup_field_value)

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
      
class ChangePasswordView(viewsets.ModelViewSet):
    http_method_names = ['put']
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
  

def up_vote(request):
  username = request.user.username
  post_id = request.GET.get(post_id)
  post = Post.objects.get(id=post_id)
  
  like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
  
  if like_filter == None:
    new_like = LikePost.objects.create(post_id=post_id, username=username)
    new_like.save()
    post.no_likes = post.no_likes+1
    post.save()
    return redirect('/')
  else:
    like_filter.delete()
    post.no_likes = post.no_likes-1
    post.save()
    return redirect('/')
