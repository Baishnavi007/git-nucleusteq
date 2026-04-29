package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.Address;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Repository for Address entity
 */
public interface AddressRepository extends JpaRepository<Address, Long> {
}