package com.baishnavi.restaurantOrderPortalBackend.entity;

import com.baishnavi.restaurantOrderPortalBackend.enums.Role;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class UserTest {

    private User user;
    private LocalDateTime now;

    @BeforeEach
    void setUp() {
        now = LocalDateTime.now();
        user = new User(1L, "John", "Doe", "1234567890", "john@example.com", "password", Role.USER, 100.0, now, new ArrayList<>(), 10L);
    }

    @Test
    void testGettersAndSetters() {
        User emptyUser = new User();
        emptyUser.setId(2L);
        emptyUser.setFirstName("Jane");
        emptyUser.setLastName("Smith");
        emptyUser.setPhoneNumber("0987654321");
        emptyUser.setEmail("jane@example.com");
        emptyUser.setPassword("newpass");
        emptyUser.setRole(Role.RESTAURANT_OWNER);
        emptyUser.setWalletBalance(200.0);
        emptyUser.setCreatedAt(now);

        List<Address> addresses = new ArrayList<>();
        emptyUser.setAddresses(addresses);
        emptyUser.setSelectedAddressId(20L);

        assertEquals(2L, emptyUser.getId());
        assertEquals("Jane", emptyUser.getFirstName());
        assertEquals("Smith", emptyUser.getLastName());
        assertEquals("0987654321", emptyUser.getPhoneNumber());
        assertEquals("jane@example.com", emptyUser.getEmail());
        assertEquals("newpass", emptyUser.getPassword());
        assertEquals(Role.RESTAURANT_OWNER, emptyUser.getRole());
        assertEquals(200.0, emptyUser.getWalletBalance());
        assertEquals(now, emptyUser.getCreatedAt());
        assertEquals(addresses, emptyUser.getAddresses());
        assertEquals(20L, emptyUser.getSelectedAddressId());
    }

    @Test
    void testAllArgsConstructor() {
        assertEquals(1L, user.getId());
        assertEquals("John", user.getFirstName());
        assertEquals("Doe", user.getLastName());
        assertEquals("1234567890", user.getPhoneNumber());
        assertEquals("john@example.com", user.getEmail());
        assertEquals("password", user.getPassword());
        assertEquals(Role.USER, user.getRole());
        assertEquals(100.0, user.getWalletBalance());
        assertEquals(now, user.getCreatedAt());
        assertNotNull(user.getAddresses());
        assertEquals(10L, user.getSelectedAddressId());
    }

    @Test
    void testEqualsAndHashCode() {
        User user1 = new User();
        user1.setId(1L);

        User user2 = new User();
        user2.setId(1L);

        User user3 = new User();
        user3.setId(2L);

        assertEquals(user1, user1);
        assertEquals(user1, user2);
        assertNotEquals(user1, user3);
        assertNotEquals(user1, null);
        assertNotEquals(user1, new Object());

        assertEquals(user1.hashCode(), user2.hashCode());
        assertNotEquals(user1.hashCode(), user3.hashCode());
    }

    @Test
    void testToString() {
        String expected = "User{id=1, firstName='John', email='john@example.com', role=USER, walletBalance=100.0}";
        assertEquals(expected, user.toString());
    }
}