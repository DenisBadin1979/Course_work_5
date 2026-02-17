from rest_framework import viewsets, permissions

from users.models import User
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializers

from rest_framework import permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]