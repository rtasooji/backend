from django.urls import path
from user import views


app_name = 'user'
# the name in path is to identify when using reverse lookup function and the
# app is the first argument in revers
# reverse(user:create)
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name="me"),
]
