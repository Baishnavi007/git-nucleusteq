package com.baishnavi.restaurantOrderPortalBackend.entity;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;

class CartTest {

    private Cart cart;
    private User user;

    @BeforeEach
    void setUp() {
        user = new User();
        user.setId(1L);

        cart = new Cart(1L, 250.0, user, new ArrayList<>());
    }

    @Test
    void testGettersAndSetters() {
        Cart newCart = new Cart();
        newCart.setId(2L);
        newCart.setTotalAmount(500.0);
        newCart.setUser(user);
        newCart.setCartItems(new ArrayList<>());

        assertEquals(2L, newCart.getId());
        assertEquals(500.0, newCart.getTotalAmount());
        assertEquals(user, newCart.getUser());
        assertNotNull(newCart.getCartItems());
    }

    @Test
    void testEqualsAndHashCode() {
        Cart cart1 = new Cart();
        cart1.setId(1L);

        Cart cart2 = new Cart();
        cart2.setId(1L);

        Cart cart3 = new Cart();
        cart3.setId(2L);

        assertEquals(cart1, cart1);
        assertEquals(cart1, cart2);
        assertNotEquals(cart1, cart3);
        assertNotEquals(cart1, null);
        assertNotEquals(cart1, new Object());

        assertEquals(cart1.hashCode(), cart2.hashCode());
    }

    @Test
    void testToString() {
        String expectedString = "Cart{id=1, totalAmount=250.0}";
        assertEquals(expectedString, cart.toString());
    }
}