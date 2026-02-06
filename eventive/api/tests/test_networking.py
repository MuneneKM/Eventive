# Copyright (c) 2024 Your Company Name
# License: MIT

import frappe
import unittest
from unittest.mock import patch, MagicMock


class TestNetworking(unittest.TestCase):
    """Unit tests for networking API functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock frappe.session.user
        self.mock_user = "testuser@example.com"
        
    def tearDown(self):
        """Clean up after tests."""
        frappe.local.session = None

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_get_matches_guest_user(self, mock_get_all, mock_session):
        """Test that guest users cannot access networking matches."""
        mock_session.user = "Guest"
        
        from eventive.api.networking import get_matches
        
        with self.assertRaises(frappe.PermissionError):
            get_matches()

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_get_matches_no_profile(self, mock_get_all, mock_session):
        """Test that users without a profile get empty results."""
        mock_session.user = "testuser@example.com"
        mock_get_all.return_value = []
        
        from eventive.api.networking import get_matches
        
        result = get_matches()
        self.assertEqual(result, [])

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_get_matches_not_open_to_networking(self, mock_get_all, mock_session):
        """Test that users not open to networking get empty results."""
        mock_session.user = "testuser@example.com"
        
        # First call returns user profile (not open to networking)
        mock_get_all.side_effect = [
            [{"name": "profile-123", "open_to_networking": 0}],  # User profile
        ]
        
        from eventive.api.networking import get_matches
        
        result = get_matches()
        self.assertEqual(result, [])

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_get_matches_returns_matches_for_open_user(self, mock_get_all, mock_session):
        """Test that users open to networking get their matches."""
        mock_session.user = "testuser@example.com"
        
        # Mock data
        mock_user_profile = {"name": "profile-123", "open_to_networking": 1}
        mock_match = {
            "name": "match-456",
            "attendee_1": "profile-123",
            "attendee_2": "profile-789",
            "event": "event-001",
            "match_score": 85.5,
            "status": "Suggested"
        }
        mock_other_profile = {
            "name": "profile-789",
            "user": "other@example.com",
            "full_name": "Other User",
            "company": "Test Corp",
            "job_title": "Developer",
            "bio": "A developer",
            "profile_image": "/files/photo.jpg",
            "social_link": "https://linkedin.com/in/other",
            "open_to_networking": 1
        }
        mock_interests = [
            {"interest": "Python"},
            {"interest": "Machine Learning"}
        ]
        
        mock_get_all.side_effect = [
            [mock_user_profile],  # User profile
            [mock_match],  # Match suggestions
            [mock_other_profile],  # Other attendee profile
            mock_interests  # Interests
        ]
        
        from eventive.api.networking import get_matches
        
        result = get_matches()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["match_id"], "match-456")
        self.assertEqual(result[0]["attendee_2"]["full_name"], "Other User")
        self.assertEqual(result[0]["attendee_2"]["interests"][0]["interest"], "Python")

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_get_matches_filters_by_event(self, mock_get_all, mock_session):
        """Test that matches can be filtered by event ID."""
        mock_session.user = "testuser@example.com"
        
        mock_user_profile = {"name": "profile-123", "open_to_networking": 1}
        
        mock_get_all.side_effect = [
            [mock_user_profile],  # User profile
            [],  # No matches for specific event
        ]
        
        from eventive.api.networking import get_matches
        
        result = get_matches(event_id="event-002")
        
        # Verify that the event filter was passed correctly
        call_args = mock_get_all.call_args_list
        self.assertEqual(call_args[1][1]["filters"]["event"], "event-002")

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_get_connected_matches(self, mock_get_all, mock_session):
        """Test that connected matches are returned correctly."""
        mock_session.user = "testuser@example.com"
        
        mock_user_profile = {"name": "profile-123", "open_to_networking": 1}
        mock_connected_match = {
            "name": "match-connected",
            "attendee_1": "profile-123",
            "attendee_2": "profile-connected",
            "event": "event-001",
            "match_score": 92.0,
            "status": "Connected",
            "modified": "2024-01-15 10:30:00"
        }
        mock_connected_profile = {
            "name": "profile-connected",
            "user": "connected@example.com",
            "full_name": "Connected User",
            "company": "Connected Corp",
            "job_title": "Manager",
            "bio": "A manager",
            "profile_image": "/files/manager.jpg",
            "social_link": "https://linkedin.com/in/connected",
            "open_to_networking": 1
        }
        mock_interests = [
            {"interest": "Networking"},
            {"interest": "Business"}
        ]
        
        mock_get_all.side_effect = [
            [mock_user_profile],  # User profile
            [mock_connected_match],  # Connected matches
            [mock_connected_profile],  # Connected attendee profile
            mock_interests  # Interests
        ]
        
        from eventive.api.networking import get_connected_matches
        
        result = get_connected_matches()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["match_id"], "match-connected")
        self.assertEqual(result[0]["status"], "Connected")
        self.assertIn("connected_on", result[0])


class TestSendMessage(unittest.TestCase):
    """Unit tests for send_message function."""

    @patch('frappe.session')
    @patch('frappe.get_all')
    @patch('frappe.get_value')
    def test_send_message_guest_user(self, mock_get_value, mock_get_all, mock_session):
        """Test that guest users cannot send messages."""
        mock_session.user = "Guest"
        
        from eventive.api.networking import send_message
        
        with self.assertRaises(frappe.PermissionError):
            send_message(receiver_id="other@example.com", event_id="event-001", message="Hello!")

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_send_message_missing_fields(self, mock_get_all, mock_session):
        """Test that missing required fields raise an error."""
        mock_session.user = "testuser@example.com"
        
        # No profile
        mock_get_all.return_value = []
        
        from eventive.api.networking import send_message
        
        with self.assertRaises(frappe.ValidationError):
            send_message(receiver_id=None, event_id=None, message="Hello!")

    @patch('frappe.session')
    @patch('frappe.get_all')
    @patch('frappe.get_doc')
    def test_send_message_success(self, mock_get_doc, mock_get_all, mock_session):
        """Test successful message sending."""
        mock_session.user = "testuser@example.com"
        
        mock_get_all.return_value = [{"name": "profile-123", "full_name": "Test User"}]
        mock_get_value.return_value = "Receiver Name"
        
        # Mock the created document
        mock_msg = MagicMock()
        mock_msg.name = "msg-001"
        mock_msg.creation = "2024-01-15 10:00:00"
        mock_get_doc.return_value = mock_msg
        
        from eventive.api.networking import send_message
        
        result = send_message(receiver_id="receiver@example.com", event_id="event-001", message="Hello, World!")
        
        self.assertEqual(result["message_id"], "msg-001")
        self.assertEqual(result["event_id"], "event-001")
        self.assertEqual(result["message"], "Hello, World!")


class TestGetMessages(unittest.TestCase):
    """Unit tests for get_messages function."""

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_get_messages_guest_user(self, mock_get_all, mock_session):
        """Test that guest users cannot view messages."""
        mock_session.user = "Guest"
        
        from eventive.api.networking import get_messages
        
        with self.assertRaises(frappe.PermissionError):
            get_messages(other_user_id="other@example.com", event_id="event-001")

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_get_messages_missing_fields(self, mock_get_all, mock_session):
        """Test that missing required fields raise an error."""
        mock_session.user = "testuser@example.com"
        
        from eventive.api.networking import get_messages
        
        with self.assertRaises(frappe.ValidationError):
            get_messages(other_user_id=None, event_id=None)

    @patch('frappe.session')
    @patch('frappe.get_all')
    def test_get_messages_returns_conversation(self, mock_get_all, mock_session):
        """Test that messages between two users are returned."""
        mock_session.user = "testuser@example.com"
        
        mock_messages = [
            {
                "event": "event-001",
                "name": "msg-001",
                "sender": "testuser@example.com",
                "receiver": "other@example.com",
                "sender_name": "Test User",
                "receiver_name": "Other User",
                "message": "Hello!",
                "is_read": 1,
                "creation": "2024-01-15T10:00:00Z"
            },
            {
                "event": "event-001",
                "name": "msg-002",
                "sender": "other@example.com",
                "receiver": "testuser@example.com",
                "sender_name": "Other User",
                "receiver_name": "Test User",
                "message": "Hi there!",
                "is_read": 0,
                "creation": "2024-01-15T10:35:00Z"
            }
        ]
        
        mock_get_all.return_value = mock_messages
        
        from eventive.api.networking import get_messages
        
        result = get_messages(other_user_id="other@example.com", event_id="event-001")
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "msg-001")
        self.assertEqual(result[0]["event_id"], "event-001")
        self.assertEqual(result[0]["message"], "Hello!")
        self.assertEqual(result[1]["message"], "Hi there!")
        self.assertEqual(result[0]["is_read"], True)
        self.assertEqual(result[1]["is_read"], False)


if __name__ == "__main__":
    unittest.main()
