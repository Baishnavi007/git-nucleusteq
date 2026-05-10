package com.baishnavi.restaurantOrderPortalBackend.entity;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;

class CategoryTest {

    private Category category;
    private Restaurant restaurant;

    @BeforeEach
    void setUp() {
        restaurant = new Restaurant();
        restaurant.setId(1L);

        category = new Category(1L, "Starters", restaurant, new ArrayList<>());
    }

    @Test
    void testGettersAndSetters() {
        Category newCategory = new Category();
        newCategory.setId(2L);
        newCategory.setName("Desserts");
        newCategory.setRestaurant(restaurant);
        newCategory.setMenuItems(new ArrayList<>());
        newCategory.setDeleted(true);

        assertEquals(2L, newCategory.getId());
        assertEquals("Desserts", newCategory.getName());
        assertEquals(restaurant, newCategory.getRestaurant());
        assertNotNull(newCategory.getMenuItems());
        assertTrue(newCategory.getDeleted());
    }

    @Test
    void testEqualsAndHashCode() {
        Category category1 = new Category();
        category1.setId(1L);

        Category category2 = new Category();
        category2.setId(1L);

        Category category3 = new Category();
        category3.setId(2L);

        assertEquals(category1, category1);
        assertEquals(category1, category2);
        assertNotEquals(category1, category3);
        assertNotEquals(category1, null);
        assertNotEquals(category1, new Object());

        assertEquals(category1.hashCode(), category2.hashCode());
    }

    @Test
    void testToString() {
        String expectedString = "Category{id=1, name='Starters'}";
        assertEquals(expectedString, category.toString());
    }
}