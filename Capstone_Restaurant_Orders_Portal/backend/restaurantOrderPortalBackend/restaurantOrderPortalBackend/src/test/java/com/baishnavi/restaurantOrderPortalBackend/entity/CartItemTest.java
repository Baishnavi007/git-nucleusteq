package com.baishnavi.restaurantOrderPortalBackend.entity;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CartItemTest {

    private CartItem cartItem;
    private Cart cart;
    private MenuItem menuItem;

    @BeforeEach
    void setUp() {
        cart = new Cart();
        cart.setId(1L);

        menuItem = new MenuItem();
        menuItem.setId(1L);

        cartItem = new CartItem(1L, 1, 150.0, cart, menuItem);
    }

    @Test
    void testGettersAndSetters() {
        CartItem newItem = new CartItem();
        newItem.setId(2L);
        newItem.setQuantity(4);
        newItem.setPrice(600.0);
        newItem.setCart(cart);
        newItem.setMenuItem(menuItem);

        assertEquals(2L, newItem.getId());
        assertEquals(4, newItem.getQuantity());
        assertEquals(600.0, newItem.getPrice());
        assertEquals(cart, newItem.getCart());
        assertEquals(menuItem, newItem.getMenuItem());
    }

    @Test
    void testEqualsAndHashCode() {
        CartItem item1 = new CartItem();
        item1.setId(1L);

        CartItem item2 = new CartItem();
        item2.setId(1L);

        CartItem item3 = new CartItem();
        item3.setId(2L);

        assertEquals(item1, item1);
        assertEquals(item1, item2);
        assertNotEquals(item1, item3);
        assertNotEquals(item1, null);
        assertNotEquals(item1, new Object());

        assertEquals(item1.hashCode(), item2.hashCode());
    }

    @Test
    void testToString() {
        String expectedString = "CartItem{id=1, quantity=1, price=150.0}";
        assertEquals(expectedString, cartItem.toString());
    }
}