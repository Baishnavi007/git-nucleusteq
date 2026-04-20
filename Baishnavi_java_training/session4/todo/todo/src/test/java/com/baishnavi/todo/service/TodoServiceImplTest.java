package com.baishnavi.todo.service;

import com.baishnavi.todo.dto.TodoDTO;
import com.baishnavi.todo.entity.Todo;
import com.baishnavi.todo.repository.TodoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.jupiter.api.Assertions.*;
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
    // Tests createTodo() success
    @Test
    void testCreateTodo() {

        TodoDTO dto = new TodoDTO();
        dto.setTitle("Test Task");

        Todo savedTodo = new Todo();
        savedTodo.setId(1L);
        savedTodo.setTitle("Test Task");
        savedTodo.setStatus(Todo.Status.PENDING);

        when(repository.save(any(Todo.class))).thenReturn(savedTodo);

        TodoDTO result = service.createTodo(dto);

        assertEquals("Test Task", result.getTitle());

        verify(repository, times(1)).save(any(Todo.class));
        verify(notificationServiceClient, times(1))
                .sendNotification(anyString());
    }

    // ------------------- TEST CASE 2 -------------------
    // Tests getTodoById() success
    @Test
    void testGetTodoById() {

        Todo todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Sample Task");
        todo.setStatus(Todo.Status.PENDING); // IMPORTANT

        when(repository.findById(1L)).thenReturn(java.util.Optional.of(todo));

        TodoDTO result = service.getTodoById(1L);

        assertEquals("Sample Task", result.getTitle());
    }

    // ------------------- TEST CASE 3 -------------------
    // Tests deleteTodo() success
    @Test
    void testDeleteTodo() {

        when(repository.existsById(1L)).thenReturn(true);

        service.deleteTodo(1L);

        verify(repository, times(1)).deleteById(1L);
    }

    // ------------------- TEST CASE 4 -------------------
    // Tests getTodoById() when not found
    @Test
    void testGetTodoByIdNotFound() {

        when(repository.findById(1L)).thenReturn(java.util.Optional.empty());

        assertThrows(RuntimeException.class, () -> {
            service.getTodoById(1L);
        });
    }

    // ------------------- TEST CASE 5 -------------------
    // Tests updateTodo() success
    @Test
    void testUpdateTodo() {

        Todo existing = new Todo();
        existing.setId(1L);
        existing.setTitle("Old");
        existing.setStatus(Todo.Status.PENDING);

        Todo updated = new Todo();
        updated.setId(1L);
        updated.setTitle("New");
        updated.setStatus(Todo.Status.COMPLETED);

        when(repository.findById(1L)).thenReturn(java.util.Optional.of(existing));
        when(repository.save(any(Todo.class))).thenReturn(updated);

        TodoDTO dto = new TodoDTO();
        dto.setTitle("New");
        dto.setStatus("COMPLETED");

        TodoDTO result = service.updateTodo(1L, dto);

        assertEquals("New", result.getTitle());
    }

    // ------------------- TEST CASE 6 -------------------
    // Tests deleteTodo() when ID not found
    @Test
    void testDeleteTodoNotFound() {

        when(repository.existsById(1L)).thenReturn(false);

        assertThrows(RuntimeException.class, () -> {
            service.deleteTodo(1L);
        });
    }
}