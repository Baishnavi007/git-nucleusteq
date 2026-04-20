📝 TODO Application (Spring Boot)

A RESTful TODO management application built using Spring Boot, following a clean layered architecture.
This project demonstrates backend development concepts such as DTO pattern, validation, logging, exception handling, external service simulation, and unit testing using Mockito.

---

🚀 Tech Stack
Java 17
Spring Boot
Spring Data JPA (Hibernate)
H2 In-Memory Database
Maven
JUnit 5
Mockito
SLF4J (Logging)

---

📌 Key Features
✅ CRUD APIs
Create TODO
Get All TODOs
Get TODO by ID
Update TODO
Delete TODO

--- 

✅ Layered Architecture
Controller → Service → Repository
Controller handles HTTP requests
Service contains business logic
Repository interacts with database

---

📁 Project Structure

![Alt text](Screenshots/projectstructure.png)
---

📌 Core Concepts

🔹 DTO Pattern
Entity is not exposed directly
DTO used for request/response
Manual mapping implemented

🔹 Validation
@NotNull → Title cannot be null
@Size(min = 3) → Minimum length validation
Applied using @Valid

🔹 Logging (SLF4J)
Logging implemented in:
Controller layer (API logs)
Service layer (business logic logs)

Example Logs:
![Alt text](Screenshots/logs.png)
API call: Create Todo
Creating new Todo with title: Test Task
Todo created successfully with ID: 1
Notification sent: Notification sent for new TODO


🔹 Exception Handling

Custom exceptions:

ResourceNotFoundException
InvalidStatusException
InvalidStatusTransitionException

Handled using:

@RestControllerAdvice (GlobalExceptionHandler)


🔹 Status Handling

Allowed values:

PENDING
COMPLETED

Valid transitions:

PENDING → COMPLETED
COMPLETED → PENDING

Invalid transitions throw:

InvalidStatusTransitionException


🔹 External Service Simulation

NotificationServiceClient
Simulates external API call
Triggered on TODO creation


🧪 Unit Testing

Testing is implemented using JUnit 5 + Mockito, covering both Controller and Service layers.

🔹 Test Summary

Controller	TodoControllerTest	5 Tests
Service	TodoServiceImplTest	6 Tests
Total	—	11 Tests

🔹 Controller Tests (TodoControllerTest)

Uses:

@WebMvcTest
MockMvc
Mocked TodoService
✔ Test Cases:
testCreateTodo()
testGetAllTodos()
testGetTodoById()
testUpdateTodo()
testDeleteTodo()


🔹 Service Tests (TodoServiceImplTest)

Uses:
Mockito (@Mock, @InjectMocks)
Repository mocked (no real DB)
✔ Test Cases:
testCreateTodo()
testGetTodoById()
testDeleteTodo()
testGetTodoByIdNotFound()
testUpdateTodo()
testDeleteTodoNotFound()


🔹 Testing Highlights

Mocking dependencies using Mockito
Isolated unit testing (no DB calls)
Covers success and failure scenarios
Verifies interactions using verify()

![Alt text](Screenshots/tests.png)

🗄️ Database
H2 In-Memory Database
No external DB setup required
![Alt text](Screenshots/h2.png)


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