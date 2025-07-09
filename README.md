# 📋 TaskTracker

A modern task management API built with FastAPI, PostgreSQL, and Docker. This application demonstrates best practices in software engineering, including clean architecture, comprehensive testing, and containerized deployment.

## 🚀 Features

- ✅ **Create new tasks** with title validation
- 📋 **List all tasks** with pagination and filtering
- ✅ **Mark tasks as completed**
- 🔄 **Update task details**
- 🗑️ **Delete tasks**
- 📊 **Get task statistics** (total, completed, pending)
- 🔍 **Filter tasks** by completion status
- 🏥 **Health check endpoints**
- 📚 **Automatic API documentation** (Swagger UI)

## 🏗️ Architecture

TaskTracker follows a **3-tier architecture**:

1. **Presentation Layer**: FastAPI REST endpoints
2. **Business Logic Layer**: CRUD operations and validation
3. **Data Layer**: PostgreSQL database with SQLAlchemy ORM

![Architecture Diagram](architecture_diagram.svg)

## 🛠️ Technology Stack

- **Backend**: FastAPI + Uvicorn
- **Database**: PostgreSQL + SQLAlchemy
- **Validation**: Pydantic
- **Containerization**: Docker + Docker Compose
- **Language**: Python 3.11

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/tasktracker.git
cd tasktracker
```

### 2. Environment Setup

Copy the environment file and customize if needed:

```bash
cp .env.example .env
```

### 3. Start the Application

```bash
# Start all services (database + API)
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 4. Access the Application

- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Base URL**: http://localhost:8000

## 📖 API Endpoints

### Health & Info

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/health` | Health check with database status |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all tasks (with pagination/filtering) |
| GET | `/tasks/{id}` | Get specific task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update an existing task |
| POST | `/tasks/{id}/complete` | Mark task as completed |
| DELETE | `/tasks/{id}` | Delete a task |

### Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/stats` | Get task statistics |

### Example API Usage

```bash
# Create a new task
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI"}'

# Get all tasks
curl -X GET "http://localhost:8000/tasks"

# Mark task as completed
curl -X POST "http://localhost:8000/tasks/1/complete"

# Get task statistics
curl -X GET "http://localhost:8000/tasks/stats"
```

## 🔧 Development Setup

### Local Development (without Docker)

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up local PostgreSQL** and update `.env` file

4. **Run the application**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Management

```bash
# Access database container
docker-compose exec db psql -U postgres -d tasktracker

# View database logs
docker-compose logs db

# Reset database (⚠️ destroys all data)
docker-compose down -v
docker-compose up -d
```

### Application Logs

```bash
# View application logs
docker-compose logs app

# Follow logs in real-time
docker-compose logs -f app

# View specific service logs
docker-compose logs db
```

## 🧪 Testing

### Run Tests (Coming Soon)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_crud.py
```

### Manual Testing with Swagger UI

1. Open http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in the parameters
4. Click "Execute" to test

## 📊 Monitoring

### Health Checks

The application includes comprehensive health checks:

- **Application Health**: `GET /health`
- **Database Connectivity**: Verified in health endpoint
- **Docker Health Checks**: Configured in docker-compose.yml

### Logs

Structured logging is implemented throughout the application:

```bash
# Application logs
docker-compose logs app

# Database logs
docker-compose logs db

# All logs
docker-compose logs
```

## 🔒 Security Considerations

- **Input Validation**: All inputs validated with Pydantic schemas
- **SQL Injection Prevention**: SQLAlchemy ORM used throughout
- **Non-root Container**: Application runs as non-root user
- **Environment Variables**: Sensitive data stored in environment variables
- **Network Isolation**: Services communicate via Docker network

## 📈 Performance

- **Async Support**: FastAPI's async capabilities utilized
- **Database Connection Pooling**: Configured in SQLAlchemy
- **Pagination**: Large result sets are paginated
- **Indexing**: Database indexes on frequently queried fields

## 🚀 Deployment

### Production Deployment

1. **Update environment variables** for production
2. **Use production database** credentials
3. **Configure reverse proxy** (nginx/Apache)
4. **Set up SSL/TLS** certificates
5. **Configure monitoring** and logging

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@db:5432/tasktracker` |
| `API_HOST` | API host binding | `0.0.0.0` |
| `API_PORT` | API port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `SECRET_KEY` | Application secret key | `your-secret-key-change-in-production` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you have any questions or need help:

1. Check the [documentation](http://localhost:8000/docs)
2. Review the [architecture guide](ARCHITECTURE.md)
3. Read the [best practices](BEST_PRACTICES.md)
4. Open an issue in the repository

## 🔄 Changelog

### v1.0.0 (2024-01-15)
- Initial release
- Core CRUD operations
- Docker containerization
- API documentation
- Health checks
