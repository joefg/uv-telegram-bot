from unittest.mock import patch, Mock

import app.models.user as user_model

def test_get_user():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
       
        # GIVEN that we want a specific user
        # THEN we get that user
        mock_cursor.fetchone.return_value = \
            user_model.User(0, 0, 'Test', 'User', 0, 0, None)
        result = user_model.get_user(0)
        assert result == \
            user_model.User(0, 0, 'Test', 'User', 0, 0, None)

        # GIVEN that the user we want doesn't exist
        # THEN we don't get a user
        mock_cursor.fetchone.return_value = None
        result = user_model.get_user(999)
        assert result == None
