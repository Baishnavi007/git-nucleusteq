package com.baishnavi.restaurantOrderPortalBackend.dto;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class CategoryRequestDTOTest {

    @Test
    void testGettersAndSetters() {
        CategoryRequestDTO dto = new CategoryRequestDTO();
        dto.setRestaurantId(1L);
        dto.setName("Beverages");

        assertEquals(1L, dto.getRestaurantId());
        assertEquals("Beverages", dto.getName());
    }

    @Test
    void testAllArgsConstructor() {
        CategoryRequestDTO dto = new CategoryRequestDTO(2L, "Desserts");
        assertEquals(2L, dto.getRestaurantId());
        assertEquals("Desserts", dto.getName());
    }
}

class CategoryResponseTest {

    @Test
    void testConstructorsAndGetters() {
        CategoryResponse response = new CategoryResponse("Starters", new ArrayList<>());

        assertEquals("Starters", response.getCategoryName());
        assertNotNull(response.getItems());
    }
}

class CategoryMenuDTOTest {

    @Test
    void testGettersAndSetters() {
        CategoryMenuDTO dto = new CategoryMenuDTO();
        dto.setCategoryId(1L);
        dto.setCategoryName("Mains");
        dto.setItems(new ArrayList<>());

        assertEquals(1L, dto.getCategoryId());
        assertEquals("Mains", dto.getCategoryName());
        assertNotNull(dto.getItems());
    }

    @Test
    void testAllArgsConstructor() {
        CategoryMenuDTO dto = new CategoryMenuDTO(2L, "Soups", new ArrayList<>());
        assertEquals(2L, dto.getCategoryId());
        assertEquals("Soups", dto.getCategoryName());
        assertNotNull(dto.getItems());
    }
}