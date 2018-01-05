from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from workatolist.api.serializers import (
    UserSerializer,
    GroupSerializer,
    ChannelSerializer,
    CategorySerializer,
)
from workatolist.models import Channel, Category


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allow channels do be viwed or edited.
    """
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = "slug"


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allow categories do be viwed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
