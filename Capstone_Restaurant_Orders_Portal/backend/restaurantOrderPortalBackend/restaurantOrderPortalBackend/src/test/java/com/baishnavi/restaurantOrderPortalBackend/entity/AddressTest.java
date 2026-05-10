package com.baishnavi.restaurantOrderPortalBackend.entity;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AddressTest {

    private Address address;
    private User user;

    @BeforeEach
    void setUp() {
        user = new User();
        user.setId(1L);
        address = new Address(1L, "123 Main St", "Pune", "Maharashtra", "411001", true, user);
    }

    @Test
    void testGettersAndSetters() {
        Address emptyAddress = new Address();
        emptyAddress.setId(2L);
        emptyAddress.setStreet("456 Park Ave");
        emptyAddress.setCity("Mumbai");
        emptyAddress.setState("Maharashtra");
        emptyAddress.setPincode("400001");
        emptyAddress.setIsDefault(false);

        User newUser = new User();
        newUser.setId(2L);
        emptyAddress.setUser(newUser);

        assertEquals(2L, emptyAddress.getId());
        assertEquals("456 Park Ave", emptyAddress.getStreet());
        assertEquals("Mumbai", emptyAddress.getCity());
        assertEquals("Maharashtra", emptyAddress.getState());
        assertEquals("400001", emptyAddress.getPincode());
        assertFalse(emptyAddress.getIsDefault());
        assertEquals(newUser, emptyAddress.getUser());
    }

    @Test
    void testAllArgsConstructor() {
        assertEquals(1L, address.getId());
        assertEquals("123 Main St", address.getStreet());
        assertEquals("Pune", address.getCity());
        assertEquals("Maharashtra", address.getState());
        assertEquals("411001", address.getPincode());
        assertTrue(address.getIsDefault());
        assertEquals(user, address.getUser());
    }

    @Test
    void testEqualsAndHashCode() {
        Address address1 = new Address();
        address1.setId(1L);

        Address address2 = new Address();
        address2.setId(1L);

        Address address3 = new Address();
        address3.setId(2L);

        assertEquals(address1, address1);
        assertEquals(address1, address2);
        assertNotEquals(address1, address3);
        assertNotEquals(address1, null);
        assertNotEquals(address1, new Object());

        assertEquals(address1.hashCode(), address2.hashCode());
        assertNotEquals(address1.hashCode(), address3.hashCode());
    }

    @Test
    void testToString() {
        String expected = "Address{id=1, city='Pune', state='Maharashtra', pincode='411001', isDefault=true}";
        assertEquals(expected, address.toString());
    }
}