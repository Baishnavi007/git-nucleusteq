package com.baishnavi.restaurantOrderPortalBackend.service;

import com.baishnavi.restaurantOrderPortalBackend.entity.Address;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import com.baishnavi.restaurantOrderPortalBackend.repository.AddressRepository;
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
class AddressServiceImplTest {

    @Mock
    private AddressRepository addressRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private SecurityContext securityContext;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private AddressServiceImpl addressService;

    private User user;
    private Address address;

    @BeforeEach
    void setUp() {
        SecurityContextHolder.setContext(securityContext);

        user = new User();
        user.setId(1L);
        user.setEmail("test@example.com");

        address = new Address();
        address.setId(10L);
        address.setUser(user);
    }

    private void mockAuth() {
        when(securityContext.getAuthentication()).thenReturn(authentication);
        when(authentication.getName()).thenReturn("test@example.com");
    }

    @Test
    void addAddress_Success() {
        mockAuth();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(addressRepository.save(any(Address.class))).thenReturn(address);

        Address result = addressService.addAddress(new Address());

        assertNotNull(result);
        assertEquals(user, result.getUser());
        verify(addressRepository).save(any(Address.class));
    }

    @Test
    void addAddress_UserNotFound() {
        mockAuth();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.empty());

        RuntimeException ex = assertThrows(RuntimeException.class, () -> addressService.addAddress(new Address()));
        assertEquals("User not found", ex.getMessage());
    }

    @Test
    void getUserAddresses_Success() {
        mockAuth();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(addressRepository.findByUser(user)).thenReturn(List.of(address));

        List<Address> results = addressService.getUserAddresses();

        assertFalse(results.isEmpty());
        assertEquals(1, results.size());
    }

    @Test
    void getUserAddresses_UserNotFound() {
        mockAuth();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.empty());

        RuntimeException ex = assertThrows(RuntimeException.class, () -> addressService.getUserAddresses());
        assertEquals("User not found", ex.getMessage());
    }

    @Test
    void selectAddress_Success() {
        mockAuth();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));

        addressService.selectAddress(10L);

        assertEquals(10L, user.getSelectedAddressId());
        verify(userRepository).save(user);
    }

    @Test
    void selectAddress_UserNotFound() {
        mockAuth();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.empty());

        RuntimeException ex = assertThrows(RuntimeException.class, () -> addressService.selectAddress(10L));
        assertEquals("User not found", ex.getMessage());
    }

    @Test
    void selectAddress_AddressNotFound() {
        mockAuth();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(addressRepository.findById(99L)).thenReturn(Optional.empty());

        RuntimeException ex = assertThrows(RuntimeException.class, () -> addressService.selectAddress(99L));
        assertEquals("Address not found", ex.getMessage());
    }

    @Test
    void selectAddress_Unauthorized() {
        User otherUser = new User();
        otherUser.setId(2L);
        address.setUser(otherUser);

        mockAuth();
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(addressRepository.findById(10L)).thenReturn(Optional.of(address));

        RuntimeException ex = assertThrows(RuntimeException.class, () -> addressService.selectAddress(10L));
        assertEquals("Unauthorized address selection", ex.getMessage());
    }
}