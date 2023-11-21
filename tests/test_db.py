import unittest
import sys
import os
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyweb_team7_project.database.db import get_db


class TestRstToHtml(unittest.TestCase):
    @patch("pyweb_team7_project.database.db.SessionLocal")
    def test_get_db(self, mock_session_local):
        # Arrange
        mock_session = MagicMock(spec=Session)
        mock_session_instance = mock_session()
        mock_session_instance.close.return_value = None
        mock_session_local.return_value = mock_session_instance

        # Act
        db = list(get_db())  # Преобразуем генератор в список

        # Assert
        self.assertEqual(len(db), 1)  # Проверяем, что список содержит один элемент
        self.assertIs(
            db[0], mock_session_instance
        )  # Проверяем, что элемент списка является mock_session_instance

        # Verify that the session was closed
        mock_session_instance.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
