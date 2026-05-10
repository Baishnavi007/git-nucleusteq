package com.baishnavi.restaurantOrderPortalBackend.entity;

import com.baishnavi.restaurantOrderPortalBackend.enums.RestaurantStatus;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;

class RestaurantTest {

    private Restaurant restaurant;
    private User owner;

    @BeforeEach
    void setUp() {
        owner = new User();
        owner.setId(1L);

        restaurant = new Restaurant(
                1L, "Test Cafe", "Pune", "Nice place",
                "http://image.url", RestaurantStatus.OPEN,
                owner, new ArrayList<>()
        );
    }

    @Test
    void testGettersAndSetters() {
        Restaurant newRestaurant = new Restaurant();
        newRestaurant.setId(2L);
        newRestaurant.setName("New Cafe");
        newRestaurant.setCity("Mumbai");
        newRestaurant.setDescription("Great food");
        newRestaurant.setImageUrl("http://new.url");
        newRestaurant.setStatus(RestaurantStatus.CLOSED);
        newRestaurant.setOwner(owner);
        newRestaurant.setCategories(new ArrayList<>());

        assertEquals(2L, newRestaurant.getId());
        assertEquals("New Cafe", newRestaurant.getName());
        assertEquals("Mumbai", newRestaurant.getCity());
        assertEquals("Great food", newRestaurant.getDescription());
        assertEquals("http://new.url", newRestaurant.getImageUrl());
        assertEquals(RestaurantStatus.CLOSED, newRestaurant.getStatus());
        assertEquals(owner, newRestaurant.getOwner());
        assertNotNull(newRestaurant.getCategories());
    }

    @Test
    void testEqualsAndHashCode() {
        Restaurant restaurant1 = new Restaurant();
        restaurant1.setId(1L);

        Restaurant restaurant2 = new Restaurant();
        restaurant2.setId(1L);

        Restaurant restaurant3 = new Restaurant();
        restaurant3.setId(2L);

        assertEquals(restaurant1, restaurant1);
        assertEquals(restaurant1, restaurant2);
        assertNotEquals(restaurant1, restaurant3);
        assertNotEquals(restaurant1, null);
        assertNotEquals(restaurant1, new Object());

        assertEquals(restaurant1.hashCode(), restaurant2.hashCode());
        assertNotEquals(restaurant1.hashCode(), restaurant3.hashCode());
    }

    @Test
    void testToString() {
        String expectedString = "Restaurant{id=1, name='Test Cafe', city='Pune', status=OPEN}";
        assertEquals(expectedString, restaurant.toString());
    }
}