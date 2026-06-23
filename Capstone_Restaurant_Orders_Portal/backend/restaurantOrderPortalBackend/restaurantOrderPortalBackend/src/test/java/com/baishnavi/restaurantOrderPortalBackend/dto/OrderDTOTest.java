package com.baishnavi.restaurantOrderPortalBackend.dto;

import org.junit.jupiter.api.Test;
import java.time.LocalDateTime;
import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class OrderDTOTest {

    @Test
    void testGettersAndSetters() {
        OrderDTO dto = new OrderDTO();
        LocalDateTime now = LocalDateTime.now();

        dto.setId(1L);
        dto.setTotalAmount(1500.0);
        dto.setStatus("PLACED");
        dto.setCreatedAt(now);
        dto.setItems(new ArrayList<>());
        dto.setCustomerName("John Doe");
        dto.setAddress("123 Main St");
        dto.setRestaurantName("Tasty Bites");

        assertEquals(1L, dto.getId());
        assertEquals(1500.0, dto.getTotalAmount());
        assertEquals("PLACED", dto.getStatus());
        assertEquals(now, dto.getCreatedAt());
        assertNotNull(dto.getItems());
        assertEquals("John Doe", dto.getCustomerName());
        assertEquals("123 Main St", dto.getAddress());
        assertEquals("Tasty Bites", dto.getRestaurantName());
    }

    @Test
    void testAllArgsConstructor() {
        LocalDateTime now = LocalDateTime.now();
        OrderDTO dto = new OrderDTO(2L, 500.0, "PENDING", now, new ArrayList<>(), "Jane Doe", "456 Oak St", "Cafe Java");

        assertEquals(2L, dto.getId());
        assertEquals(500.0, dto.getTotalAmount());
        assertEquals("PENDING", dto.getStatus());
        assertEquals("Jane Doe", dto.getCustomerName());
        assertEquals("456 Oak St", dto.getAddress());
        assertEquals("Cafe Java", dto.getRestaurantName());
    }
}

class OrderItemDTOTest {

    @Test
    void testGettersAndSetters() {
        OrderItemDTO dto = new OrderItemDTO();
        dto.setItemName("Coke");
        dto.setQuantity(2);
        dto.setPrice(100.0);

        assertEquals("Coke", dto.getItemName());
        assertEquals(2, dto.getQuantity());
        assertEquals(100.0, dto.getPrice());
    }

    @Test
    void testAllArgsConstructor() {
        OrderItemDTO dto = new OrderItemDTO("Sprite", 1, 50.0);
        assertEquals("Sprite", dto.getItemName());
        assertEquals(1, dto.getQuantity());
        assertEquals(50.0, dto.getPrice());
    }
}