package com.baishnavi.todo.repository;

import com.baishnavi.todo.entity.Todo;
import org.springframework.data.jpa.repository.JpaRepository;

// Repository interface for Todo entity
public interface TodoRepository extends JpaRepository<Todo, Long> {
}