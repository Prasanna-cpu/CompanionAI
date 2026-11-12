# 🤖 CompanionAI – Multi-Agent AI Email Assistant

CompanionAI is an AI-powered email assistant built using **Python, FastAPI, LangChain, and LangGraph**. It uses a multi-agent architecture to automate email-related tasks by coordinating specialized AI agents through a supervisor.

The application enables users to generate email content, retrieve unread emails, research information, and send emails through natural language instructions.

It integrates LLM-powered tool calling, Gmail IMAP, SMTP-based email delivery, PostgreSQL persistence, and Docker-based deployment.

## 🚀 Key Features

### 🧠 Multi-Agent Architecture
- Implemented a supervisor-based multi-agent architecture using LangGraph.
- Specialized Email Agent for managing email-related operations.
- Research Agent for gathering information and preparing email content.
- Supervisor dynamically coordinates agents and delegates tasks based on user instructions.
- Tool calling enables agents to interact with external email services.

### ✉️ Intelligent Email Management
- Generate email subjects and message content using LLMs.
- Retrieve unread emails from the inbox.
- Filter unread emails based on a configurable time window.
- Send emails through SMTP with SSL encryption.
- Execute email operations through natural language instructions.

### 🔗 LLM Integration
- Integrated LangChain with OpenAI-compatible chat model APIs.
- Configurable model selection and API base URL.
- Tool binding for connecting LLMs with application functions.
- Structured AI responses using Pydantic schemas.
- Configurable model temperature and token limits.

### 🗄️ Database Persistence
- PostgreSQL integration using SQLModel.
- Persistent storage of chat messages.
- UUID-based identifiers for chat records.
- Automatic database initialization during application startup.
- SQLModel sessions for database operations.

### ⚡ API Development
- RESTful API development using FastAPI.
- Pydantic-based request and response validation.
- Dependency injection for database sessions.
- Dedicated endpoints for chat creation and recent chat retrieval.
- HTTP exception handling for AI service failures.

### 🐳 Containerization & Deployment
- Dockerized FastAPI application.
- Docker Compose orchestration for application and PostgreSQL services.
- Persistent PostgreSQL storage using Docker volumes.
- Railway deployment configuration.
- Environment-based application configuration.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.14 |
| Backend Framework | FastAPI |
| AI Framework | LangChain |
| Multi-Agent Orchestration | LangGraph Supervisor |
| LLM Integration | LangChain OpenAI |
| Database | PostgreSQL 17 |
| ORM | SQLModel |
| Data Validation | Pydantic |
| Email Retrieval | Gmail IMAP |
| Email Delivery | SMTP, smtplib |
| Server | Uvicorn |
| Containerization | Docker, Docker Compose |
| Package Management | uv, pip |
| Deployment | Railway |

## 🏗️ Architecture Overview

CompanionAI uses a supervisor-based multi-agent architecture in which a central supervisor coordinates specialized agents to execute email-related tasks.

### Multi-Agent Workflow

```text
                    User
                      |
                      v
               FastAPI Backend
                      |
                      v
                 Chat API
                      |
                      v
               Supervisor Agent
                      |
              +-------+-------+
              |               |
              v               v
         Email Agent      Research Agent
              |               |
       +------+------+        |
       |      |      |        |
       v      v      v        v
     Send   Retrieve Research Generate
     Email  Emails   Email    Content
       |      |      |        |
       v      v      +--------+
     SMTP   Gmail IMAP
              |
              v
         PostgreSQL
       (Chat History)
```

### Agent Responsibilities

**1. Supervisor Agent**

- Receives user instructions through the chat API.
- Coordinates specialized agents.
- Delegates tasks to the appropriate agent.
- Combines agent outputs into a final response.

**2. Email Agent**

- Handles email-related operations.
- Retrieves unread emails.
- Sends emails through SMTP.
- Uses registered tools to interact with email services.

**3. Research Agent**

- Processes research requests.
- Generates relevant email content using an LLM.
- Prepares email subjects and message bodies.

## 🔄 Application Workflow

1. The user submits a natural language instruction through the chat API.
2. FastAPI validates the request and persists the incoming chat message in PostgreSQL.
3. The supervisor agent receives the user's instruction.
4. The supervisor delegates tasks to the Email Agent or Research Agent.
5. Agents invoke their registered tools to retrieve emails, generate content, or send messages.
6. The supervisor collects the agent's response.
7. The API returns the generated response to the client.

## 📂 Project Structure

```text
CompanionAI/
│
├── src/
│   ├── main.py
│   │
│   └── api/
│       ├── db.py
│       │
│       ├── chat/
│       │   ├── routing.py
│       │   └── models.py
│       │
│       ├── ai/
│       │   ├── agents.py
│       │   ├── tools.py
│       │   ├── services.py
│       │   ├── schemas.py
│       │   └── llms.py
│       │
│       └── email/
│           ├── sender.py
│           ├── inbox_reader.py
│           └── imap_parser.py
│
├── static_html/              # Static frontend assets
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── railway.json
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.14+
- Docker and Docker Compose
- OpenAI API key or compatible LLM provider credentials
- Gmail account with an appropriately configured app password, if using Gmail
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Prasanna-cpu/CompanionAI.git

cd CompanionAI
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Application
ENVIRONMENT=development
DEBUG=True

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DATABASE=companionai
POSTGRES_URL=postgresql://postgres:your_password@db_service:5432/companionai

# LLM Configuration
OPENAI_API_KEY=your_api_key
OPENAI_MODEL_NAME=your_model_name
OPENAI_BASE_URL=https://api.openai.com/v1

# Email Configuration
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
```

**Important:**
- Never commit `.env` files or API credentials to GitHub.
- Use a Gmail App Password where supported instead of your regular account password.
- Configure the correct LLM provider endpoint and model name.
- For local execution outside Docker, change the database hostname from `db_service` to `localhost` and use the mapped PostgreSQL port.

### 3. Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

Alternatively, using uv:

```bash
uv sync
```

### 4. Start the Application Using Docker Compose

Build and start the containers:

```bash
docker compose up --build
```

The application and PostgreSQL database will start through Docker Compose.

The FastAPI application is configured to run on port:

```text
http://localhost:8080
```

### 5. Access API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://localhost:8080/docs
```

ReDoc:

```text
http://localhost:8080/redoc
```

### 6. Run Without Docker

Start the FastAPI application:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
```

Ensure PostgreSQL is running and the environment variables are configured correctly.

## 📡 API Endpoints

The following endpoints are implemented in the chat router.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application health/basic information |
| GET | `/user` | Returns basic user information |
| GET | `/api/chats/` | Chat API health check |
| POST | `/api/chats/create` | Creates a chat message and invokes the AI supervisor |
| GET | `/api/chats/recent` | Retrieves the 10 most recent chat messages |

### Create Chat Message

**Endpoint:**

```http
POST /api/chats/create
```

Request:

```json
{
  "message": "Research a topic and prepare an email about it."
}
```

Response:

```json
{
  "content": "Generated response from the AI supervisor."
}
```

### Retrieve Recent Conversations

**Endpoint:**

```http
GET /api/chats/recent
```

Returns the 10 most recent persisted chat messages, ordered by creation time.

## 🗄️ Database Design

CompanionAI uses PostgreSQL with SQLModel for relational data persistence.

### ChatMessage

| Field | Type | Description |
|---|---|---|
| id | String (UUID) | Unique chat message identifier |
| message | String | User-submitted message |
| created_at | DateTime | Message creation timestamp |

Database initialization is handled during FastAPI's application lifespan.

## 🐳 Docker Configuration

Docker Compose orchestrates two primary services:

**Application Service**
- Runs the FastAPI backend using Uvicorn.
- Exposes port 8080.
- Loads application configuration from environment variables.
- Supports source-code synchronization during development.

**Database Service**
- Uses PostgreSQL 17.5.
- Exposes PostgreSQL on port 5432.
- Uses a named Docker volume for persistent storage.

Start the services:

```bash
docker compose up --build
```

Stop the services:

```bash
docker compose down
```

Stop services and remove database volumes:

```bash
docker compose down -v
```

## 🚀 Deployment

The repository includes a `railway.json` configuration for Railway deployment.

The deployment configuration specifies:

- Dockerfile-based application builds.
- Uvicorn as the application server.
- Automatic restart behavior on deployment failures.
- A single application replica.

Configure the required environment variables and a reachable PostgreSQL database in the deployment environment.

## 🔐 Security Considerations

- Store LLM API keys and email credentials in environment variables.
- Never expose provider credentials to frontend clients.
- Use application-specific email credentials where supported.
- Restrict database access to trusted services.
- Validate incoming requests using Pydantic.
- Use secure HTTPS connections in production.
- Consider adding user authentication and authorization before exposing the API publicly.

## 🔮 Future Improvements

- Implement persistent conversational memory across sessions.
- Add user authentication and multi-user support.
- Introduce streaming responses for real-time AI interactions.
- Add automated integration tests for agents and email tools.
- Implement background task processing for long-running agent workflows.
- Introduce observability with structured logging and tracing.
- Add human approval before executing sensitive email operations.

## 👨‍💻 Author

**Prasanna Kumar M**

- GitHub: [Prasanna-cpu](https://github.com/Prasanna-cpu)
- Repository: [CompanionAI](https://github.com/Prasanna-cpu/CompanionAI)

---

⭐ If you find this project interesting, consider giving the repository a star!
