from rest_framework.routers import SimpleRouter
from .views import UserViewSet, LoginViewSet, RegistrationViewSet, RefreshViewSet, PostViewSet, CommentViewSet 

routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# USER
routes.register(r'user', UserViewSet, basename='user')

# Post and Comments
routes.register(r'posts', PostViewSet)
routes.register(r'comments', CommentViewSet)

urlpatterns = [
    *routes.urls,
]