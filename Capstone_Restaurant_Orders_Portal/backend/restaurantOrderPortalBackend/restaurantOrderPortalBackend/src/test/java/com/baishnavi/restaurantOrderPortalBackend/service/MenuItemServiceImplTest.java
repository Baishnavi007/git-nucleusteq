package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Category;
import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
import com.baishnavi.restaurantOrderPortalBackend.repository.CategoryRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.MenuItemRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class MenuItemServiceImplTest {

    @Mock
    private MenuItemRepository menuItemRepository;

    @Mock
    private CategoryRepository categoryRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private SecurityContext securityContext;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private MenuItemServiceImpl menuItemService;

    private User user;
    private Restaurant restaurant;
    private Category category;
    private MenuItem menuItem;

    @BeforeEach
    void setUp() {
        SecurityContextHolder.setContext(securityContext);

        user = new User();
        user.setId(1L);
        user.setEmail("test@example.com");

        restaurant = new Restaurant();
        restaurant.setId(10L);
        restaurant.setOwner(user);

        category = new Category();
        category.setId(100L);
        category.setRestaurant(restaurant);

        menuItem = new MenuItem();
        menuItem.setId(1000L);
        menuItem.setName("Burger");
        menuItem.setRestaurant(restaurant);
        menuItem.setCategory(category);
    }

    private void mockSecurity() {
        when(securityContext.getAuthentication()).thenReturn(authentication);
        when(authentication.getName()).thenReturn("test@example.com");
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
    }

    @Test
    void addMenuItem_success() {
        mockSecurity();
        when(categoryRepository.findById(100L)).thenReturn(Optional.of(category));
        when(menuItemRepository.save(any(MenuItem.class))).thenReturn(menuItem);

        MenuItem savedItem = menuItemService.addMenuItem(100L, "Burger", "Tasty", 150.0);

        assertNotNull(savedItem);
        verify(menuItemRepository).save(any(MenuItem.class));
    }

    @Test
    void addMenuItem_unauthorized() {
        User otherUser = new User();
        otherUser.setId(2L);
        restaurant.setOwner(otherUser);

        mockSecurity();
        when(categoryRepository.findById(100L)).thenReturn(Optional.of(category));

        assertThrows(RuntimeException.class, () -> menuItemService.addMenuItem(100L, "Burger", "Tasty", 150.0));
    }

    @Test
    void getAllMenuItems_success() {
        when(menuItemRepository.findByCategoryIdAndIsDeletedFalse(100L)).thenReturn(List.of(menuItem));

        List<MenuItem> items = menuItemService.getAllMenuItems(100L);

        assertEquals(1, items.size());
        verify(menuItemRepository).findByCategoryIdAndIsDeletedFalse(100L);
    }

    @Test
    void getAvailableMenuItems_success() {
        when(menuItemRepository.findByCategoryIdAndIsAvailableTrueAndIsDeletedFalse(100L)).thenReturn(List.of(menuItem));

        List<MenuItem> items = menuItemService.getAvailableMenuItems(100L);

        assertEquals(1, items.size());
        verify(menuItemRepository).findByCategoryIdAndIsAvailableTrueAndIsDeletedFalse(100L);
    }

    @Test
    void updateAvailability_success() {
        mockSecurity();
        when(menuItemRepository.findById(1000L)).thenReturn(Optional.of(menuItem));
        when(menuItemRepository.save(any(MenuItem.class))).thenReturn(menuItem);

        MenuItem updatedItem = menuItemService.updateAvailability(1000L, false);

        assertFalse(updatedItem.getIsAvailable());
        verify(menuItemRepository).save(menuItem);
    }

    @Test
    void updateMenuItem_success() {
        when(menuItemRepository.findById(1000L)).thenReturn(Optional.of(menuItem));
        when(menuItemRepository.save(any(MenuItem.class))).thenReturn(menuItem);

        MenuItem updatedItem = menuItemService.updateMenuItem(1000L, "New Burger", "New Desc", 200.0);

        assertEquals("New Burger", updatedItem.getName());
        verify(menuItemRepository).save(menuItem);
    }

    @Test
    void deleteMenuItem_success() {
        mockSecurity();
        when(menuItemRepository.findById(1000L)).thenReturn(Optional.of(menuItem));
        when(menuItemRepository.save(any(MenuItem.class))).thenReturn(menuItem);

        menuItemService.deleteMenuItem(1000L);

        assertTrue(menuItem.getDeleted());
        assertFalse(menuItem.getIsAvailable());
        verify(menuItemRepository).save(menuItem);
    }
}