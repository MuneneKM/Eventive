# Copyright (c) 2024 Your Company Name
# License: MIT

import frappe
import unittest
from unittest.mock import patch, MagicMock


class TestUpdateProfile(unittest.TestCase):
    """Unit tests for update_profile function."""

    @patch('frappe.get_doc')
    def test_update_profile_updates_fields(self, mock_get_doc):
        """Test that update_profile correctly updates profile fields."""
        # Mock the profile document
        mock_profile = MagicMock()
        mock_profile.name = "profile-123"
        mock_profile.open_to_networking = 0
        mock_profile.social_link = None
        mock_profile.interests = []
        mock_get_doc.return_value = mock_profile
        
        from eventive.api.auth import update_profile
        
        result = update_profile(
            profile_id="profile-123",
            interests=["Python", "Machine Learning"],
            open_to_networking=True,
            social_link="https://linkedin.com/in/user"
        )
        
        # Verify the profile was saved
        mock_profile.save.assert_called_once()
        
        # Verify interests were added
        self.assertEqual(len(mock_profile.interests), 2)

    @patch('frappe.get_doc')
    def test_update_profile_with_string_interests(self, mock_get_doc):
        """Test that update_profile handles string interests correctly."""
        mock_profile = MagicMock()
        mock_profile.name = "profile-123"
        mock_profile.open_to_networking = 0
        mock_profile.social_link = None
        mock_profile.interests = []
        mock_get_doc.return_value = mock_profile
        
        from eventive.api.auth import update_profile
        
        # Pass interests as a JSON string
        result = update_profile(
            profile_id="profile-123",
            interests='["Python", "AI"]',
            open_to_networking=True
        )
        
        # Verify interests were parsed and added
        self.assertEqual(len(mock_profile.interests), 2)

    @patch('frappe.get_doc')
    def test_update_profile_without_interests(self, mock_get_doc):
        """Test that update_profile works without changing interests."""
        mock_profile = MagicMock()
        mock_profile.name = "profile-123"
        mock_profile.open_to_networking = 1
        mock_profile.social_link = "https://twitter.com/user"
        mock_profile.interests = []
        mock_get_doc.return_value = mock_profile
        
        from eventive.api.auth import update_profile
        
        result = update_profile(
            profile_id="profile-123",
            interests=None,
            open_to_networking=False,
            social_link=None
        )
        
        # Verify interests were not cleared when None
        mock_profile.save.assert_called_once()


if __name__ == "__main__":
    unittest.main()
