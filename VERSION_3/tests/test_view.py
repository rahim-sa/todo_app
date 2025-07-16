from unittest.mock import patch
import pytest

class TestTodoView:
    @patch('builtins.input', side_effect=['Test', '', '2023-12-31'])