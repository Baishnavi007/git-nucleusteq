package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.constants.AppConstants;
import com.baishnavi.restaurantOrderPortalBackend.entity.Address;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
import com.baishnavi.restaurantOrderPortalBackend.exception.UnauthorizedException;
import com.baishnavi.restaurantOrderPortalBackend.exception.BadRequestException;
import com.baishnavi.restaurantOrderPortalBackend.repository.AddressRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.UserRepository;
import com.baishnavi.restaurantOrderPortalBackend.security.JwtUtil;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.time.LocalDateTime;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Implementation of UserService
 */
@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final JwtUtil jwtUtil;
    private final PasswordEncoder passwordEncoder;
    private final AddressRepository addressRepository;

    private static final Logger logger =
            LoggerFactory.getLogger(UserServiceImpl.class);

    public UserServiceImpl(UserRepository userRepository,
                           JwtUtil jwtUtil,
                           PasswordEncoder passwordEncoder,
                           AddressRepository addressRepository) {
        this.userRepository = userRepository;
        this.jwtUtil = jwtUtil;
        this.passwordEncoder = passwordEncoder;
        this.addressRepository = addressRepository;
    }

    /**
     * Register new user
     */
    @Override
    public User registerUser(User user) {

        logger.info("Registering user: {}", user.getEmail());

        if (userRepository.findByEmail(user.getEmail()).isPresent()) {
            logger.error("User already exists: {}", user.getEmail());
            throw new BadRequestException("User already exists");
        }

        user.setWalletBalance((double) AppConstants.DEFAULT_WALLET_BALANCE);
        user.setCreatedAt(LocalDateTime.now());
        user.setPassword(passwordEncoder.encode(user.getPassword()));

        User saved = userRepository.save(user);

        logger.info("User registered successfully: {}", saved.getId());

        return saved;
    }

    /**
     * Validate user credentials
     */
    @Override
    public User validateUser(String email, String password) {

        logger.info("Validating user: {}", email);

        User user = userRepository.findByEmail(email)
                .orElseThrow(() ->
                        new ResourceNotFoundException("User not found"));

        if (!passwordEncoder.matches(password, user.getPassword())) {
            logger.error("Invalid password for user: {}", email);
            throw new UnauthorizedException("Invalid credentials");
        }

        return user;
    }

    /**
     * Generate JWT token
     */
    @Override
    public String generateToken(User user) {

        logger.info("Generating token for user: {}", user.getEmail());

        return jwtUtil.generateToken(
                user.getEmail(),
                user.getRole().name()
        );
    }

    /**
     * Add money to wallet
     */
    @Override
    public Double addMoney(Double amount) {

        if (amount <= 0) {
            throw new BadRequestException("Amount must be greater than zero");
        }

        User user = getLoggedInUser();

        user.setWalletBalance(user.getWalletBalance() + amount);
        userRepository.save(user);

        logger.info("Money added. New balance: {}", user.getWalletBalance());

        return user.getWalletBalance();
    }

    /**
     * Deduct money from wallet
     */
    @Override
    public Double deductMoney(Double amount) {

        if (amount <= 0) {
            throw new BadRequestException("Invalid amount");
        }

        User user = getLoggedInUser();

        if (user.getWalletBalance() < amount) {
            throw new BadRequestException("Insufficient balance");
        }

        user.setWalletBalance(user.getWalletBalance() - amount);
        userRepository.save(user);

        logger.info("Money deducted. Remaining balance: {}", user.getWalletBalance());

        return user.getWalletBalance();
    }

    /**
     * Get wallet balance
     */
    @Override
    public Double getWalletBalance() {

        User user = getLoggedInUser();
        return user.getWalletBalance();
    }

    /**
     * Select an address
     */
    @Override
    public void selectAddress(Long addressId) {

        User user = getLoggedInUser();

        Address address = addressRepository.findById(addressId)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Address not found"));

        if (!address.getUser().getId().equals(user.getId())) {
            throw new UnauthorizedException("Address does not belong to user");
        }

        user.setSelectedAddressId(addressId);
        userRepository.save(user);

        logger.info("Address selected: {}", addressId);
    }

    /**
     * Get selected address
     */
    @Override
    public Address getSelectedAddress() {

        User user = getLoggedInUser();

        if (user.getSelectedAddressId() == null) {
            throw new BadRequestException("No address selected");
        }

        return addressRepository.findById(user.getSelectedAddressId())
                .orElseThrow(() ->
                        new ResourceNotFoundException("Address not found"));
    }

    /**
     * Get all user addresses
     */
    @Override
    public List<Address> getUserAddresses() {

        User user = getLoggedInUser();
        return user.getAddresses();
    }

    /**
     * Get logged-in user from security context
     */
    private User getLoggedInUser() {

        Authentication auth =
                SecurityContextHolder.getContext().getAuthentication();

        String email = auth.getName();

        return userRepository.findByEmail(email)
                .orElseThrow(() ->
                        new ResourceNotFoundException("User not found"));
    }
}