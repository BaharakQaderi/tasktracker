# 🏗️ TaskTracker System Architecture

## 📋 Table of Contents
- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Component Details](#component-details)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)
- [Security Considerations](#security-considerations)
- [Scalability Considerations](#scalability-considerations)

## 🎯 System Overview

TaskTracker is a containerized web application built with a **3-tier architecture**:

1. **Presentation Layer**: REST API endpoints (FastAPI)
2. **Business Logic Layer**: CRUD operations and data validation
3. **Data Layer**: PostgreSQL database

## 🏛️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                         │
├─────────────────────────────────────────────────────────────┤
│  • Browser (Swagger UI)                                    │
│  • API Testing Tools (Postman, curl)                       │
│  • Frontend Applications                                   │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP/HTTPS Requests
                  │ (GET, POST, PUT, DELETE)
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    DOCKER COMPOSE                          │
│ ┌─────────────────────────┐ ┌─────────────────────────────┐ │
│ │    FASTAPI SERVICE      │ │    POSTGRESQL SERVICE      │ │
│ │    (Container: app)     │ │   (Container: database)    │ │
│ │                         │ │                             │ │
│ │ ┌─────────────────────┐ │ │ ┌─────────────────────────┐ │ │
│ │ │   PRESENTATION      │ │ │ │      DATA STORAGE       │ │ │
│ │ │     LAYER           │ │ │ │                         │ │ │
│ │ │ ┌─────────────────┐ │ │ │ │  ┌─────────────────┐    │ │ │
│ │ │ │  FastAPI Routes │ │ │ │ │  │   PostgreSQL    │    │ │ │
│ │ │ │  • GET /tasks   │ │ │ │ │  │     Database    │    │ │ │
│ │ │ │  • POST /tasks  │ │ │ │ │  │                 │    │ │ │
│ │ │ │  • POST /{id}/  │ │ │ │ │  │  Tables:        │    │ │ │
│ │ │ │    complete     │ │ │ │ │  │  - tasks        │    │ │ │
│ │ │ └─────────────────┘ │ │ │ │  │    * id (PK)    │    │ │ │
│ │ │                     │ │ │ │  │    * title      │    │ │ │
│ │ │ ┌─────────────────┐ │ │ │ │  │    * completed  │    │ │ │
│ │ │ │ Pydantic        │ │ │ │ │  └─────────────────┘    │ │ │
│ │ │ │ Schemas         │ │ │ │ │                         │ │ │
│ │ │ │ (Validation)    │ │ │ │ │  Port: 5432            │ │ │
│ │ │ └─────────────────┘ │ │ │ │  Volume: postgres_data  │ │ │
│ │ └─────────────────────┘ │ │ └─────────────────────────┘ │ │
│ │                         │ │                             │ │
│ │ ┌─────────────────────┐ │ │                             │ │
│ │ │   BUSINESS LOGIC    │ │ │                             │ │
│ │ │      LAYER          │ │ │                             │ │
│ │ │ ┌─────────────────┐ │ │ │                             │ │
│ │ │ │ CRUD Operations │ │ │ │                             │ │
│ │ │ │ • create_task() │ │ │ │                             │ │
│ │ │ │ • get_tasks()   │ │ │ │                             │ │
│ │ │ │ • complete_task │ │ │ │                             │ │
│ │ │ └─────────────────┘ │ │ │                             │ │
│ │ │                     │ │ │                             │ │
│ │ │ ┌─────────────────┐ │ │ │                             │ │
│ │ │ │ SQLAlchemy ORM  │ │ │ │                             │ │
│ │ │ │ Models & Session│ │ │ │                             │ │
│ │ │ └─────────────────┘ │ │ │                             │ │
│ │ └─────────────────────┘ │ │                             │ │
│ │                         │ │                             │ │
│ │ Port: 8000              │ │                             │ │
│ │ Network: tasktracker_net│ │ Network: tasktracker_net    │ │
│ └─────────────────────────┘ └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Component Details

### **1. FastAPI Application Container**
```
app/
├── main.py          # Entry point, FastAPI instance, route definitions
├── models.py        # SQLAlchemy ORM models (Task model)
├── schemas.py       # Pydantic models for request/response validation
├── crud.py          # Database operations (Create, Read, Update, Delete)
└── database.py      # Database configuration, session management
```

**Responsibilities**:
- Handle HTTP requests/responses
- Input validation and serialization
- Business logic execution
- Database interactions through ORM

### **2. PostgreSQL Database Container**
**Responsibilities**:
- Data persistence
- ACID transactions
- Data integrity constraints
- Concurrent access handling

### **3. Docker Compose Orchestration**
**Responsibilities**:
- Service orchestration
- Network management
- Volume management
- Environment configuration

## 🔄 Data Flow

### **Creating a Task (POST /tasks)**
```
1. Client sends HTTP POST request with task data
2. FastAPI receives request
3. Pydantic schema validates input data
4. CRUD function creates new task in database
5. SQLAlchemy ORM executes INSERT SQL
6. PostgreSQL stores data and returns task ID
7. Response flows back through layers to client
```

### **Listing Tasks (GET /tasks)**
```
1. Client sends HTTP GET request
2. FastAPI processes request
3. CRUD function queries all tasks
4. SQLAlchemy ORM executes SELECT SQL
5. PostgreSQL returns task data
6. Pydantic schema serializes response
7. JSON response sent to client
```

### **Completing a Task (POST /tasks/{id}/complete)**
```
1. Client sends HTTP POST with task ID
2. FastAPI extracts ID from path parameter
3. CRUD function updates task completion status
4. SQLAlchemy ORM executes UPDATE SQL
5. PostgreSQL updates record
6. Success response returned to client
```

## 🛠️ Technology Stack

### **Backend Framework**
- **FastAPI**: Modern, fast web framework for Python APIs
- **Uvicorn**: ASGI server for running FastAPI

### **Database**
- **PostgreSQL**: Robust, ACID-compliant relational database
- **SQLAlchemy**: Python ORM for database interactions
- **psycopg2**: PostgreSQL adapter for Python

### **Data Validation**
- **Pydantic**: Data validation using Python type hints

### **Containerization**
- **Docker**: Application containerization
- **Docker Compose**: Multi-container orchestration

## 🏗️ Design Patterns

### **1. Repository Pattern**
- `crud.py` acts as repository layer
- Separates business logic from data access
- Makes testing easier with mock repositories

### **2. Dependency Injection**
- Database sessions injected into route handlers
- Promotes loose coupling and testability

### **3. MVC-like Structure**
- **Controllers**: FastAPI route handlers (`main.py`)
- **Models**: SQLAlchemy models (`models.py`)
- **Views**: JSON responses via Pydantic schemas

### **4. Single Responsibility Principle**
- Each module has one clear purpose
- Easy to maintain and extend

## 🔒 Security Considerations

### **Input Validation**
- Pydantic schemas validate all input data
- Type checking prevents injection attacks
- Request size limits prevent DoS

### **Database Security**
- SQLAlchemy ORM prevents SQL injection
- Database credentials in environment variables
- Database not exposed to host network

### **Container Security**
- Non-root user in containers
- Minimal base images
- Network isolation between containers

## 📈 Scalability Considerations

### **Current Architecture**
- Single instance design
- Suitable for development and small deployments

### **Future Enhancements**
- **Horizontal Scaling**: Multiple FastAPI instances behind load balancer
- **Database Scaling**: Read replicas, connection pooling
- **Caching**: Redis for frequently accessed data
- **API Gateway**: Rate limiting, authentication
- **Monitoring**: Logging, metrics, health checks

## 🧪 Testing Strategy

### **Unit Testing**
- Test CRUD functions in isolation
- Mock database dependencies
- Test Pydantic schema validation

### **Integration Testing**
- Test API endpoints with test database
- Verify database interactions
- Test complete request/response cycle

### **Container Testing**
- Test Docker build process
- Verify container networking
- Test environment variable configuration

## 📊 Performance Considerations

### **Database Optimization**
- Proper indexing on frequently queried fields
- Connection pooling for concurrent requests
- Query optimization using SQLAlchemy

### **API Performance**
- Async/await for non-blocking operations
- Response compression
- Proper HTTP status codes and caching headers

---

## 🚀 Next Steps

After understanding this architecture:

1. **Review and understand each component**
2. **Create the project structure**
3. **Implement components layer by layer**
4. **Test each layer independently**
5. **Integration testing**
6. **Container deployment**

This architecture follows **software engineering best practices**:
- ✅ Separation of concerns
- ✅ Single responsibility principle
- ✅ Dependency injection
- ✅ Layered architecture
- ✅ Containerization
- ✅ Environment-based configuration
- ✅ Input validation and error handling
