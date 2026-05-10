package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.dto.CategoryResponse;
import com.baishnavi.restaurantOrderPortalBackend.entity.Address;
import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import com.baishnavi.restaurantOrderPortalBackend.security.JwtUtil;
import com.baishnavi.restaurantOrderPortalBackend.service.AddressService;
import com.baishnavi.restaurantOrderPortalBackend.service.RestaurantService;
import com.baishnavi.restaurantOrderPortalBackend.service.UserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.ArrayList;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(UserController.class)
@AutoConfigureMockMvc(addFilters = false)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private UserService userService;

    @MockitoBean
    private RestaurantService restaurantService;

    @MockitoBean
    private AddressService addressService;

    @MockitoBean
    private JwtUtil jwtUtil;

    @Autowired
    private ObjectMapper objectMapper;

    private Address address;
    private Restaurant restaurant;
    private CategoryResponse categoryResponse;

    @BeforeEach
    void setUp() {
        address = new Address();
        address.setId(1L);
        address.setCity("Pune");
        address.setStreet("MG Road");
        address.setPincode("411001");

        restaurant = new Restaurant();
        restaurant.setId(1L);
        restaurant.setName("Test Restaurant");

        categoryResponse = new CategoryResponse("Starters", new ArrayList<>());
    }

    @Test
    void getProfile() throws Exception {
        when(userService.getWalletBalance()).thenReturn(500.0);

        mockMvc.perform(get("/users/profile"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.walletBalance").value(500.0));
    }

    @Test
    void addAddress() throws Exception {
        when(addressService.addAddress(any(Address.class))).thenReturn(address);

        mockMvc.perform(post("/users/address")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(address)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.city").value("Pune"));
    }

    @Test
    void selectAddress() throws Exception {
        doNothing().when(userService).selectAddress(1L);

        mockMvc.perform(post("/users/select-address")
                        .param("addressId", "1"))
                .andExpect(status().isOk())
                .andExpect(content().string("Address selected successfully"));
    }

    @Test
    void getRestaurants() throws Exception {
        when(restaurantService.getAllRestaurants()).thenReturn(List.of(restaurant));

        mockMvc.perform(get("/users/restaurants"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Test Restaurant"));
    }

    @Test
    void search() throws Exception {
        when(restaurantService.searchRestaurants("Test")).thenReturn(List.of(restaurant));

        mockMvc.perform(get("/users/search")
                        .param("keyword", "Test"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Test Restaurant"));
    }

    @Test
    void getMenu() throws Exception {
        when(restaurantService.getMenuByRestaurant(1L)).thenReturn(List.of(categoryResponse));

        mockMvc.perform(get("/users/restaurants/1/menu"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].categoryName").value("Starters"));
    }

    @Test
    void addMoney() throws Exception {
        when(userService.addMoney(100.0)).thenReturn(600.0);

        mockMvc.perform(post("/users/wallet/add")
                        .param("amount", "100.0"))
                .andExpect(status().isOk())
                .andExpect(content().string("600.0"));
    }

    @Test
    void deductMoney() throws Exception {
        when(userService.deductMoney(50.0)).thenReturn(450.0);

        mockMvc.perform(post("/users/wallet/deduct")
                        .param("amount", "50.0"))
                .andExpect(status().isOk())
                .andExpect(content().string("450.0"));
    }

    @Test
    void getBalance() throws Exception {
        when(userService.getWalletBalance()).thenReturn(500.0);

        mockMvc.perform(get("/users/wallet"))
                .andExpect(status().isOk())
                .andExpect(content().string("500.0"));
    }

    @Test
    void getUserAddresses() throws Exception {
        when(userService.getUserAddresses()).thenReturn(List.of(address));

        mockMvc.perform(get("/users/addresses"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].city").value("Pune"));
    }
}