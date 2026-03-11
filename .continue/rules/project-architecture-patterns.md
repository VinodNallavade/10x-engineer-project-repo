---
description: Defines the preferred project structure and coding patterns to maintain a clean and scalable architecture.
---

Follow the project architecture and separation of concerns.

Code organization:
- models → data schemas
- services → business logic
- routes → API endpoints
- utils → helper functions

Guidelines:
- Use Pydantic BaseModel for data models.
- Keep API routes thin and delegate logic to services.
- Avoid placing business logic inside route handlers.
- Prefer simple and maintainable solutions over complex abstractions.