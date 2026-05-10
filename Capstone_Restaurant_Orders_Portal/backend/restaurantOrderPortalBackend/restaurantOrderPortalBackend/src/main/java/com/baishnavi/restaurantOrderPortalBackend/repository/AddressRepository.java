package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.Address;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * Repository for Address entity
 */
public interface AddressRepository extends JpaRepository<Address, Long> {
    List<Address> findByUser(User user);
}