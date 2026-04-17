package com.baishnavi.todo.service;

import com.baishnavi.todo.dto.TodoDTO;
import com.baishnavi.todo.entity.Todo;
import com.baishnavi.todo.exception.InvalidStatusException;
import com.baishnavi.todo.exception.ResourceNotFoundException;
import com.baishnavi.todo.repository.TodoRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

// Handles business logic for Todo operations
@Service
public class TodoServiceImpl implements TodoService {

    private final TodoRepository repository;

    // Constructor Injection (Spring injects repository automatically)
    public TodoServiceImpl(TodoRepository repository) {
        this.repository = repository;
    }

    // Creates a new Todo by converting DTO to Entity, setting default values, and saving to DB
    @Override
    public TodoDTO createTodo(TodoDTO dto) {

        // Convert DTO → Entity
        Todo todo = new Todo();
        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        // Set default status if not provided, else validate and set
        if (dto.getStatus() == null) {
            todo.setStatus(Todo.Status.PENDING);
        } else {
            todo.setStatus(parseStatus(dto.getStatus()));
        }

        // Set system-generated timestamp
        todo.setCreatedAt(LocalDateTime.now());

        // Save entity to database
        Todo savedTodo = repository.save(todo);

        // Convert saved entity back to DTO and return
        return mapToDTO(savedTodo);
    }

    // Fetches all Todos from DB and converts them to DTO list
    @Override
    public List<TodoDTO> getAllTodos() {
        return repository.findAll()
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    // Retrieves a Todo by ID, throws exception if not found
    @Override
    public TodoDTO getTodoById(Long id) {
        Todo todo = repository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Todo not found with id: " + id));

        return mapToDTO(todo);
    }

    // Updates an existing Todo with new values from DTO
    @Override
    public TodoDTO updateTodo(Long id, TodoDTO dto) {
        Todo todo = repository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Todo not found with id: " + id));

        // Update fields
        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        // Update status only if provided (with validation)
        if (dto.getStatus() != null) {
            todo.setStatus(parseStatus(dto.getStatus()));
        }

        // Save updated entity
        Todo updatedTodo = repository.save(todo);

        return mapToDTO(updatedTodo);
    }

    // Deletes a Todo by ID after checking existence
    @Override
    public void deleteTodo(Long id) {
        if (!repository.existsById(id)) {
            throw new ResourceNotFoundException("Todo not found with id: " + id);
        }
        repository.deleteById(id);
    }

    // Converts Entity to DTO (manual mapping as required)
    private TodoDTO mapToDTO(Todo todo) {
        TodoDTO dto = new TodoDTO();
        dto.setTitle(todo.getTitle());
        dto.setDescription(todo.getDescription());
        dto.setStatus(todo.getStatus().name());
        return dto;
    }

    // Parses and validates status string into Enum, throws custom exception if invalid
    private Todo.Status parseStatus(String status) {
        try {
            return Todo.Status.valueOf(status.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new InvalidStatusException("Invalid status value: " + status);
        }
    }
}