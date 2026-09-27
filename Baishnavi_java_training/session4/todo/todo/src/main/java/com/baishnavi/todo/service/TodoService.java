package com.baishnavi.todo.service;

import com.baishnavi.todo.dto.TodoDTO;
import java.util.List;
//Made this interface for lose coupling and abstraction
// Defines operations for Todo management
public interface TodoService {

    TodoDTO createTodo(TodoDTO dto);

    List<TodoDTO> getAllTodos();

    TodoDTO getTodoById(Long id);

    TodoDTO updateTodo(Long id, TodoDTO dto);

    void deleteTodo(Long id);
}