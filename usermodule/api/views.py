from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from usermodule.api.serializers import ProfileSerializer
from usermodule.models import FollowerMap
from usermodule.models import Profile


@api_view(['POST'])
def create_auth(request):
    """
    Create user for Misco.

    request.POST['email']: str
    request.POST['username']: str
    request.POST['password']: password (plain string -> hashing in backend)
    """
    serialized = request.POST
    try:
        user_obj = User.objects.create_user(
            email=serialized['email'],
            username=serialized['username'],
            password=serialized['password']
        )
        Profile.objects.create(user=user_obj)
        return Response({'message': 'User Created !'}, status=status.HTTP_201_CREATED)
    except BaseException as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FollowerRequestView(APIView):
    """Allows one user to follow/unfollow other user."""

    def get(self, request, follow_tag):
        """
        Get list of followers or following.

        Available tag:
        1. follower
        2. following
        """
        if follow_tag.lower() == 'follower':
            uuid_list = FollowerMap.objects.filter(
                following=request.user.profile
            ).values_list(
                'follower__uuid', flat=True
            )
        elif follow_tag.lower() == 'following':
            uuid_list = FollowerMap.objects.filter(
                follower=request.user.profile
            ).values_list(
                'following__uuid', flat=True
            )
        else:
            raise Exception('Proper Tag was not passed.')
        profiles = Profile.objects.filter(
            uuid__in=uuid_list
        )
        serialized = ProfileSerializer(
            profiles,
            many=True
        )
        return Response(
            data=serialized.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, follow_profile_username):
        """Follow an user."""
        following_profile = Profile.objects.get(
            user__username=follow_profile_username
        )
        try:
            FollowerMap.objects.create(
                follower=request.user.profile,
                following=following_profile
            )
            return Response(
                {
                    'message': 'You have followed {}'.format(following_profile.user.get_full_name())
                },
                status=status.HTTP_200_OK
            )
        except BaseException as e:
            FollowerMap.objects.filter(
                follower=request.user.profile,
                following=following_profile
            ).delete()
            return Response(
                {
                    'message': 'You have unfollowed {}'.format(following_profile.user.get_full_name())
                },
                status=status.HTTP_200_OK
            )

