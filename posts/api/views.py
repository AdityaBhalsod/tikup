from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.api.serializers import PostSerializer
from posts.controllers.uploader import PostUploader
from posts.exceptions import PostUploadException
from posts.models import Post


class PostUploadView(APIView):
    """Handle post basic functions."""

    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """Upload post to model."""
        if not request.FILES:
            raise PostUploadException('No Video file supplied.')
        return Response(
            data=PostUploader().upload(
                request.user,
                request.FILES,
                request.POST
            ),
            status=status.HTTP_201_CREATED
        )


class PostSearchAPI(APIView):
    """Search posts."""

    def get(self, request, *args, **kwargs):
        """Get paginated search results."""
        page_number = request.query_params.get('page_number ', 1)
        page_size = request.query_params.get('page_size ', 50)
        search_token = request.query_params.get('search', None)
        if not search_token:
            raise Exception('Search Token not provided.')
        posts = Post.objects.filter(
            description__icontains=search_token
        )
        paginator = Paginator(posts, page_size)
        serializer = PostSerializer(
            paginator.page(page_number),
            many=True,
            context={'request': request}
        )
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

