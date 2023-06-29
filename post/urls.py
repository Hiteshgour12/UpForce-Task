from django.urls import path
from .views import *


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='Register'),
    path('login/', UserLoginView.as_view(), name='Login'),
    path('post/', PostView.as_view(), name='post'),
    path('post/<int:pk>', PostUpdateView.as_view(), name='post'),
    path('allpost/', AllPostView.as_view(), name='allpost'),
    path('likes/', LikeView.as_view(), name='likes'),
    path('likes/<int:pk>', LikeUpdateView.as_view(), name='likes'),
    path('user/', UserView.as_view(), name='User '),
    path('userlist/', UserListView.as_view(), name='User List'),
    path('userupdate/<int:pk>', UserUpdateView.as_view(), name='User List'),




]
