from rest_framework import serializers

from posts.utils import comments_count, likes_count, share_count

from sounds.api.serializers import SoundSerializer

from usermodule.api.serializers import ProfileSerializer

from posts.models import Post, PostCategory


class PostCategorySerializer(serializers.ModelSerializer):
    """Serializer for post category model."""

    class Meta:
        model = PostCategory
        fields = ('uuid', 'name', 'icon', 'description')


class PostSerializer(serializers.ModelSerializer):
    """Serializer for post model."""
    profile = ProfileSerializer()
    sound = SoundSerializer()
    category = PostCategory()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    shares = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return likes_count(obj)

    def get_comments(self, obj):
        return comments_count(obj)

    def get_shares(self, obj):
        return share_count(obj)

    class Meta:
        model = Post
        fields = (
            'uuid', 'profile', 'sound', 'video_file',
            'video_gif', 'description', 'category',
            'likes', 'shares', 'comments'
        )
