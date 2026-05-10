package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.dto.CategoryResponse;
import com.baishnavi.restaurantOrderPortalBackend.entity.Category;
import com.baishnavi.restaurantOrderPortalBackend.entity.MenuItem;
import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.enums.RestaurantStatus;
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
class RestaurantServiceImplTest {

    @Mock
    private RestaurantRepository restaurantRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private CategoryRepository categoryRepository;

    @Mock
    private MenuItemRepository menuItemRepository;

    @Mock
    private SecurityContext securityContext;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private RestaurantServiceImpl restaurantService;

    private User user;
    private Restaurant restaurant;

    @BeforeEach
    void setUp() {
        SecurityContextHolder.setContext(securityContext);

        user = new User();
        user.setId(1L);
        user.setEmail("test@example.com");

        restaurant = new Restaurant();
        restaurant.setId(1L);
        restaurant.setName("Test Restaurant");
        restaurant.setOwner(user);
    }

    private void mockSecurity() {
        when(securityContext.getAuthentication()).thenReturn(authentication);
        when(authentication.getName()).thenReturn("test@example.com");
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
    }

    @Test
    void createRestaurant_withoutImage() {
        when(restaurantRepository.save(any(Restaurant.class))).thenReturn(restaurant);

        Restaurant savedRestaurant = restaurantService.createRestaurant(restaurant, null);

        assertNotNull(savedRestaurant);
        assertEquals("https://images.unsplash.com/photo-1414235077428-338989a2e8c0", restaurant.getImageUrl());
        verify(restaurantRepository).save(restaurant);
    }

    @Test
    void getAllRestaurants() {
        when(restaurantRepository.findAll()).thenReturn(List.of(restaurant));

        List<Restaurant> restaurants = restaurantService.getAllRestaurants();

        assertEquals(1, restaurants.size());
        verify(restaurantRepository).findAll();
    }

    @Test
    void getMyRestaurants() {
        mockSecurity();
        when(restaurantRepository.findByOwner(user)).thenReturn(List.of(restaurant));

        List<Restaurant> restaurants = restaurantService.getMyRestaurants();

        assertEquals(1, restaurants.size());
        verify(restaurantRepository).findByOwner(user);
    }

    @Test
    void updateStatus() {
        when(restaurantRepository.findById(1L)).thenReturn(Optional.of(restaurant));
        when(restaurantRepository.save(any(Restaurant.class))).thenReturn(restaurant);

        Restaurant updated = restaurantService.updateStatus(1L, "OPEN");

        assertEquals(RestaurantStatus.OPEN, updated.getStatus());
        verify(restaurantRepository).save(restaurant);
    }

    @Test
    void searchRestaurants() {
        when(restaurantRepository.findByNameContainingIgnoreCase("Test")).thenReturn(List.of(restaurant));

        List<Restaurant> restaurants = restaurantService.searchRestaurants("Test");

        assertEquals(1, restaurants.size());
        verify(restaurantRepository).findByNameContainingIgnoreCase("Test");
    }

    @Test
    void deleteRestaurant_success() {
        mockSecurity();
        when(restaurantRepository.findById(1L)).thenReturn(Optional.of(restaurant));

        Category category = new Category();
        category.setId(10L);
        when(categoryRepository.findByRestaurantIdAndIsDeletedFalse(1L)).thenReturn(List.of(category));

        MenuItem menuItem = new MenuItem();
        when(menuItemRepository.findByCategory(category)).thenReturn(List.of(menuItem));

        restaurantService.deleteRestaurant(1L);

        verify(menuItemRepository).deleteAll(anyList());
        verify(categoryRepository).delete(category);
        verify(restaurantRepository).delete(restaurant);
    }

    @Test
    void deleteRestaurant_unauthorized() {
        User otherUser = new User();
        otherUser.setId(2L);
        restaurant.setOwner(otherUser);

        mockSecurity();
        when(restaurantRepository.findById(1L)).thenReturn(Optional.of(restaurant));

        assertThrows(RuntimeException.class, () -> restaurantService.deleteRestaurant(1L));
    }

    @Test
    void getMenuByRestaurant() {
        Category category = new Category();
        category.setId(10L);
        category.setName("Starters");

        MenuItem menuItem = new MenuItem();
        menuItem.setName("Soup");

        when(categoryRepository.findByRestaurantIdAndIsDeletedFalse(1L)).thenReturn(List.of(category));
        when(menuItemRepository.findByCategoryIdAndIsAvailableTrueAndIsDeletedFalse(10L)).thenReturn(List.of(menuItem));

        List<CategoryResponse> responses = restaurantService.getMenuByRestaurant(1L);

        assertEquals(1, responses.size());
        assertEquals("Starters", responses.get(0).getCategoryName());
        assertEquals(1, responses.get(0).getItems().size());
    }
}