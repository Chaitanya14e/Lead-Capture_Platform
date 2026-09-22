# Capstone Evidence

This document records verification evidence for the FlyRank Embeddable Widget & Lead-Capture Platform.

## Environment

- OS: Windows
- Backend: FastAPI
- Database: PostgreSQL 16
- Database access: Docker
- Customer site: Python HTTP server
- API port: 8000
- Customer site port: 5500

---

# 1. Authentication

Owner authentication was implemented using JWT.

Verified endpoints:

```text
POST /auth/register
POST /auth/login
GET  /auth/me