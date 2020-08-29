"""API views for favorites."""
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from favorites.api.serializers import *
from favorites.controller.favourite import FavoriteCentral, MarkFavorite


class FavoriteView(APIView):
    """Handle all favorite functions."""

    def post(self, request, model_marker, object_id):
        """Mark or unmark a favorite post or sound."""
        is_favorite_marked = MarkFavorite().mark(
            request.user.profile,
            model_marker,
            object_id
        )
        if is_favorite_marked:
            message = 'Successfully done.'
        else:
            message = 'Unusual Problem was faced.'
        return Response(
            data={'message': message},
            status=status.HTTP_200_OK
        )

    def get(self, request, model_marker):
        """Get all favorites for an user."""
        page_number = request.query_params.get('page_number ', 1)
        page_size = request.query_params.get('page_size ', 100)
        instances = FavoriteCentral().show(
            request.user.profile,
            model_marker
        )
        if not instances:
            raise Exception('There are no favorites for you to see.')
        paginator = Paginator(instances, page_size)
        serializer = None
        if model_marker.lower() == 'post':
            serializer = FavoritePostSerializer(
                paginator.page(page_number),
                many=True,
                context={'request': request}
            )
        if model_marker.lower() == 'sound':
            serializer = FavoriteSoundSerializer(
                paginator.page(page_number),
                many=True,
                context={'request': request}
            )
        if not serializer:
            raise Exception('Please pass proper Model marker for favorites retrieval.')
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )