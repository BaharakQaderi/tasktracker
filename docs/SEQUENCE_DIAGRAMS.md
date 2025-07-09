# 🔄 TaskTracker Sequence Diagrams

## 📋 API Interaction Flows

### 1. Create Task Flow
```
Client          FastAPI         CRUD            SQLAlchemy      PostgreSQL
  │                │              │                 │              │
  │ POST /tasks    │              │                 │              │
  ├───────────────>│              │                 │              │
  │                │              │                 │              │
  │                │ validate     │                 │              │
  │                │ request      │                 │              │
  │                │ (Pydantic)   │                 │              │
  │                │              │                 │              │
  │                │ create_task()│                 │              │
  │                ├─────────────>│                 │              │
  │                │              │                 │              │
  │                │              │ db.add(task)    │              │
  │                │              ├────────────────>│              │
  │                │              │                 │              │
  │                │              │                 │ INSERT INTO  │
  │                │              │                 │ tasks...     │
  │                │              │                 ├─────────────>│
  │                │              │                 │              │
  │                │              │                 │ task_id      │
  │                │              │                 │<─────────────┤
  │                │              │                 │              │
  │                │              │ task_obj        │              │
  │                │              │<────────────────┤              │
  │                │              │                 │              │
  │                │ task_response│                 │              │
  │                │<─────────────┤                 │              │
  │                │              │                 │              │
  │ 201 Created    │              │                 │              │
  │ {task_data}    │              │                 │              │
  │<───────────────┤              │                 │              │
```

### 2. Get All Tasks Flow
```
Client          FastAPI         CRUD            SQLAlchemy      PostgreSQL
  │                │              │                 │              │
  │ GET /tasks     │              │                 │              │
  ├───────────────>│              │                 │              │
  │                │              │                 │              │
  │                │ get_tasks()  │                 │              │
  │                ├─────────────>│                 │              │
  │                │              │                 │              │
  │                │              │ db.query(Task)  │              │
  │                │              ├────────────────>│              │
  │                │              │                 │              │
  │                │              │                 │ SELECT *     │
  │                │              │                 │ FROM tasks   │
  │                │              │                 ├─────────────>│
  │                │              │                 │              │
  │                │              │                 │ task_rows[]  │
  │                │              │                 │<─────────────┤
  │                │              │                 │              │
  │                │              │ tasks_list[]    │              │
  │                │              │<────────────────┤              │
  │                │              │                 │              │
  │                │ tasks_response                 │              │
  │                │<─────────────┤                 │              │
  │                │              │                 │              │
  │ 200 OK         │              │                 │              │
  │ [tasks_array]  │              │                 │              │
  │<───────────────┤              │                 │              │
```

### 3. Complete Task Flow
```
Client          FastAPI         CRUD            SQLAlchemy      PostgreSQL
  │                │              │                 │              │
  │ POST /tasks/   │              │                 │              │
  │ {id}/complete  │              │                 │              │
  ├───────────────>│              │                 │              │
  │                │              │                 │              │
  │                │ validate     │                 │              │
  │                │ task_id      │                 │              │
  │                │              │                 │              │
  │                │ complete_    │                 │              │
  │                │ task(id)     │                 │              │
  │                ├─────────────>│                 │              │
  │                │              │                 │              │
  │                │              │ db.query(Task)  │              │
  │                │              │ .filter(id)     │              │
  │                │              ├────────────────>│              │
  │                │              │                 │              │
  │                │              │                 │ SELECT *     │
  │                │              │                 │ FROM tasks   │
  │                │              │                 │ WHERE id=?   │
  │                │              │                 ├─────────────>│
  │                │              │                 │              │
  │                │              │                 │ task_row     │
  │                │              │                 │<─────────────┤
  │                │              │                 │              │
  │                │              │ task_obj        │              │
  │                │              │<────────────────┤              │
  │                │              │                 │              │
  │                │              │ task.completed  │              │
  │                │              │ = True          │              │
  │                │              │                 │              │
  │                │              │ db.commit()     │              │
  │                │              ├────────────────>│              │
  │                │              │                 │              │
  │                │              │                 │ UPDATE tasks │
  │                │              │                 │ SET completed│
  │                │              │                 │ = true...    │
  │                │              │                 ├─────────────>│
  │                │              │                 │              │
  │                │              │                 │ success      │
  │                │              │                 │<─────────────┤
  │                │              │                 │              │
  │                │              │ updated_task    │              │
  │                │              │<────────────────┤              │
  │                │              │                 │              │
  │                │ task_response│                 │              │
  │                │<─────────────┤                 │              │
  │                │              │                 │              │
  │ 200 OK         │              │                 │              │
  │ {updated_task} │              │                 │              │
  │<───────────────┤              │                 │              │
```

## 🏗️ System Startup Sequence

### Docker Compose Startup
```
Docker Compose   PostgreSQL      FastAPI App     Health Check
      │              │               │               │
      │ docker-      │               │               │
      │ compose up   │               │               │
      │              │               │               │
      │ start        │               │               │
      │ postgres     │               │               │
      ├─────────────>│               │               │
      │              │               │               │
      │              │ initialize    │               │
      │              │ database      │               │
      │              │               │               │
      │              │ ready         │               │
      │              │<──────────────│               │
      │              │               │               │
      │ start        │               │               │
      │ fastapi      │               │               │
      ├──────────────┼──────────────>│               │
      │              │               │               │
      │              │               │ connect to    │
      │              │               │ database      │
      │              │               ├──────────────>│
      │              │               │               │
      │              │               │ connection    │
      │              │               │ successful    │
      │              │               │<──────────────┤
      │              │               │               │
      │              │               │ start server  │
      │              │               │ port 8000     │
      │              │               │               │
      │              │               │ health check  │
      │              │               ├──────────────>│
      │              │               │               │
      │              │               │ 200 OK        │
      │              │               │<──────────────┤
      │              │               │               │
      │ system       │               │               │
      │ ready        │               │               │
```

## 🔄 Error Handling Flow

### Database Connection Error
```
FastAPI App     Database        Error Handler   Client
     │              │                │            │
     │ attempt      │                │            │
     │ connection   │                │            │
     ├─────────────>│                │            │
     │              │                │            │
     │              │ connection     │            │
     │              │ timeout        │            │
     │              │<───────────────│            │
     │              │                │            │
     │ ConnectionError              │            │
     │<─────────────┤                │            │
     │              │                │            │
     │ log error    │                │            │
     │              │                │            │
     │ trigger      │                │            │
     │ exception    │                │            │
     │ handler      │                │            │
     ├──────────────┼───────────────>│            │
     │              │                │            │
     │              │                │ format     │
     │              │                │ error      │
     │              │                │ response   │
     │              │                │            │
     │              │                │ 503 Service│
     │              │                │ Unavailable│
     │              │                ├───────────>│
     │              │                │            │
     │              │                │ retry      │
     │              │                │ mechanism  │
```

## 🧪 Testing Flow

### Unit Test Execution
```
Test Runner     Mock Database   CRUD Function   Test Assertion
     │              │               │               │
     │ setup test   │               │               │
     │ environment  │               │               │
     │              │               │               │
     │ create mock  │               │               │
     │ database     │               │               │
     ├─────────────>│               │               │
     │              │               │               │
     │              │ mock ready    │               │
     │              │<──────────────│               │
     │              │               │               │
     │ call         │               │               │
     │ create_task()│               │               │
     ├──────────────┼──────────────>│               │
     │              │               │               │
     │              │               │ execute       │
     │              │               │ with mock     │
     │              │               ├──────────────>│
     │              │               │               │
     │              │               │ return        │
     │              │               │ mock data     │
     │              │               │<──────────────┤
     │              │               │               │
     │              │               │ task object   │
     │              │<──────────────┤               │
     │              │               │               │
     │ verify       │               │               │
     │ result       │               │               │
     ├──────────────┼───────────────┼──────────────>│
     │              │               │               │
     │              │               │               │ assert
     │              │               │               │ task.id == 1
     │              │               │               │ assert
     │              │               │               │ task.title
     │              │               │               │ == "Test"
```

---

These sequence diagrams help you understand:

1. **🔄 Data Flow**: How data moves through the system
2. **🏗️ Component Interaction**: How each layer communicates
3. **⚡ Timing**: When each operation happens
4. **🚨 Error Handling**: How errors are caught and handled
5. **🧪 Testing**: How to test each component in isolation

This gives you a **complete picture** of the system before you start coding!
