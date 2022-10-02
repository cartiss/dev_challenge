from django.urls import path, include

from .views import PersonView, TrustConnectionsView, MessageView, PathView

urlpatterns = [
    path('people/', PersonView.as_view(), name='people'),
    path('people/<int:pk>/trust_connections/', TrustConnectionsView.as_view(), name='trust_connections'),
    path('messages/', MessageView.as_view(), name='messages'),
    path('path/', PathView.as_view(), name='path')
]