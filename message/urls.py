from django.urls import include, path
from . import views

urlpatterns = [
    path('inbox/', views.inbox),
    path('outbox/', views.outbox),
    path('trash/', views.trash),
    path('compose/', views.compose),
    path('reply/', views.reply),
    path('delete/', views.delete),
    path('undelete/', views.undelete),
    path('view/', views.view),
]
