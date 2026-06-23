package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Category;
import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
import com.baishnavi.restaurantOrderPortalBackend.repository.CategoryRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.MenuItemRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.RestaurantRepository;
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
class CategoryServiceImplTest {

    @Mock
    private CategoryRepository categoryRepository;

    @Mock
    private RestaurantRepository restaurantRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private MenuItemRepository menuItemRepository;

    @Mock
    private SecurityContext securityContext;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private CategoryServiceImpl categoryService;

    private User user;
    private Restaurant restaurant;
    private Category category;

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
        category.setName("Beverages");
        category.setRestaurant(restaurant);
        category.setDeleted(false);
    }

    private void mockSecurity() {
        when(securityContext.getAuthentication()).thenReturn(authentication);
        when(authentication.getName()).thenReturn("test@example.com");
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
    }

    @Test
    void addCategory_success() {
        mockSecurity();
        when(restaurantRepository.findById(10L)).thenReturn(Optional.of(restaurant));
        when(categoryRepository.save(any(Category.class))).thenReturn(category);

        Category savedCategory = categoryService.addCategory(10L, "Beverages");

        assertNotNull(savedCategory);
        assertEquals("Beverages", savedCategory.getName());
        verify(categoryRepository).save(any(Category.class));
    }

    @Test
    void addCategory_unauthorized() {
        User otherUser = new User();
        otherUser.setId(2L);
        restaurant.setOwner(otherUser);

        mockSecurity();
        when(restaurantRepository.findById(10L)).thenReturn(Optional.of(restaurant));

        assertThrows(RuntimeException.class, () -> categoryService.addCategory(10L, "Beverages"));
    }

    @Test
    void getCategoriesByRestaurant_success() {
        when(categoryRepository.findByRestaurantIdAndIsDeletedFalse(10L)).thenReturn(List.of(category));

        List<Category> categories = categoryService.getCategoriesByRestaurant(10L);

        assertEquals(1, categories.size());
        verify(categoryRepository).findByRestaurantIdAndIsDeletedFalse(10L);
    }

    @Test
    void deleteCategory_success() {
        mockSecurity();
        when(categoryRepository.findById(100L)).thenReturn(Optional.of(category));
        when(categoryRepository.save(any(Category.class))).thenReturn(category);

        categoryService.deleteCategory(100L);

        assertTrue(category.getDeleted());
        verify(categoryRepository).save(category);
    }

    @Test
    void deleteCategory_unauthorized() {
        User otherUser = new User();
        otherUser.setId(2L);
        restaurant.setOwner(otherUser);

        mockSecurity();
        when(categoryRepository.findById(100L)).thenReturn(Optional.of(category));

        assertThrows(RuntimeException.class, () -> categoryService.deleteCategory(100L));
    }
}