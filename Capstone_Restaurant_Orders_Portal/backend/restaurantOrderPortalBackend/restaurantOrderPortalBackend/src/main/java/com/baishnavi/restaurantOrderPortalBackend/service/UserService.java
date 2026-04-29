package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Address;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;

import java.util.List;

/**
 * Service interface for User operations
 */
public interface UserService {

    /**
     * Register a new user
     *
     * @param user user object
     * @return saved user
     */
    User registerUser(User user);

    /**
     * Validate user credentials
     *
     * @param email user email
     * @param password raw password
     * @return authenticated user
     */
    User validateUser(String email, String password);

    /**
     * Generate JWT token
     *
     * @param user authenticated user
     * @return JWT token
     */
    String generateToken(User user);

    /**
     * Add money to wallet
     *
     * @param amount amount to add
     * @return updated balance
     */
    Double addMoney(Double amount);

    /**
     * Deduct money from wallet
     *
     * @param amount amount to deduct
     * @return updated balance
     */
    Double deductMoney(Double amount);

    /**
     * Get wallet balance
     *
     * @return wallet balance
     */
    Double getWalletBalance();

    /**
     * Select an address for the user
     *
     * @param addressId address ID to select
     */
    void selectAddress(Long addressId);

    /**
     * Get currently selected address of user
     *
     * @return selected Address
     */
    Address getSelectedAddress();

    /**
     * Get all user addresses
     *
     * @return list of addresses
     */
    List<Address> getUserAddresses();
}