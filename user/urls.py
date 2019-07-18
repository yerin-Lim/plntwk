from django.urls import include, path
from .views import RegisterUserView, UserDetailView, CustomLogin, UserView,CustomLogout

urlpatterns = [
    path('',UserView.as_view()),
    path('<int:pk>', UserDetailView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('login/', CustomLogin.as_view()),
    path('logout/', CustomLogout.as_view()),
]