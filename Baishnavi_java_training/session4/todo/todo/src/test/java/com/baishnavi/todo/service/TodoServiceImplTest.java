package com.baishnavi.todo.service;

import com.baishnavi.todo.repository.TodoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

// This class is used to test TodoServiceImpl methods
public class TodoServiceImplTest {

    // Fake repository (real DB call is not happening)
    @Mock
    private TodoRepository repository;

    // Mock external service
    @Mock
    private NotificationServiceClient notificationServiceClient;

    // Actual service which is being tested(With injected mocks)
    @InjectMocks
    private TodoServiceImpl service;

    // Setup method: runs before each test
    @BeforeEach
    void setup() {
        MockitoAnnotations.openMocks(this);
    }
}