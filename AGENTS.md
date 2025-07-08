# Agent Instructions for AI Drawing Learning App

Welcome, AI Developer! This document provides guidelines for working on the AI Drawing Learning App repository.

## Project Overview

This is a Python-based web application aimed at helping users learn drawing with AI assistance. Key components include:
*   User authentication
*   Drawing canvas with AI feedback/suggestions
*   Structured learning modules
*   Showcase for user artwork
*   Backend API and database

## General Guidelines

1.  **Understand the Goal:** Before making changes, ensure you understand the specific task or feature request. Refer to the `README.md` for project structure and overall goals.
2.  **Follow the Plan:** Adhere to the plan provided or created for the task. If the plan needs adjustment, update it using the `set_plan` tool and explain the reasoning.
3.  **Code Quality:**
    *   Write clean, readable, and maintainable Python code.
    *   Follow PEP 8 style guidelines.
    *   Add comments to explain complex logic or non-obvious decisions.
    *   Ensure code is well-tested.
4.  **Testing:**
    *   Write unit tests for new functions and modules in the `tests/` directory.
    *   Ensure all tests pass before submitting changes. If you add new features, add new tests. If you modify existing features, ensure existing tests still pass or update them accordingly.
    *   Aim for good test coverage.
5.  **Dependencies:**
    *   If new Python dependencies are needed, add them to `requirements.txt`.
    *   Use `run_in_bash_session` to install dependencies (`pip install -r requirements.txt`).
6.  **Directory Structure:**
    *   Place code in the appropriate directories as outlined in `README.md` and the project plan.
    *   Backend API code goes into `app/api/`.
    *   Authentication code into `app/auth/`.
    *   Database models/logic into `app/database/`.
    *   Learning module specific code into `app/learn/`.
    *   Drawing canvas and AI interaction code into `app/draw/`.
    *   User showcase code into `app/showcase/`.
    *   Static assets (CSS, JS, images for frontend if any) into `app/static/`.
    *   HTML templates (if using Flask/Django templates) into `app/templates/`.
    *   Tests go into the `tests/` directory, mirroring the structure of the `app/` directory where applicable.
7.  **`__init__.py` Files:** Ensure `__init__.py` files are present in all directories that should be treated as Python packages. These are typically empty or may contain package-level imports or initializations.
8.  **Commit Messages:** Write clear and concise commit messages. Follow standard conventions (e.g., imperative mood for the subject line, max 50 chars for subject, detailed body if needed).
9.  **Security:** Be mindful of security best practices, especially for authentication, data handling, and external API interactions. Do not commit sensitive information (API keys, secrets) directly into the repository; use environment variables or a secure configuration management system.
10. **User Interaction:**
    *   If requirements are unclear, ask for clarification using `request_user_input`.
    *   If you're stuck or need to make a significant design decision not covered by the plan, consult the user.
11. **`AGENTS.md` Precedence:** Instructions in more deeply-nested `AGENTS.md` files take precedence over this one for files within their scope. User's explicit instructions always take precedence.

## Specific Technologies (To be updated as project evolves)

*   **Primary Language:** Python
*   **Web Framework:** (e.g., Flask, Django - TBD)
*   **Database:** (e.g., PostgreSQL, SQLite - TBD)
*   **AI Libraries:** (e.g., TensorFlow, PyTorch, OpenAI SDK - TBD)

Thank you for your contribution!
