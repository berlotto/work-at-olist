import re

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

    def to_internal_value(self, value):
        assert isinstance(value, str), \
            "value is not a string: {0}".format(value)
        m = re.search(r"/(?P<slug>[\w-]+)/$", value)
        if m:
            the_category = Category.objects.filter(
                slug=m.groupdict()['slug']).first()
            return the_category
        elif value:
            the_category = Category.objects.filter(slug=value).first()
        if the_category:
            return the_category
        else:
            return None

    def to_representation(self, value):
        if value:
            request = self.context['request']
            url = reverse(
                'category-detail', args=[value.slug], request=request)
            return url
        return None


class ChannelSlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, value):
        assert isinstance(value, str), \
            "value is not a string: {0}".format(value)
        m = re.search(r"/(?P<slug>[\w-]+)/$", value)
        if m:
            the_channel = Channel.objects.filter(
                slug=m.groupdict()['slug']).first()
            return the_channel
        elif value:
            the_channel = Channel.objects.filter(slug=value).first()
        if the_channel:
            return the_channel
        else:
            return None

    def to_representation(self, value):
        if value.slug:
            request = self.context['request']
            url = reverse(
                'channel-detail', args=[value.slug], request=request)
            return url
        return None


class SubCategory(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'name')


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('category_url')
    parent = CategorySlugRelatedField(
        many=False,
        read_only=False,
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )
    channel = ChannelSlugRelatedField(
        many=False,
        read_only=False,
        slug_field='slug',
        queryset=Channel.objects.all(),
        # source='channel.id',
    )

    def category_url(self, instance):
        request = self.context['request']
        return reverse(
            'category-detail', args=[instance.slug], request=request)

    class Meta:
        model = Category
        fields = ('url', 'slug', 'name', 'channel', 'parent')
