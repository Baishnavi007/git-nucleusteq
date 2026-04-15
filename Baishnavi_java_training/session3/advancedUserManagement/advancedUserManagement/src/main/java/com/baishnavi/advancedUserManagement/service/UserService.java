package com.baishnavi.advancedUserManagement.service;

import com.baishnavi.advancedUserManagement.model.User;
import com.baishnavi.advancedUserManagement.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;

// Service layer: contains business logic
@Service
public class UserService {

    private final UserRepository userRepository;
    // Constructor Injection
    public UserService(UserRepository userRepository) {//Demonstrates IoC and DI
        this.userRepository = userRepository;
    }

    // Get all users
    public List<User> getAllUsers() {
        return userRepository.getAllUsers();
    }

    // Add user
    public void addUser(User user) {
        userRepository.addUser(user);
    }


    // Delete user
    public boolean deleteUser(int id) {
        return userRepository.deleteUser(id);
    }
}