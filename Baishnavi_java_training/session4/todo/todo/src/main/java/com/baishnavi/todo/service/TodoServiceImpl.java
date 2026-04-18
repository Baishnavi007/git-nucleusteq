package com.baishnavi.todo.service;

import com.baishnavi.todo.dto.TodoDTO;
import com.baishnavi.todo.entity.Todo;
import com.baishnavi.todo.exception.InvalidStatusException;
import com.baishnavi.todo.exception.InvalidStatusTransitionException;
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

    // Constructor Injection
    public TodoServiceImpl(TodoRepository repository) {
        this.repository = repository;
    }

    // Creates a new Todo
    @Override
    public TodoDTO createTodo(TodoDTO dto) {

        // Convert DTO → Entity
        Todo todo = new Todo();
        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        // Set default status or validate provided status
        if (dto.getStatus() == null) {
            todo.setStatus(Todo.Status.PENDING);
        } else {
            todo.setStatus(parseStatus(dto.getStatus()));
        }

        // Set system-generated timestamp
        todo.setCreatedAt(LocalDateTime.now());

        // Save to DB
        Todo savedTodo = repository.save(todo);

        // Return DTO
        return mapToDTO(savedTodo);
    }

    // Fetch all Todos
    @Override
    public List<TodoDTO> getAllTodos() {
        return repository.findAll()
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    // Get Todo by ID
    @Override
    public TodoDTO getTodoById(Long id) {
        Todo todo = repository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Todo not found with id: " + id));

        return mapToDTO(todo);
    }

    // Update Todo
    @Override
    public TodoDTO updateTodo(Long id, TodoDTO dto) {
        Todo todo = repository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Todo not found with id: " + id));

        // Update basic fields
        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        // Update status if provided (validated)
        if (dto.getStatus() != null) {
            Todo.Status newStatus = parseStatus(dto.getStatus());

            // Validate status transition before updating (for future scalability)
            validateStatusTransition(todo.getStatus(), newStatus);

            todo.setStatus(newStatus);
        }

        // Save updated entity
        Todo updatedTodo = repository.save(todo);

        return mapToDTO(updatedTodo);
    }

    // Delete Todo
    @Override
    public void deleteTodo(Long id) {
        if (!repository.existsById(id)) {
            throw new ResourceNotFoundException("Todo not found with id: " + id);
        }
        repository.deleteById(id);
    }

    // Convert Entity → DTO
    private TodoDTO mapToDTO(Todo todo) {
        TodoDTO dto = new TodoDTO();
        dto.setTitle(todo.getTitle());
        dto.setDescription(todo.getDescription());
        dto.setStatus(todo.getStatus().name());
        return dto;
    }

    // Parse and validate status with detailed error message
    private Todo.Status parseStatus(String status) {
        try {
            return Todo.Status.valueOf(status.toUpperCase());
        } catch (IllegalArgumentException e) {

            String allowedValues = String.join(", ",
                    java.util.Arrays.stream(Todo.Status.values())
                            .map(Enum::name)
                            .toList());

            throw new InvalidStatusException(
                    "Invalid status value: " + status +
                            ". Allowed values are: " + allowedValues
            );
        }
    }

    // Validates allowed status transitions
    // Currently allows toggling between PENDING and COMPLETED
    // Added for future scalability (in case more statuses are introduced)
    private void validateStatusTransition(Todo.Status current, Todo.Status newStatus) {

        if (current == newStatus) {
            return; // no change, allowed
        }

        // Allowed transitions: PENDING ↔ COMPLETED
        if ((current == Todo.Status.PENDING && newStatus == Todo.Status.COMPLETED) ||
                (current == Todo.Status.COMPLETED && newStatus == Todo.Status.PENDING)) {
            return;
        }

        throw new InvalidStatusTransitionException(
                "Invalid status transition from " + current + " to " + newStatus
        );
    }
}