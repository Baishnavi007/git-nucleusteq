package com.baishnavi.restaurantOrderPortalBackend.dto;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class CartDTOTest {

    @Test
    void testGettersAndSetters() {
        CartDTO cartDTO = new CartDTO();
        List<CartItemDTO> items = new ArrayList<>();
        items.add(new CartItemDTO("Pizza", 2, 400.0));

        cartDTO.setTotalAmount(400.0);
        cartDTO.setItems(items);

        assertEquals(400.0, cartDTO.getTotalAmount());
        assertNotNull(cartDTO.getItems());
        assertEquals(1, cartDTO.getItems().size());
    }

    @Test
    void testAllArgsConstructor() {
        CartDTO cartDTO = new CartDTO(500.0, new ArrayList<>());
        assertEquals(500.0, cartDTO.getTotalAmount());
        assertNotNull(cartDTO.getItems());
    }
}

class CartItemDTOTest {

    @Test
    void testGettersAndSetters() {
        CartItemDTO itemDTO = new CartItemDTO();
        itemDTO.setItemName("Burger");
        itemDTO.setQuantity(3);
        itemDTO.setPrice(450.0);

        assertEquals("Burger", itemDTO.getItemName());
        assertEquals(3, itemDTO.getQuantity());
        assertEquals(450.0, itemDTO.getPrice());
    }

    @Test
    void testAllArgsConstructor() {
        CartItemDTO itemDTO = new CartItemDTO("Fries", 1, 100.0);
        assertEquals("Fries", itemDTO.getItemName());
        assertEquals(1, itemDTO.getQuantity());
        assertEquals(100.0, itemDTO.getPrice());
    }
}