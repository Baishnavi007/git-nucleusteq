package com.baishnavi.restaurantOrderPortalBackend.entity;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class OrderItemTest {

    private OrderItem orderItem;
    private Order order;
    private MenuItem menuItem;

    @BeforeEach
    void setUp() {
        order = new Order();
        order.setId(1L);

        menuItem = new MenuItem();
        menuItem.setId(1L);

        orderItem = new OrderItem(1L, 2, 300.0, order, menuItem);
    }

    @Test
    void testGettersAndSetters() {
        OrderItem newItem = new OrderItem();
        newItem.setId(2L);
        newItem.setQuantity(3);
        newItem.setPrice(450.0);
        newItem.setOrder(order);
        newItem.setMenuItem(menuItem);

        assertEquals(2L, newItem.getId());
        assertEquals(3, newItem.getQuantity());
        assertEquals(450.0, newItem.getPrice());
        assertEquals(order, newItem.getOrder());
        assertEquals(menuItem, newItem.getMenuItem());
    }

    @Test
    void testEqualsAndHashCode() {
        OrderItem item1 = new OrderItem();
        item1.setId(1L);

        OrderItem item2 = new OrderItem();
        item2.setId(1L);

        OrderItem item3 = new OrderItem();
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
        String expectedString = "OrderItem{id=1, quantity=2, price=300.0}";
        assertEquals(expectedString, orderItem.toString());
    }
}