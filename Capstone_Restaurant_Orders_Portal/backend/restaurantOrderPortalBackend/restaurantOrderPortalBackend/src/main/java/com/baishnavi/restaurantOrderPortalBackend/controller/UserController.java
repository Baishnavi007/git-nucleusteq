package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.dto.CategoryResponse;
import com.baishnavi.restaurantOrderPortalBackend.entity.Address;
import com.baishnavi.restaurantOrderPortalBackend.entity.Restaurant;
import com.baishnavi.restaurantOrderPortalBackend.service.AddressService;
import com.baishnavi.restaurantOrderPortalBackend.service.RestaurantService;
import com.baishnavi.restaurantOrderPortalBackend.service.UserService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Controller for User APIs
 * Handles all user-related operations such as:
 * - Address management
 * - Wallet operations
 * - Restaurant browsing
 */
@RestController
@RequestMapping("/users")
public class UserController {

    private static final Logger logger =
            LoggerFactory.getLogger(UserController.class);

    private final RestaurantService restaurantService;
    private final UserService userService;
    private final AddressService addressService;

    /**
     * Constructor-based Dependency Injection
     */
    public UserController(UserService userService,
                          RestaurantService restaurantService,
                          AddressService addressService) {
        this.userService = userService;
        this.restaurantService = restaurantService;
        this.addressService = addressService;
    }

    /**
     * Get user profile
     * @return profile message
     */
    @GetMapping("/profile")
     public Map<String, Object> getProfile() {
         logger.info("User profile accessed");
            Double balance = userService.getWalletBalance();

            Map<String, Object> response = new HashMap<>();
            response.put("walletBalance", balance);

            return response;

    }

    /**
     * Add address for user
     * @param address Address object
     * @return saved address
     */
    @PostMapping("/address")
    public Address addAddress(@RequestBody Address address) {
        logger.info("Adding address for user: {}", address.getCity());
        return addressService.addAddress(address);
    }

    /**
     * Select active address for user
     * @param addressId selected address ID
     * @return success message
     */
    @PostMapping("/select-address")
    public String selectAddress(@RequestParam Long addressId) {
        logger.info("Selecting address with ID: {}", addressId);
        userService.selectAddress(addressId);
        return "Address selected successfully";
    }

    /**
     * Get restaurants for user
     * @return list of restaurants
     */
    @GetMapping("/restaurants")
    public List<Restaurant> getRestaurants() {
        return restaurantService.getAllRestaurants();
    }

    /**
     * Search restaurants by keyword
     * @param keyword search keyword
     * @return list of matching restaurants
     */
    @GetMapping("/search")
    public List<Restaurant> search(@RequestParam String keyword) {
        logger.info("Searching restaurants with keyword: {}", keyword);
        return restaurantService.searchRestaurants(keyword);
    }

    @GetMapping("/restaurants/{id}/menu")
    public List<CategoryResponse> getMenu(@PathVariable Long id) {
        return restaurantService.getMenuByRestaurant(id);
    }
    /**
     * Add money to wallet
     * @param amount amount to add
     * @return updated balance
     */
    @PostMapping("/wallet/add")
    public Double addMoney(@RequestParam Double amount) {
        logger.info("Adding money to wallet: {}", amount);
        return userService.addMoney(amount);
    }

    /**
     * Deduct money from wallet
     * @param amount amount to deduct
     * @return updated balance
     */
    @PostMapping("/wallet/deduct")
    public Double deductMoney(@RequestParam Double amount) {
        logger.info("Deducting money from wallet: {}", amount);
        return userService.deductMoney(amount);
    }

    /**
     * Get wallet balance
     * @return current balance
     */
    @GetMapping("/wallet")
    public Double getBalance() {
        logger.info("Fetching wallet balance");
        return userService.getWalletBalance();
    }

    /**
     * Get all addresses of logged-in user
     * @return list of addresses
     */
    @GetMapping("/addresses")
    public List<Address> getUserAddresses() {
        logger.info("Fetching all addresses for user");
        return userService.getUserAddresses();
    }
}