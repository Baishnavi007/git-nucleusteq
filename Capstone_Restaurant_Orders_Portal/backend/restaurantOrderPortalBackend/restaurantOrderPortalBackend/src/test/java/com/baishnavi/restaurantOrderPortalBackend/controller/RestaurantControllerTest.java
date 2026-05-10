package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.security.JwtUtil;
import com.baishnavi.restaurantOrderPortalBackend.service.RestaurantService;
import com.baishnavi.restaurantOrderPortalBackend.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;
import static org.mockito.Mockito.mock;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(RestaurantController.class)
@AutoConfigureMockMvc(addFilters = false)
class RestaurantControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private RestaurantService restaurantService;

    @MockitoBean
    private UserRepository userRepository;

    @MockitoBean
    private JwtUtil jwtUtil;

    private Restaurant restaurant;
    private User user;

    @BeforeEach
    void setUp() {
        user = new User();
        user.setId(1L);
        user.setEmail("owner@example.com");

        restaurant = new Restaurant();
        restaurant.setId(1L);
        restaurant.setName("Test Restaurant");
        restaurant.setCity("Pune");
        restaurant.setOwner(user);

        Authentication authentication = mock(Authentication.class);
        SecurityContext securityContext = mock(SecurityContext.class);
        when(securityContext.getAuthentication()).thenReturn(authentication);
        when(authentication.getName()).thenReturn("owner@example.com");
        SecurityContextHolder.setContext(securityContext);
    }

    @Test
    void createRestaurant() throws Exception {
        MockMultipartFile image = new MockMultipartFile("image", "test.jpg", "image/jpeg", "test image data".getBytes());

        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(user));
        when(restaurantService.createRestaurant(any(Restaurant.class), any())).thenReturn(restaurant);

        mockMvc.perform(multipart("/owner/restaurants")
                        .file(image)
                        .param("name", "Test Restaurant")
                        .param("city", "Pune")
                        .param("description", "Best food"))
                .andExpect(status().isOk());
    }

    @Test
    void getMyRestaurants() throws Exception {
        when(restaurantService.getMyRestaurants()).thenReturn(List.of(restaurant));

        mockMvc.perform(get("/owner/restaurants"))
                .andExpect(status().isOk());
    }

    @Test
    void deleteRestaurant() throws Exception {
        doNothing().when(restaurantService).deleteRestaurant(1L);

        mockMvc.perform(delete("/owner/restaurants/1"))
                .andExpect(status().isOk())
                .andExpect(content().string("Restaurant deleted successfully"));
    }

    @Test
    void updateStatus() throws Exception {
        when(restaurantService.updateStatus(1L, "OPEN")).thenReturn(restaurant);

        mockMvc.perform(post("/owner/restaurants/status")
                        .param("restaurantId", "1")
                        .param("status", "OPEN"))
                .andExpect(status().isOk());
    }
}