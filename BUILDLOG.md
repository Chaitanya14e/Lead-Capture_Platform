# Build Log

This document records the development process, implementation decisions, problems encountered, and AI-assisted development used during the capstone.

---

## Phase 1 — Design

### Initial Planning

Defined the core problem:

Build a multi-tenant platform where customers can create embeddable widgets and receive validated lead submissions from external websites.

Created:

- `DESIGN.md`
- `README.md`
- `EVIDENCE.md`
- `BUILDLOG.md`
- `capstone.yaml`
- `.env.example`
- `.gitignore`

The initial design defined:

- User model
- Widget model
- Submission model
- Authentication
- Tenant isolation
- Public submission flow
- Geo enrichment
- Rate limiting
- Spam protection
- Background notifications
- Dashboard APIs
- Explicit non-goals

---

# Phase 2 — Backend Foundation

## PostgreSQL

PostgreSQL 16 was selected for persistent storage.

The database was initially exposed on port `5433` because the default host port was unavailable.

Final local database configuration:

```text
127.0.0.1:5433