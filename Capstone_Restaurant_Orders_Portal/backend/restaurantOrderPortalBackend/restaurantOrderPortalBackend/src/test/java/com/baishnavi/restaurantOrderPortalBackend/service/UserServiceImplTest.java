package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Address;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.enums.Role;
import com.baishnavi.restaurantOrderPortalBackend.exception.BadRequestException;
import com.baishnavi.restaurantOrderPortalBackend.exception.ResourceNotFoundException;
import com.baishnavi.restaurantOrderPortalBackend.exception.UnauthorizedException;
import com.baishnavi.restaurantOrderPortalBackend.repository.AddressRepository;
import com.baishnavi.restaurantOrderPortalBackend.repository.UserRepository;
import com.baishnavi.restaurantOrderPortalBackend.security.JwtUtil;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceImplTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private JwtUtil jwtUtil;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private AddressRepository addressRepository;

    @Mock
    private SecurityContext securityContext;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private UserServiceImpl userService;

    private User user;
    private String email = "test@example.com";

    @BeforeEach
    void setUp() {
        user = new User();
        user.setId(1L);
        user.setEmail(email);
        user.setPassword("encodedPassword");
        user.setRole(Role.USER);
        user.setWalletBalance(100.0);
        user.setAddresses(new ArrayList<>());
    }

    private void mockSecurityContext() {
        SecurityContextHolder.setContext(securityContext);
        when(securityContext.getAuthentication()).thenReturn(authentication);
        when(authentication.getName()).thenReturn(email);
    }

    @Test
    void registerUser_Success() {
        when(userRepository.findByEmail(email)).thenReturn(Optional.empty());
        when(passwordEncoder.encode(any())).thenReturn("encodedPassword");
        when(userRepository.save(any(User.class))).thenReturn(user);

        User result = userService.registerUser(user);

        assertNotNull(result);
        assertEquals(email, result.getEmail());
        verify(userRepository).save(any(User.class));
    }

    @Test
    void registerUser_AlreadyExists() {
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));

        assertThrows(BadRequestException.class, () -> userService.registerUser(user));
    }

    @Test
    void validateUser_Success() {
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));
        when(passwordEncoder.matches("password", "encodedPassword")).thenReturn(true);

        User result = userService.validateUser(email, "password");

        assertNotNull(result);
        assertEquals(email, result.getEmail());
    }

    @Test
    void validateUser_InvalidPassword() {
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));
        when(passwordEncoder.matches("wrong", "encodedPassword")).thenReturn(false);

        assertThrows(UnauthorizedException.class, () -> userService.validateUser(email, "wrong"));
    }

    @Test
    void validateUser_NotFound() {
        when(userRepository.findByEmail(email)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> userService.validateUser(email, "password"));
    }

    @Test
    void generateToken_Success() {
        when(jwtUtil.generateToken(email, "USER")).thenReturn("token");

        String token = userService.generateToken(user);

        assertEquals("token", token);
    }

    @Test
    void addMoney_Success() {
        mockSecurityContext();
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));

        Double newBalance = userService.addMoney(50.0);

        assertEquals(150.0, newBalance);
        verify(userRepository).save(user);
    }

    @Test
    void addMoney_InvalidAmount() {
        assertThrows(BadRequestException.class, () -> userService.addMoney(0.0));
    }

    @Test
    void deductMoney_Success() {
        mockSecurityContext();
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));

        Double remaining = userService.deductMoney(40.0);

        assertEquals(60.0, remaining);
        verify(userRepository).save(user);
    }

    @Test
    void deductMoney_InsufficientBalance() {
        mockSecurityContext();
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));

        assertThrows(BadRequestException.class, () -> userService.deductMoney(200.0));
    }

    @Test
    void getWalletBalance_Success() {
        mockSecurityContext();
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));

        Double balance = userService.getWalletBalance();

        assertEquals(100.0, balance);
    }

    @Test
    void selectAddress_Success() {
        mockSecurityContext();
        Address address = new Address();
        address.setId(10L);
        address.setUser(user);

        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));

        userService.selectAddress(10L);

        assertEquals(10L, user.getSelectedAddressId());
        verify(userRepository).save(user);
    }

    @Test
    void selectAddress_Unauthorized() {
        mockSecurityContext();
        User otherUser = new User();
        otherUser.setId(2L);

        Address address = new Address();
        address.setId(10L);
        address.setUser(otherUser);

        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));

        assertThrows(UnauthorizedException.class, () -> userService.selectAddress(10L));
    }

    @Test
    void getSelectedAddress_Success() {
        mockSecurityContext();
        user.setSelectedAddressId(10L);
        Address address = new Address();
        address.setId(10L);

        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));

        Address result = userService.getSelectedAddress();

        assertNotNull(result);
        assertEquals(10L, result.getId());
    }

    @Test
    void getSelectedAddress_NoneSelected() {
        mockSecurityContext();
        user.setSelectedAddressId(null);
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));

        assertThrows(BadRequestException.class, () -> userService.getSelectedAddress());
    }

    @Test
    void getUserAddresses_Success() {
        mockSecurityContext();
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(user));

        List<Address> results = userService.getUserAddresses();

        assertNotNull(results);
    }
}