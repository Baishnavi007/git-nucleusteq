package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.dto.AuthRequestDTO;
import com.baishnavi.restaurantOrderPortalBackend.dto.RegisterRequestDTO;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.enums.Role;
import com.baishnavi.restaurantOrderPortalBackend.security.JwtUtil;
import com.baishnavi.restaurantOrderPortalBackend.service.UserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AuthController.class)
@AutoConfigureMockMvc(addFilters = false)
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private UserService userService;

    @MockitoBean
    private JwtUtil jwtUtil;

    @Autowired
    private ObjectMapper objectMapper;

    private User user;

    @BeforeEach
    void setUp() {
        user = new User();
        user.setId(1L);
        user.setFirstName("John");
        user.setLastName("Doe");
        user.setEmail("test@example.com");
        user.setPassword("password");
        user.setRole(Role.USER);
    }

    @Test
    void register() throws Exception {
        RegisterRequestDTO request = new RegisterRequestDTO("John", "Doe", "1234567890", "test@example.com", "password", "USER");
        when(userService.registerUser(any(User.class))).thenReturn(user);

        mockMvc.perform(post("/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk());
    }

    @Test
    void login() throws Exception {
        AuthRequestDTO request = new AuthRequestDTO("test@example.com", "password");
        when(userService.validateUser("test@example.com", "password")).thenReturn(user);
        when(userService.generateToken(user)).thenReturn("mock-token");

        mockMvc.perform(post("/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.token").value("mock-token"))
                .andExpect(jsonPath("$.email").value("test@example.com"));
    }
}