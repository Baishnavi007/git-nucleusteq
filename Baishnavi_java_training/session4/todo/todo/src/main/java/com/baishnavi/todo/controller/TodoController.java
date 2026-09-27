package com.baishnavi.todo.controller;

import com.baishnavi.todo.dto.TodoDTO;
import com.baishnavi.todo.service.TodoService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// REST Controller to handle Todo APIs
@RestController
@RequestMapping("/todos")
public class TodoController {

    private final TodoService service;

    // Logger for API-level logging
    private static final Logger logger = LoggerFactory.getLogger(TodoController.class);

    // Constructor Injection
    public TodoController(TodoService service) {
        this.service = service;
    }

    // Creates a new Todo using request body data
    @PostMapping
    public TodoDTO createTodo(@Valid @RequestBody TodoDTO dto) {

        logger.info("API call: Create Todo");

        return service.createTodo(dto);
    }

    // Fetches all Todos
    @GetMapping
    public List<TodoDTO> getAllTodos() {

        logger.info("API call: Get all Todos");

        return service.getAllTodos();
    }

    // Fetches a Todo by its ID
    @GetMapping("/{id}")
    public TodoDTO getTodoById(@PathVariable Long id) {

        logger.info("API call: Get Todo by ID: {}", id);

        return service.getTodoById(id);
    }

    // Updates an existing Todo
    @PutMapping("/{id}")
    public TodoDTO updateTodo(@PathVariable Long id,
                              @RequestBody TodoDTO dto) {

        logger.info("API call: Update Todo with ID: {}", id);

        return service.updateTodo(id, dto);
    }

    // Deletes a Todo by ID
    @DeleteMapping("/{id}")
    public void deleteTodo(@PathVariable Long id) {

        logger.warn("API call: Delete Todo with ID: {}", id);

        service.deleteTodo(id);
    }
}