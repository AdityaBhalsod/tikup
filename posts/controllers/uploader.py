from posts.models import Post

from tag.controllers.tag_central import TagCentral


class PostUploader:
    """Handle sound upload."""

    @staticmethod
    def upload(user, file, details):
        """Upload a post in model."""
        try:
            post = Post.objects.create(
                profile=user.profile,
                video_file=file['video_file'],
                video_gif=file['video_gif'],
                description=details.get('description', None),
                sound__uuid=details.get('sound_uuid', None),
                share_pointer__uuid=details.get('share_post_uuid', None),
                category__name=details.get('category', None),
                is_pornographic=details.get('is_pornographic', False)
            )
            TagCentral().handle_tag_cycle(post)
            return {'message': 'Succesfully Uploaded'}
        except BaseException as e:
            return {'message': 'Error Occured: {}'.format(e)}
