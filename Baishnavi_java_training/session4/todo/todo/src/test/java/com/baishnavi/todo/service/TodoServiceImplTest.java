package com.baishnavi.todo.service;

import com.baishnavi.todo.dto.TodoDTO;
import com.baishnavi.todo.entity.Todo;
import com.baishnavi.todo.repository.TodoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

// This class is used to test TodoServiceImpl methods
public class TodoServiceImplTest {

    // Fake repository (real DB call is not happening)
    @Mock
    private TodoRepository repository;

    // Mock external service
    @Mock
    private NotificationServiceClient notificationServiceClient;

    // Actual service which is being tested (with injected mocks)
    @InjectMocks
    private TodoServiceImpl service;

    // Setup method: runs before each test
    @BeforeEach
    void setup() {
        MockitoAnnotations.openMocks(this);
    }

    // ------------------- TEST CASE -------------------

    // Tests whether createTodo() correctly saves data and triggers notification
    @Test
    void testCreateTodo() {

        // ------------------- ARRANGE -------------------
        // Creating input DTO (simulating user request)
        TodoDTO dto = new TodoDTO();
        dto.setTitle("Test Task");


        // Creating fake saved entity (simulating DB response)
        Todo savedTodo = new Todo();
        savedTodo.setId(1L);
        savedTodo.setTitle("Test Task");
        savedTodo.setStatus(Todo.Status.PENDING);

        // Mocking repository behavior: When save() is called just return savedTodo
        when(repository.save(any(Todo.class))).thenReturn(savedTodo);

        // ------------------- ACT -------------------
        // Calling actual service method
        TodoDTO result = service.createTodo(dto);

        // ------------------- ASSERT -------------------
        // Checking if returned result is correct
        assertEquals("Test Task", result.getTitle());

        // Verifying repository.save() was called exactly once
        verify(repository, times(1)).save(any(Todo.class));

        // Verifying notification service was called
        verify(notificationServiceClient, times(1))
                .sendNotification(anyString());
    }
}