package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Address;

/**
 * Service for handling address operations
 */
public interface AddressService {

    /**
     * Add address for logged-in user
     */
    Address addAddress(Address address);
}