package com.baishnavi.usermanagement.repository;

import com.baishnavi.usermanagement.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/*
 * Repository layer
  This class is responsible for managing user data.
  Here we are using in-memory storage (List) instead of database.
 */
@Repository
public class UserRepository {

    // In-memory list to store users
    private List<User> userList = new ArrayList<>();


    // Constructor adding some dummy data for better testing
    public UserRepository() {
        userList.add(new User(1, "John Doe", "john.doe@gmail.com"));
        userList.add(new User(2, "Alice Smith", "alice.smith@gmail.com"));
        userList.add(new User(3, "Bob Johnson", "bob.johnson@gmail.com"));
        userList.add(new User(4, "Charlie Brown", "charlie.brown@gmail.com"));
        userList.add(new User(5, "David Miller", "david.miller@gmail.com"));
        userList.add(new User(6, "Emma Wilson", "emma.wilson@gmail.com"));
        userList.add(new User(7, "Sophia Taylor", "sophia.taylor@gmail.com"));
        userList.add(new User(8, "Liam Anderson", "liam.anderson@gmail.com"));
        userList.add(new User(9, "Olivia Thomas", "olivia.thomas@gmail.com"));
        userList.add(new User(10, "Noah Jackson", "noah.jackson@gmail.com"));
    }

    /*
     * Method to get all users
     */
    public List<User> findAll() {
        return userList;
    }

    /*
     * Method to save a new user
     */
    public User save(User user) {
        userList.add(user);
        return user;
    }

    /*
     * Method to find user by ID
     */
    public Optional<User> findById(int id) {
        return userList.stream()
                .filter(user -> user.getId() == id)
                .findFirst();
    }
}