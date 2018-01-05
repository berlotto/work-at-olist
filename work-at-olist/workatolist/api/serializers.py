from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.reverse import reverse

from workatolist.models import Channel, Category


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ('url', 'name', 'slug')
        extra_kwargs = {
            'url': {'view_name': 'channel-detail', 'lookup_field': 'slug'},
        }


class CategorySlugRelatedField(serializers.SlugRelatedField):

    def to_representation(self, value):
        if value.parent:
            request = self.context['request']
            url = reverse(
                'category-detail', args=[value.parent.slug], request=request)
            return url
        return None


class ChannelSlugRelatedField(serializers.SlugRelatedField):

    def to_representation(self, value):
        if value.slug:
            request = self.context['request']
            url = reverse(
                'channel-detail', args=[value.slug], request=request)
            return url
        return None


class CategorySerializer(serializers.ModelSerializer):
    parent = CategorySlugRelatedField(
        many=False,
        read_only=False,
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    channel = ChannelSlugRelatedField(
        many=False,
        read_only=False,
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Category
        fields = ('slug', 'name', 'channel', 'parent')
