# Gemini Backend

A Django REST API backend for chatrooms, authentication, subscriptions, and AI-powered responses using the Gemini API. Includes JWT authentication, Stripe integration, and asynchronous task processing with Celery and Redis.

---

## Table of Contents

- [Setup & Run](#setup--run)
- [Architecture Overview](#architecture-overview)
- [Queue System (Celery)](#queue-system-celery)
- [Gemini API Integration](#gemini-api-integration)
- [Assumptions & Design Decisions](#assumptions--design-decisions)
- [Testing with Postman](#testing-with-postman)
- [Deployment & Access](#deployment--access)

---

## Setup & Run

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/gemini-backend.git
cd gemini-backend
```

### 2. Create & Activate Virtual Environment

```sh
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the root directory:

```
SECRET_KEY=your-django-secret
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
GOOGLE_GEMINI_API_KEY=your-gemini-api-key
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```sh
python manage.py createsuperuser
```

### 7. Start Redis (if not running)

```sh
redis-server
```

### 8. Start Celery Worker

```sh
celery -A backend worker --loglevel=info --pool=solo
```

### 9. Start Django Server

```sh
python manage.py runserver
```

---

## Architecture Overview

- **apps/authentication**: Custom user model (mobile-based), OTP, JWT authentication.
- **apps/chatrooms**: ChatRoom and ChatMessage models, async AI response via Celery.
- **apps/subscriptions**: UserProfile, Stripe integration for subscriptions.
- **Celery**: Handles background tasks (e.g., Gemini API calls).
- **Redis**: Used as broker and cache backend.
- **Stripe**: Handles payments and webhooks.
- **Gemini API**: Provides AI responses to user messages.

---

## Queue System (Celery)

- **Purpose**: Offloads long-running tasks (like Gemini API calls) from the main request/response cycle.
- **How it works**:
  - When a user sends a message, a Celery task is queued.
  - The worker picks up the task, calls the Gemini API, and updates the message with the AI response.
- **Broker/Backend**: Redis is used for both task queue and result backend.

---

## Gemini API Integration

- **Location**: `apps/chatrooms/gemini.py`
- **Usage**: When a user sends a message, the message is sent to the Gemini API via a Celery task.
- **API Key**: Set via `GOOGLE_GEMINI_API_KEY` in your `.env`.
- **Error Handling**: If the Gemini API fails, the message status is updated accordingly.

---

## Assumptions & Design Decisions

- **Mobile-based authentication**: Users log in with mobile numbers, not usernames/emails.
- **UserProfile**: Created automatically via Django signals for each user.
- **Caching**: Chatroom lists are cached per user for performance.
- **Stripe**: Used for subscription management; webhooks are handled and verified.
- **Celery**: Used for all time-consuming or external API tasks.
- **Environment-specific settings**: Use `development.py` and `production.py` to override `base.py`.

---

## Testing with Postman

1. **Authentication**

   - Register: `POST /auth/signup`
   - Send OTP: `POST /auth/send-otp`
   - Verify OTP: `POST /auth/verify-otp`
   - Login: `POST /auth/token/obtain/` (if JWT endpoints are exposed)

2. **Headers**

   - For authenticated endpoints, set:
     ```
     Authorization: Bearer <your_jwt_token>
     ```

3. **Chatrooms**

   - List: `GET /chatroom`
   - Create: `POST /chatroom` (body: `{ "name": "My Room" }`)

4. **Messages**

   - List: `GET /chatroom/<chatroom_id>/messages`
   - Send: `POST /chatroom/<chatroom_id>/messages` (body: `{ "user_message": "Hello" }`)

5. **Subscriptions**

   - Subscribe: `POST /subscribe/pro`
   - Webhook: Stripe will call `/webhook/stripe` (test with Stripe CLI)

6. **User Info**
   - `GET /user/me`

---

## Deployment & Access

### Render.com Example

- **render.yaml** should specify:
  ```yaml
  startCommand: python -m gunicorn backend.asgi:application -k uvicorn.workers.UvicornWorker
  ```
- Set environment variables in Render dashboard (`.env` values).
- Set `DJANGO_SETTINGS_MODULE` to `backend.settings.production` for production.
- Add your Render domain to `ALLOWED_HOSTS`.

### Other Platforms

- Neon - used for postgressql
- Redis - cloud redis

---
