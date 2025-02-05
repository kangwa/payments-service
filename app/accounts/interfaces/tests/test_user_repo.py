"""Test suite for UserRepository interface."""

from datetime import datetime
from uuid import uuid4

import pytest

from app.accounts.entities.user import User, UserStatus
from app.common.value_objects.email import Email

from .mock_repositories import MockUserRepository


@pytest.fixture
def user_repo():
    """Fixture providing a mock user repository."""
    return MockUserRepository()


@pytest.fixture
def sample_user():
    """Fixture providing a sample user entity."""
    return User(
        email=Email("test@example.com"),
        organization_id=uuid4(),
        hashed_password="hashed_secret",
        name="Test User",
    )


class TestUserRepository:
    """Test cases for UserRepository interface."""

    def test_save_and_get_by_id(self, user_repo, sample_user):
        """Test saving and retrieving a user."""
        # Save user
        saved = user_repo.save(sample_user)
        assert saved.id == sample_user.id

        # Retrieve user
        retrieved = user_repo.get_by_id(sample_user.id)
        assert retrieved is not None
        assert retrieved.id == sample_user.id
        assert retrieved.email == sample_user.email
        assert retrieved.name == sample_user.name

    def test_get_by_email(self, user_repo, sample_user):
        """Test retrieving a user by email."""
        # Save user
        user_repo.save(sample_user)

        # Retrieve by email
        retrieved = user_repo.get_by_email(sample_user.email)
        assert retrieved is not None
        assert retrieved.id == sample_user.id

        # Test non-existent email
        nonexistent = user_repo.get_by_email(Email("nonexistent@example.com"))
        assert nonexistent is None

    def test_update_login_time(self, user_repo, sample_user):
        """Test updating user's last login time."""
        # Save user
        user_repo.save(sample_user)
        assert sample_user.last_login is None

        # Update login time
        before_update = datetime.now()
        user_repo.update_login_time(sample_user.id)

        # Verify update
        updated = user_repo.get_by_id(sample_user.id)
        assert updated.last_login is not None
        assert updated.last_login >= before_update

        # Test updating non-existent user
        with pytest.raises(ValueError):
            user_repo.update_login_time(uuid4())

    def test_list_pagination(self, user_repo):
        """Test user listing with pagination."""
        # Create test users
        users = [
            User(
                email=Email(f"user{i}@example.com"),
                organization_id=uuid4(),
                hashed_password="hashed_secret",
                name=f"User {i}",
            )
            for i in range(5)
        ]
        for user in users:
            user_repo.save(user)

        # Test pagination
        page_1 = user_repo.list(limit=2, offset=0)
        assert len(page_1) == 2

        page_2 = user_repo.list(limit=2, offset=2)
        assert len(page_2) == 2

        page_3 = user_repo.list(limit=2, offset=4)
        assert len(page_3) == 1

    def test_delete(self, user_repo, sample_user):
        """Test user deletion."""
        # Save and then delete
        user_repo.save(sample_user)
        user_repo.delete(sample_user.id)

        # Verify deletion
        assert user_repo.get_by_id(sample_user.id) is None

        # Verify delete of non-existent user raises error
        with pytest.raises(ValueError):
            user_repo.delete(uuid4())

    def test_status_persistence(self, user_repo, sample_user):
        """Test persistence of user status changes."""
        # Save initial state
        user_repo.save(sample_user)
        assert sample_user.status == UserStatus.ACTIVE

        # Modify and save
        retrieved = user_repo.get_by_id(sample_user.id)
        retrieved.deactivate()
        user_repo.save(retrieved)

        # Verify status change persisted
        updated = user_repo.get_by_id(sample_user.id)
        assert updated.status == UserStatus.INACTIVE
