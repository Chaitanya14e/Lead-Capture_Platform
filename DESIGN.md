# Embeddable Widget & Lead-Capture Platform — Design

## 1. Problem Statement

This platform allows customers to create embeddable lead-capture widgets such
as signup forms, contact forms, and call-to-action forms.

A customer creates a widget through an authenticated API and receives a
JavaScript embed snippet. The snippet can be placed on a website running on a
different origin.

When a visitor submits the widget:

1. The request reaches the public submission API.
2. The payload is validated.
3. CORS rules are enforced.
4. Rate limiting and spam protection are applied.
5. The visitor IP is enriched with geographic information.
6. The submission is stored.
7. A non-critical email/webhook side effect is triggered.
8. The widget owner can view submissions through authenticated dashboard APIs.

The system is designed to treat all public browser input as untrusted.

---

## 2. Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy

### Database

- PostgreSQL
- Docker Compose

### Authentication

- JWT-based authentication

### Public Widget

- HTML
- CSS
- JavaScript

### External Services

- Geo provider A: ip-api.com
- Geo provider B: ipapi.co
- Email side effect: local console logging or Mailpit

All secrets will be stored in environment variables.

---

## 3. High-Level Architecture

```text
                    ┌─────────────────────┐
                    │    Widget Owner     │
                    │  Authenticated User │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Widget Management    │
                    │ API                  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PostgreSQL       │
                    │                     │
                    │ Users               │
                    │ Widgets             │
                    │ Submissions         │
                    └──────────┬──────────┘
                               ▲
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              │                                 │
    ┌─────────┴──────────┐            ┌─────────┴──────────┐
    │ Customer Website   │            │ Owner Dashboard    │
    │ Different Origin   │            │ Authenticated      │
    └─────────┬──────────┘            └────────────────────┘
              │
              │ widget.js
              ▼
    ┌─────────────────────┐
    │ Public Widget API   │
    │ Config + JS         │
    └─────────┬───────────┘
              │
              │ visitor submits
              ▼
    ┌─────────────────────┐
    │ Submission API      │
    └─────────┬───────────┘
              │
       ┌──────┴───────────────┐
       │                      │
       ▼                      ▼
 Validation              Rate Limit
       │                      │
       └──────────┬───────────┘
                  ▼
            Spam Protection
                  │
                  ▼
            Geo Enrichment
             │          │
             │          └── Provider B
             └── Provider A
                  │
                  ▼
             Store Record
                  │
             ┌────┴─────┐
             │          │
             ▼          ▼
          Dashboard   Email/Webhook