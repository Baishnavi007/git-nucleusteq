package com.baishnavi.restaurantOrderPortalBackend.dto;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class UserDTOTest {

    @Test
    void testGettersAndSetters() {
        UserDTO dto = new UserDTO();
        dto.setId(1L);
        dto.setFirstName("Alice");
        dto.setEmail("alice@example.com");
        dto.setRole("USER");
        dto.setWalletBalance(1000.0);

        assertEquals(1L, dto.getId());
        assertEquals("Alice", dto.getFirstName());
        assertEquals("alice@example.com", dto.getEmail());
        assertEquals("USER", dto.getRole());
        assertEquals(1000.0, dto.getWalletBalance());
    }

    @Test
    void testAllArgsConstructor() {
        UserDTO dto = new UserDTO(2L, "Bob", "bob@example.com", "OWNER", 500.0);

        assertEquals(2L, dto.getId());
        assertEquals("Bob", dto.getFirstName());
        assertEquals("bob@example.com", dto.getEmail());
        assertEquals("OWNER", dto.getRole());
        assertEquals(500.0, dto.getWalletBalance());
    }
}