package com.baishnavi.restaurantOrderPortalBackend.entity;

import com.baishnavi.restaurantOrderPortalBackend.enums.OrderStatus;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;

class OrderTest {

    private Order order;
    private User user;
    private Address address;
    private Restaurant restaurant;
    private LocalDateTime now;

    @BeforeEach
    void setUp() {
        user = new User();
        user.setId(1L);

        address = new Address();
        address.setId(1L);

        restaurant = new Restaurant();
        restaurant.setId(1L);

        now = LocalDateTime.now();

        order = new Order(
                1L, 500.0, OrderStatus.PLACED, now,
                user, address, restaurant, new ArrayList<>()
        );
    }

    @Test
    void testGettersAndSetters() {
        Order newOrder = new Order();
        newOrder.setId(2L);
        newOrder.setTotalAmount(1000.0);
        newOrder.setStatus(OrderStatus.PENDING);
        newOrder.setCreatedAt(now);
        newOrder.setUser(user);
        newOrder.setAddress(address);
        newOrder.setRestaurant(restaurant);
        newOrder.setOrderItems(new ArrayList<>());

        assertEquals(2L, newOrder.getId());
        assertEquals(1000.0, newOrder.getTotalAmount());
        assertEquals(OrderStatus.PENDING, newOrder.getStatus());
        assertEquals(now, newOrder.getCreatedAt());
        assertEquals(user, newOrder.getUser());
        assertEquals(address, newOrder.getAddress());
        assertEquals(restaurant, newOrder.getRestaurant());
        assertNotNull(newOrder.getOrderItems());
    }

    @Test
    void testEqualsAndHashCode() {
        Order order1 = new Order();
        order1.setId(1L);

        Order order2 = new Order();
        order2.setId(1L);

        Order order3 = new Order();
        order3.setId(2L);

        assertEquals(order1, order1);
        assertEquals(order1, order2);
        assertNotEquals(order1, order3);
        assertNotEquals(order1, null);
        assertNotEquals(order1, new Object());

        assertEquals(order1.hashCode(), order2.hashCode());
    }

    @Test
    void testToString() {
        String expectedString = "Order{id=1, totalAmount=500.0, status=PLACED, createdAt=" + now + "}";
        assertEquals(expectedString, order.toString());
    }
}