# FlyRank Embeddable Widget & Lead-Capture Platform

A multi-tenant embeddable widget and lead-capture platform built with FastAPI, PostgreSQL, SQLAlchemy, and Docker.

Customers can create widgets, embed them into external websites using a single JavaScript `<script>` tag, receive public submissions, apply validation and spam protection, enrich submissions with geo-location, and view submission statistics through authenticated dashboard APIs.

---

## Features

- User registration and JWT authentication
- Multi-tenant widget management
- Widget CRUD operations
- Public widget configuration
- Embeddable JavaScript widget
- Cross-origin customer website support
- CORS configuration
- Submission validation with Pydantic
- Honeypot spam protection
- IP-based rate limiting
- Idempotent submissions
- Geo-location provider fallback
- Background notification processing with retries
- Safe notification failure handling
- PostgreSQL persistence
- Alembic migrations
- Dashboard submission APIs
- Dashboard statistics
- Database indexes
- Cached and versioned widget delivery
- Automated tests

---

## Architecture

```text
                    ┌─────────────────────┐
                    │     Owner/User      │
                    └──────────┬──────────┘
                               │
                         JWT Authentication
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │    Application      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
         Auth / Users      Widget API      Dashboard API
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                         PostgreSQL
                               ▲
                               │
                         Submissions
                               ▲
                               │
Customer Website ──► widget.js ──► Public Submission API
                               │
                               ├── Validation
                               ├── Rate Limiting
                               ├── Honeypot
                               ├── Idempotency
                               ├── Geo Provider A
                               ├── Geo Provider B
                               └── Background Notification