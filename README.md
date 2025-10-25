# To-Do App

A full-stack To-Do application built with React, Flask, and MySQL.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/BoshithaMGunarathna/To-Do-App.git
   cd To-Do-App
   ```

2. **Start the application**
   ```bash
   docker compose up -d
   ```

3. **Access the application**
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:5000
   - **phpMyAdmin**: http://localhost:8081
     - Username: `root`
     - Password: `root`

## Available Commands

### Start all services
```bash
docker compose up -d
```

### Stop all services
```bash
docker compose down
```

### Rebuild after code changes
```bash
docker compose up -d --build
```

### View logs
```bash
# All services
docker compose logs

# Specific service
docker compose logs backend
docker compose logs frontend
docker compose logs mysql_db
```

### Restart a specific service
```bash
docker compose restart backend
docker compose restart frontend
```

## Project Structure

```
To-Do-App/
├── backend/
│   ├── app.py              # Flask API
│   ├── requirements.txt    # Python dependencies
│   ├── init.sql           # Database initialization
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx        # Main React component
│   │   └── TaskList.tsx   # Task list component
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml      # Docker orchestration
```

## Technology Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: Flask (Python)
- **Database**: MySQL 8
- **Admin Panel**: phpMyAdmin
- **Containerization**: Docker

## Database

The MySQL database is automatically initialized with:
- Database name: `todo_db`
- Table: `task` with sample data
- Credentials: root/root

## Troubleshooting

### Ports already in use
If you see port conflicts, make sure no other services (like XAMPP) are using ports:
- 3306 (MySQL)
- 5000 (Backend)
- 5173 (Frontend)
- 8081 (phpMyAdmin)

### Reset everything
```bash
docker compose down -v  # Remove containers and volumes
docker compose up -d    # Start fresh
```

## Development

### Backend Development
The backend uses Flask. To add new endpoints, edit `backend/app.py`.

### Frontend Development
The frontend uses React with Vite. Hot reload is enabled by default.

### Database Changes
To modify the database schema, edit `backend/init.sql` and rebuild:
```bash
docker compose down -v
docker compose up -d --build
```

