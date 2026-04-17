package com.baishnavi.todo.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

// Represents a Todo task in the system
@Entity
@Table(name = "todos")
public class Todo {

    // Primary key
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Title of the task
    private String title;

    // Description of the task
    private String description;

    // Status of the task (PENDING / COMPLETED)
    @Enumerated(EnumType.STRING)
    private Status status;

    // Timestamp when task is created
    private LocalDateTime createdAt;

    // Enum for task status
    public enum Status {
        PENDING,
        COMPLETED
    }

    // Default constructor
    public Todo() {
    }

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }


    public void setDescription(String description) {
        this.description = description;
    }

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }


    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}