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
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // Get all users
    public List<User> getAllUsers() {
        return userRepository.getAllUsers();
    }

    // Search users based on optional filters
    public List<User> searchUsers(String name, Integer age, String role) {

        List<User> users = userRepository.getAllUsers();
        return users.stream()
                .filter(user ->
                        (name == null || user.getName().equalsIgnoreCase(name)) &&
                                (age == null || user.getAge() == age) &&
                                (role == null || user.getRole().equalsIgnoreCase(role))
                )
                .toList(); //Converts the filtered stream into a List
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