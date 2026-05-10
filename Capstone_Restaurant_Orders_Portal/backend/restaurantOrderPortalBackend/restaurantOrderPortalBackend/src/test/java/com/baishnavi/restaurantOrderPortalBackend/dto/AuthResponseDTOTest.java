package com.baishnavi.restaurantOrderPortalBackend.dto;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

class AuthResponseDTOTest {

    @Test
    void testNoArgsConstructorAndSetters() {
        AuthResponseDTO dto = new AuthResponseDTO();

        assertNull(dto.getToken());
        assertNull(dto.getRole());
        assertNull(dto.getEmail());

        dto.setToken("sample-jwt-token");
        dto.setRole("ADMIN");
        dto.setEmail("admin@restaurant.com");

        assertEquals("sample-jwt-token", dto.getToken());
        assertEquals("ADMIN", dto.getRole());
        assertEquals("admin@restaurant.com", dto.getEmail());
    }

    @Test
    void testAllArgsConstructorAndGetters() {
        AuthResponseDTO dto = new AuthResponseDTO("sample-jwt-token", "USER", "user@restaurant.com");

        assertEquals("sample-jwt-token", dto.getToken());
        assertEquals("USER", dto.getRole());
        assertEquals("user@restaurant.com", dto.getEmail());
    }
}