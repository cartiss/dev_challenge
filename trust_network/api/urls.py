from django.urls import path, include

from .views import PersonView, TrustConnectionsView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/people/', PersonView.as_view(), name='people'),
    path('api/people/<int:pk>/trust_connections/', TrustConnectionsView.as_view(), name='trust_connections')
]