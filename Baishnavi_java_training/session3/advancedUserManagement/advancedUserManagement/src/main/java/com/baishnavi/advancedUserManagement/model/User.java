package com.baishnavi.advancedUserManagement.model;

// This class represents a User in the system
public class User {

    private int id;
    private String name;
    private int age;
    private String role;

    // Constructor (important for object creation)
    public User(int id, String name, int age, String role) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.role = role;
    }

    // Getters (needed to access data)
    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public String getRole() {
        return role;
    }
}