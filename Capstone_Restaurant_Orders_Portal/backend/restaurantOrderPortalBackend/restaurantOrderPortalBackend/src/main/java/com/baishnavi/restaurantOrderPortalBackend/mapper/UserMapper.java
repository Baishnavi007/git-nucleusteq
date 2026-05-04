package com.baishnavi.restaurantOrderPortalBackend.mapper;

import com.baishnavi.restaurantOrderPortalBackend.dto.UserDTO;
import com.baishnavi.restaurantOrderPortalBackend.entity.User;

/**
 * Mapper class for converting User Entity <-> UserDTO.
 *

 */
public class UserMapper {

    /**
     * Converts User entity to UserDTO.
     *
     * @param user the User entity object
     * @return UserDTO containing only safe and required fields
     */
    public static UserDTO toDTO(User user) {

        if (user == null) {
            return null;
        }

        return new UserDTO(
                user.getId(),
                user.getFirstName(),
                user.getEmail(),
                user.getRole().name(),
                user.getWalletBalance()
        );
    }

    /**
     * Converts UserDTO to User entity.

     * @param dto the UserDTO object
     * @return User entity object
     */
    public static User toEntity(UserDTO dto) {

        if (dto == null) {
            return null;
        }

        User user = new User();
        user.setId(dto.getId());
        user.setFirstName(dto.getFirstName());
        user.setEmail(dto.getEmail());
        user.setWalletBalance(dto.getWalletBalance());

        return user;
    }
}