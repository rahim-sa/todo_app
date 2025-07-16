def test_full_workflow(empty_model, sample_todo):
    # Add
    empty_model.todos["1"] = sample_todo
    assert "1" in empty_model.todos
    
    # Complete
    empty_model.todos["1"].is_complete = True
    assert empty_model.todos["1"].is_complete
    
    # Delete
    del empty_model.todos["1"]
    assert "1" not in empty_model.todos