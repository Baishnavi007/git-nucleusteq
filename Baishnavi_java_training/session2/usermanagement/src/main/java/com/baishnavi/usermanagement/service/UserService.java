package com.baishnavi.usermanagement.service;

import com.baishnavi.usermanagement.model.User;
import com.baishnavi.usermanagement.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;

// Service Layer: Contains the business logic
@Service
public class UserService {


    private final UserRepository userRepository;
    // used final so that the reference can not be changed after the initialisation.

     //Constructor Injection: Spring will automatically inject UserRepository here

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }



    // To get all the existing users
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

   // Creating a new user
    public User createUser(User user) {
        return userRepository.save(user);
    }

    // Get user by id
    public User getUserById(int id) {

        // Handling the case when user is not found
        return userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found with id: " + id));
    }
}