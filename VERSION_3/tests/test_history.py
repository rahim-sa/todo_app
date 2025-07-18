import pytest
from datetime import datetime
from unittest.mock import MagicMock
from src.models.history import History, HistoryEntry

def test_history_entry_creation():
    """Test basic history entry creation"""
    timestamp = datetime.now()
    entry = HistoryEntry(
        action="CREATE",
        todo_id="1",
        timestamp=timestamp
    )
    
    assert entry.action == "CREATE"
    assert entry.todo_id == "1"
    assert entry.timestamp == timestamp

def test_history_add_entry():
    """Test adding entries to history"""
    history = History()
    history.add_entry("UPDATE", "2")
    
    assert len(history.entries) == 1
    assert history.entries[0].action == "UPDATE"
    assert history.entries[0].todo_id == "2"

def test_history_undo_operations():
    """Test undo stack functionality"""
    history = History()
    mock_action = MagicMock()
    
    # Test push
    history.push_undo(mock_action)
    assert len(history._undo_stack) == 1
    
    # Test pop
    action = history.pop_undo()
    action.assert_not_called()  # Just verify we got our mock back
    assert len(history._undo_stack) == 0

def test_history_clear():
    """Test clearing history"""
    history = History()
    history.add_entry("DELETE", "3")
    history.push_undo(lambda: None)
    
    history.clear()
    
    assert len(history.entries) == 0
    assert len(history._undo_stack) == 0

def test_history_empty_undo():
    """Test popping from empty undo stack"""
    history = History()
    assert history.pop_undo() is None