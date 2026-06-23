package com.baishnavi.restaurantOrderPortalBackend.repository;

import com.baishnavi.restaurantOrderPortalBackend.entity.Cart;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/**
 * Repository for Cart entity
 */
public interface CartRepository extends JpaRepository<Cart, Long> {

    /**
     * Find cart by user
     *
     * @param user user entity
     * @return optional cart
     */
    Optional<Cart> findByUser(User user);
}