package com.baishnavi.restaurantOrderPortalBackend.entity;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class MenuItemTest {

    private MenuItem menuItem;
    private Category category;
    private Restaurant restaurant;

    @BeforeEach
    void setUp() {
        category = new Category();
        category.setId(1L);

        restaurant = new Restaurant();
        restaurant.setId(1L);

        menuItem = new MenuItem(
                1L, "Pizza", "Cheese Pizza", 200.0,
                category, true, restaurant
        );
    }

    @Test
    void testGettersAndSetters() {
        MenuItem newItem = new MenuItem();
        newItem.setId(2L);
        newItem.setName("Burger");
        newItem.setDescription("Veg Burger");
        newItem.setPrice(150.0);
        newItem.setCategory(category);
        newItem.setIsAvailable(false);
        newItem.setDeleted(true);
        newItem.setRestaurant(restaurant);

        assertEquals(2L, newItem.getId());
        assertEquals("Burger", newItem.getName());
        assertEquals("Veg Burger", newItem.getDescription());
        assertEquals(150.0, newItem.getPrice());
        assertEquals(category, newItem.getCategory());
        assertFalse(newItem.getIsAvailable());
        assertTrue(newItem.getDeleted());
        assertEquals(restaurant, newItem.getRestaurant());
    }

    @Test
    void testEqualsAndHashCode() {
        MenuItem item1 = new MenuItem();
        item1.setId(1L);

        MenuItem item2 = new MenuItem();
        item2.setId(1L);

        MenuItem item3 = new MenuItem();
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
        String expectedString = "MenuItem{id=1, name='Pizza', price=200.0, isAvailable=true}";
        assertEquals(expectedString, menuItem.toString());
    }
}