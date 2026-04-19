package com.baishnavi.todo.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
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

    // NEW: Injecting external notification service
    private final NotificationServiceClient notificationServiceClient;

    // Logger for logging important events
    private static final Logger logger = LoggerFactory.getLogger(TodoServiceImpl.class);

    // Constructor Injection (updated to include NotificationServiceClient)
    public TodoServiceImpl(TodoRepository repository,
                           NotificationServiceClient notificationServiceClient) {
        this.repository = repository;
        this.notificationServiceClient = notificationServiceClient;
    }

    // Creates a new Todo
    @Override
    public TodoDTO createTodo(TodoDTO dto) {

        // Log creation request
        logger.info("Creating new Todo with title: {}", dto.getTitle());

        // Convert DTO to Entity
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

        // Log after successful creation
        logger.info("Todo created successfully with ID: {}", savedTodo.getId());

        // NEW: Simulating external service call (Notification sent shown )
        notificationServiceClient.sendNotification("Notification sent for new TODO");

        return mapToDTO(savedTodo);
    }


    // Fetch all Todos
    @Override
    public List<TodoDTO> getAllTodos() {
        logger.info("Fetching all Todos");

        return repository.findAll()
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    // Get Todo by ID
    @Override
    public TodoDTO getTodoById(Long id) {

        // Log before fetching
        logger.info("Fetching Todo with ID: {}", id);

        Todo todo = repository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Todo not found with id: " + id));

        return mapToDTO(todo);
    }

    // Update Todo
    @Override
    public TodoDTO updateTodo(Long id, TodoDTO dto) {

        logger.info("Updating Todo with ID: {}", id);

        Todo todo = repository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Todo not found with id: " + id));

        // Update basic fields
        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        // Update status if provided (validated)
        if (dto.getStatus() != null) {
            Todo.Status newStatus = parseStatus(dto.getStatus());

            // Validate status transition before updating
            validateStatusTransition(todo.getStatus(), newStatus);

            todo.setStatus(newStatus);
        }

        // Save updated entity
        Todo updatedTodo = repository.save(todo);

        logger.info("Todo updated successfully with ID: {}", id);

        return mapToDTO(updatedTodo);
    }

    // Delete Todo
    @Override
    public void deleteTodo(Long id) {

        if (!repository.existsById(id)) {
            throw new ResourceNotFoundException("Todo not found with id: " + id);
        }

        // Log before deletion
        logger.warn("Deleting Todo with ID: {}", id);

        repository.deleteById(id);

        // Log after deletion
        logger.info("Todo deleted successfully with ID: {}", id);
    }

    // Convert Entity to DTO
    private TodoDTO mapToDTO(Todo todo) {
        TodoDTO dto = new TodoDTO();
        dto.setTitle(todo.getTitle());
        dto.setDescription(todo.getDescription());
        dto.setStatus(todo.getStatus().name());
        return dto;
    }

    // Parse and validate status
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

    // Validate allowed transitions (future scalability)
    private void validateStatusTransition(Todo.Status current, Todo.Status newStatus) {

        if (current == newStatus) return;

        if ((current == Todo.Status.PENDING && newStatus == Todo.Status.COMPLETED) ||
                (current == Todo.Status.COMPLETED && newStatus == Todo.Status.PENDING)) {
            return;
        }

        throw new InvalidStatusTransitionException(
                "Invalid status transition from " + current + " to " + newStatus
        );
    }
}