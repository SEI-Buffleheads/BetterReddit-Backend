from rest_framework.routers import SimpleRouter
from .views import UserViewSet, LoginViewSet, RegistrationViewSet, RefreshViewSet, PostViewSet, CommentViewSet, ChangePasswordView, UpdateAvatarView

routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
routes.register(r'auth/changePW', ChangePasswordView, basename='auth-ChangePW')
routes.register(r'auth/updateProfile', UpdateAvatarView, basename='auth-updateProfile')

# USER
routes.register(r'user', UserViewSet, basename='user')

# Post and Comments
routes.register(r'posts', PostViewSet)
routes.register(r'comments', CommentViewSet)

urlpatterns = [
    *routes.urls,
]