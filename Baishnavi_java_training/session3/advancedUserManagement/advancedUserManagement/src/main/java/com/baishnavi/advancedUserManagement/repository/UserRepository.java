package com.baishnavi.advancedUserManagement.repository;

import com.baishnavi.advancedUserManagement.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

// This class acts like a database (in-memory storage)
@Repository
public class UserRepository {
    private final List<User> users = new ArrayList<>();

    // Auto-increment counter
    private int nextId = 1;

    // Constructor: to initialize dummy data
    public UserRepository() {

        addUser(new User("Priya", 25, "USER"));
        addUser(new User("Rahul", 30, "ADMIN"));
        addUser(new User("Amit", 30, "USER"));
        addUser(new User("Neha", 28, "USER"));
        addUser(new User("Ravi", 35, "ADMIN"));

        addUser(new User("Karan", 27, "USER"));
        addUser(new User("Simran", 24, "USER"));
        addUser(new User("Arjun", 29, "ADMIN"));
        addUser(new User("Sneha", 26, "USER"));
        addUser(new User("Vikram", 32, "ADMIN"));
        addUser(new User("Anjali", 23, "USER"));
        addUser(new User("Rohit", 31, "ADMIN"));
        addUser(new User("Pooja", 27, "USER"));
        addUser(new User("Suresh", 40, "ADMIN"));
        addUser(new User("Meena", 22, "USER"));
    }

    // Return all users
    public List<User> getAllUsers() {
        return users;
    }

    // To add new user
    public void addUser(User user) {

        User newUser = new User(
                nextId++,
                user.getName(),
                user.getAge(),
                user.getRole()
        );

        users.add(newUser);
    }

    // To delete user by id
    public boolean deleteUser(int id) {
        return users.removeIf(user -> user.getId() == id);
    }
}