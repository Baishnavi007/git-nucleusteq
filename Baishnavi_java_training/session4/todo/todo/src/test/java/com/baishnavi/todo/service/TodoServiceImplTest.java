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

    // ------------------- TEST CASE 1 -------------------
    // Tests whether createTodo() correctly saves data and triggers notification
    @Test
    void testCreateTodo() {

        // ARRANGE
        TodoDTO dto = new TodoDTO();
        dto.setTitle("Test Task");

        Todo savedTodo = new Todo();
        savedTodo.setId(1L);
        savedTodo.setTitle("Test Task");
        savedTodo.setStatus(Todo.Status.PENDING);

        when(repository.save(any(Todo.class))).thenReturn(savedTodo);

        // ACT
        TodoDTO result = service.createTodo(dto);

        // ASSERT
        assertEquals("Test Task", result.getTitle());
        verify(repository, times(1)).save(any(Todo.class));
        verify(notificationServiceClient, times(1))
                .sendNotification(anyString());
    }

    // ------------------- TEST CASE 2 -------------------
    // Tests whether getTodoById() returns correct data when todo exists
    @Test
    void testGetTodoById() {

        // ARRANGE
        Todo todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Sample Task");

        // 🔥 FIX: status must be set (warna NPE aayega)
        todo.setStatus(Todo.Status.PENDING);

        when(repository.findById(1L)).thenReturn(java.util.Optional.of(todo));

        // ACT
        TodoDTO result = service.getTodoById(1L);

        // ASSERT
        assertEquals("Sample Task", result.getTitle());
    }
    // Tests whether deleteTodo() deletes data when ID exists
    @Test
    void testDeleteTodo() {

        // ------------------- ARRANGE -------------------
        // Mocking: ID exists in database
        when(repository.existsById(1L)).thenReturn(true);

        // ------------------- ACT -------------------
        // Calling delete method
        service.deleteTodo(1L);

        // ------------------- ASSERT -------------------
        // Verifying deleteById() was called once
        verify(repository, times(1)).deleteById(1L);
    }
}