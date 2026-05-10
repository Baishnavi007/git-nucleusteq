package com.baishnavi.restaurantOrderPortalBackend.controller;

import com.baishnavi.restaurantOrderPortalBackend.entity.Address;
import com.baishnavi.restaurantOrderPortalBackend.service.AddressService;

import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for Address APIs
 */
@RestController
@RequestMapping("/users/address")
public class AddressController {

    private final AddressService addressService;

    public AddressController(AddressService addressService) {
        this.addressService = addressService;
    }

    /**
     * Add new address
     */
    @PostMapping("/add")
    public Address addAddress(@RequestBody Address address) {
        return addressService.addAddress(address);
    }

    /**
     * Get all addresses of user
     */
    @GetMapping
    public List<Address> getAllAddresses() {
        return addressService.getUserAddresses();
    }

    /**
     * Select address for order
     */
    @PostMapping("/select")
    public String selectAddress(@RequestParam Long addressId) {
        addressService.selectAddress(addressId);
        return "Address selected successfully";
    }
}