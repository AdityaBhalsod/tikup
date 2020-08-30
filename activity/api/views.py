"""API views for activity app."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.api.serializers import NestedCommentSerializer
from activity.models import Activity, Comment

from posts.models import Post


class PostReplyView(APIView):
    """Reply on a particular comment of a post."""

    def post(self, request, comment_id):
        """Reply on a comment."""
        try:
            comment = Comment.objects.get(uuid=comment_id)
            Comment.objects.create(
                comment=request.POST['comment'],
                reply=comment,
                profile=request.user.profile,
            )
            return Response(
                data={'mesaage': 'Reply has been created !'},
                status=status.HTTP_201_CREATED
            )
        except BaseException as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostCommentView(APIView):
    """Comment view for every post."""

    permission_classes = (IsAuthenticated, )

    def get(self, request, post_id):
        """Get paginated comment for a single post."""
        comments = Comment.objects.filter(
            post__uuid=post_id
        )
        serialized_comments = NestedCommentSerializer(
            comments,
            many=True
        ).data
        return Response(
            data=serialized_comments,
            status=status.HTTP_200_OK
        )

    def post(self, request, post_id):
        """
        Add comment to a post.

        request.POST['comment'] : str
            eg: 'The post is very nice.'
        """
        try:
            Comment.objects.create(
                comment=request.POST['comment'],
                post=Post.objects.get(uuid=post_id),
                profile=request.user.profile,
            )
            return Response(
                data={'message': 'Comment Added !'},
                status=status.HTTP_201_CREATED
            )
        except BaseException as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostLikeView(APIView):
    """Like or unlike post depending on user."""

    def post(self, request, post_id):
        """Like or unlike the post."""
        profile = request.user.profile
        try:
            like_record = Activity.objects.filter(
                profile=profile,
                activity_type='L',
                post__uuid=post_id
            )
            if like_record.exists():
                like_record.delete()
                return Response(
                    data={'mesaage': 'Post has been unliked !'},
                    status=status.HTTP_201_CREATED
                )
            Activity.objects.create(
                profile=profile,
                activity_type='L',
                post_uuid=post_id
            )
            return Response(
                data={'mesaage': 'Post has been liked !'},
                status=status.HTTP_201_CREATED
            )
        except BaseException as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostReportView(APIView):
    """Report or un-report post depending on user."""

    def post(self, request, post_id):
        """Report or un-report the post."""
        profile = request.user.profile
        try:
            report_record = Activity.objects.filter(
                profile=profile,
                activity_type='R',
                post_uuid=post_id
            )
            if report_record.exists():
                report_record.delete()
                return Response(
                    data={'mesaage': 'Post has been un-reported !'},
                    status=status.HTTP_201_CREATED
                )
            Activity.objects.create(
                profile=profile,
                activity_type='R',
                post_uuid=post_id
            )
            return Response(
                data={'mesaage': 'Post has been reported !'},
                status=status.HTTP_201_CREATED
            )
        except BaseException as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
