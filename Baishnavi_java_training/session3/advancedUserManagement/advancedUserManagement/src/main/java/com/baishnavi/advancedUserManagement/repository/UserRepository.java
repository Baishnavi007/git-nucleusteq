package com.baishnavi.advancedUserManagement.repository;

import com.baishnavi.advancedUserManagement.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

// This class acts like a database (in-memory storage)
@Repository
public class UserRepository {
    private final List<User> users = new ArrayList<>();

    // Constructor: to initialize dummy data
    public UserRepository() {
        users.add(new User(1, "Priya", 25, "USER"));
        users.add(new User(2, "Rahul", 30, "ADMIN"));
        users.add(new User(3, "Amit", 30, "USER"));
        users.add(new User(4, "Neha", 28, "USER"));
        users.add(new User(5, "Ravi", 35, "ADMIN"));
    }


    // Return all users
    public List<User> getAllUsers() {
        return users;
    }

    // To add new user
    public void addUser(User user) {
        users.add(user);
    }
    // To delete user by id
    public boolean deleteUser(int id) {
        return users.removeIf(user -> user.getId() == id);
    }
}