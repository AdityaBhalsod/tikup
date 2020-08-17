"""Utility functions for sound."""
from posts.models import Post


def profile_photo_url(sound_obj):
    """Get profile photo of owner."""
    if sound_obj.profile.display_pic:
        return sound_obj.profile.display_pic.url


def video_count(sound_obj):
    """Return number of videos made."""
    return Post.objects.filter(
        sound=sound_obj
    ).count()
