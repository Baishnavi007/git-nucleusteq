package com.baishnavi.todo.controller;

import com.baishnavi.todo.dto.TodoDTO;
import com.baishnavi.todo.service.TodoService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// REST Controller to handle Todo APIs
@RestController
@RequestMapping("/todos")
public class TodoController {

    private final TodoService service;

    // Constructor Injection
    public TodoController(TodoService service) {
        this.service = service;
    }

    // Creates a new Todo using request body data
    @PostMapping
    public TodoDTO createTodo(@Valid @RequestBody TodoDTO dto) {
        return service.createTodo(dto);
    }

    // Fetches all Todos
    @GetMapping
    public List<TodoDTO> getAllTodos() {
        return service.getAllTodos();
    }

    // Fetches a Todo by its ID
    @GetMapping("/{id}")
    public TodoDTO getTodoById(@PathVariable Long id) {
        return service.getTodoById(id);
    }


    // Updates an existing Todo
    @PutMapping("/{id}")
    public TodoDTO updateTodo(@PathVariable Long id,
                              @RequestBody TodoDTO dto) {
        return service.updateTodo(id, dto);
    }


    // Deletes a Todo by ID
    @DeleteMapping("/{id}")
    public void deleteTodo(@PathVariable Long id) {
        service.deleteTodo(id);
    }
}