# 📝 TODO Application (Spring Boot)

A RESTful TODO management application built using **Spring Boot** following a clean layered architecture.  
This project demonstrates backend development concepts such as **DTO pattern, validation, logging, exception handling, external service simulation, and unit testing using Mockito**.

---

## 🚀 Tech Stack

- Java 17  
- Spring Boot  
- Spring Data JPA (Hibernate)  
- H2 In-Memory Database  
- Maven  
- JUnit 5  
- Mockito  
- SLF4J (Logging)  

---

## 📌 Key Features

### ✅ CRUD APIs
- Create TODO  
- Get All TODOs  
- Get TODO by ID  
- Update TODO  
- Delete TODO  

---

### ✅ Layered Architecture

The application follows a strict:
Controller → Service → Repository

- Controller handles HTTP requests  
- Service contains business logic  
- Repository interacts with database  


---

## 📌 Project Structure
java/session4/todo/

├── src/
│   ├── main/java/com/baishnavi/todo/
│   │   ├── TodoApplication.java              ← Entry point
│   │
│   │   ├── controller/
│   │   │   └── TodoController.java           ← REST API layer (CRUD endpoints + logging)
│   │
│   │   ├── service/
│   │   │   ├── TodoService.java              ← Interface (abstraction)
│   │   │   ├── TodoServiceImpl.java          ← Business logic + logging
│   │   │   └── NotificationServiceClient.java ← Simulated external service
│   │
│   │   ├── repository/
│   │   │   └── TodoRepository.java           ← JPA Repository (DB operations)
│   │
│   │   ├── entity/
│   │   │   └── Todo.java                     ← JPA Entity (maps to DB table)
│   │
│   │   ├── dto/
│   │   │   └── TodoDTO.java                  ← Request/Response model + validation
│   │
│   │   ├── exception/
│   │   │   ├── GlobalExceptionHandler.java   ← Handles all exceptions globally
│   │   │   ├── ResourceNotFoundException.java
│   │   │   ├── InvalidStatusException.java
│   │   │   └── InvalidStatusTransitionException.java
│   │
│   │   └── resources/
│   │       └── application.properties        ← App configuration (H2, etc.)
│
│   └── test/java/com/baishnavi/todo/service/
│       └── TodoServiceImplTest.java          ← Unit tests for service layer (4 tests)
│
└── pom.xml                                  ← Maven dependencies
---


### ✅ DTO Pattern

- Entity is **not exposed directly**  
- DTO used for request/response  
- Manual mapping implemented  

---

### ✅ Validation

- `@NotNull` → Title cannot be null  
- `@Size(min = 3)` → Minimum length validation  
- Applied using `@Valid`  

---

### ✅ Logging (SLF4J)

Logging implemented in:

- Controller layer (API logs)  
- Service layer (business logic logs)  

Example:

API call: Create Todo
Creating new Todo with title: Test Task
Todo created successfully with ID: 1
Notification sent: Notification sent for new TODO


---

### ✅ Exception Handling

Custom exceptions:

- ResourceNotFoundException  
- InvalidStatusException  
- InvalidStatusTransitionException  

Handled using:

- `@RestControllerAdvice (GlobalExceptionHandler)`

---

### ✅ External Service Simulation

- `NotificationServiceClient`  
- Simulates external API call  
- Triggered on TODO creation  

---

### ✅ Unit Testing (JUnit + Mockito)

Service layer tested using mocks.

#### ✔ Test Cases:
- createTodo()  
- getTodoById()  
- deleteTodo()  
- exception case (ID not found)  

---

## 🗄️ Database

- H2 In-Memory Database  
- No external DB required  

### Access Console:

---

# 📸 Screenshots

## 🔹 API Testing (Postman)

![Postman](screenshots/postman.png)

---

## 🔹 H2 Database

![H2](screenshots/h2.png)

---

## 🔹 Logs

![Logs](screenshots/logs.png)

---

## 🔹 Unit Tests

![Tests](screenshots/tests.png)

---

# 🧪 Sample API

### Create TODO


```json
{
  "title": "Learn Spring Boot",
  "description": "Practice project",
  "status": "PENDING"
}

🧠 Concepts Demonstrated
Inversion of Control (IoC)
Dependency Injection
Layered Architecture
DTO Pattern
Exception Handling
Logging
Unit Testing
📌 Notes
Lombok not used (manual implementation)
Clean architecture followed
No business logic in controller
In-memory DB used

👩‍💻 Author

Baishnavi Singh