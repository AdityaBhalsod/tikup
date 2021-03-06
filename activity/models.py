from django.db import models

from base.models import BaseModel

from posts.models import Post

from sounds.models import Sound

from usermodule.models import Profile


class Activity(BaseModel):
    """Model to record user interactions with applications."""

    FAVORITE = 'F'
    LIKE = 'L'
    REPORT = 'R'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (REPORT, 'Report')
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return '{} -> {}'.format(
            self.profile.user.get_full_name(),
            self.get_activity_type_display()
        )

    class Meta:
        unique_together = ('profile', 'post', 'activity_type',)


class Comment(BaseModel):
    """Store comments for posts."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_link', null=True, blank=True)
    comment = models.TextField()

    def __str__(self):
        return '{}: {}'.format(
            self.profile.user.get_full_name(),
            self.comment[:100]
        )


class CommentLike(BaseModel):
    """Store likes for every comment."""

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return '{} has liked {}'.format(
            self.profile.user.get_full_name(),
            self.comment.comment
        )

    class Meta:
        unique_together = ('profile', 'comment',)


class SoundView(BaseModel):
    """Record all views in sounds."""

    sound = models.ForeignKey(Sound, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return '{} has viewed {}'.format(
            self.profile.user.username,
            self.sound.name
        )

    class Meta:
        unique_together = ('profile', 'sound',)


class PostView(BaseModel):
    """Record all views in posts."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return '{} has viewed {}'.format(
            self.profile.user.username,
            self.post.description[:20]
        )

    class Meta:
        unique_together = ('profile', 'post',)
