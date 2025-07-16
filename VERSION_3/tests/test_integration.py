def test_full_workflow(empty_model, sample_todo):
    """Test complete CRUD workflow"""
    # Create
    empty_model.todos["1"] = sample_todo
    assert "1" in empty_model.todos
    
    # Read
    todo = empty_model.todos["1"]
    assert todo.title == "Test Todo"
    
    # Update (complete)
    todo.is_complete = True
    assert todo.is_complete
    
    # Delete
    del empty_model.todos["1"]
    assert "1" not in empty_model.todos