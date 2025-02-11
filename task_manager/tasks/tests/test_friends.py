import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from tasks.models import Friendship
from django.test import Client

@pytest.mark.django_db
class TestFriendship:
    @pytest.fixture
    def setup_users(self):
        user1 = User.objects.create_user(username="user1", password="password1")
        user2 = User.objects.create_user(username="user2", password="password2")
        return user1, user2

    def test_send_friend_request(self, setup_users):
        """Test sending a friend request"""
        user1, user2 = setup_users
        friendship = Friendship.objects.create(user=user1, friend=user2)

        assert friendship.user == user1
        assert friendship.friend == user2
        assert not friendship.accepted  # Domyślnie oczekuje na akceptację

    def test_accept_friend_request(self, setup_users):
        """Test accepting a friend request"""
        user1, user2 = setup_users
        friendship = Friendship.objects.create(user=user1, friend=user2)
        friendship.accepted = True
        friendship.save()

        assert friendship.accepted is True

    def test_cannot_add_self_as_friend(self, setup_users):
        """Test that a user cannot add themselves as a friend"""
        user1, _ = setup_users

        with pytest.raises(ValidationError, match="You cannot add yourself as a friend."):
            friendship = Friendship(user=user1, friend=user1)
            friendship.full_clean()  # Wywołanie walidacji ręcznie
            friendship.save()  # Nie powinno dojść do tego kroku

    def test_remove_friend(self, setup_users):
        """Test removing a friend"""
        user1, user2 = setup_users
        friendship = Friendship.objects.create(user=user1, friend=user2, accepted=True)

        friendship.delete()

        assert not Friendship.objects.filter(user=user1, friend=user2).exists()

    def test_friend_request_view(self, setup_users):
        """Test sending a friend request via the view"""
        user1, user2 = setup_users
        client = Client()
        client.force_login(user1)

        response = client.post(reverse("add_friend"), {"friend_username": user2.username})

        assert response.status_code == 302  # Przekierowanie po wysłaniu zaproszenia
        assert Friendship.objects.filter(user=user1, friend=user2).exists()
