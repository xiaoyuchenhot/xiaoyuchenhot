# CLAUDE.md

This file provides guidance for AI assistants (Claude and others) working in this repository.

---

## Repository Status

This is a **new, empty repository** (`xiaoyuchenhot/xiaoyuchenhot`). There is no source code yet. As the project grows, update this file to reflect the actual codebase structure, tech stack, and conventions discovered.

---

## Development Branch Convention

All AI-driven development must follow the branch naming scheme:

```
claude/<task-slug>-<session-id>
```

- **Never push directly to `main` or `master`** without explicit permission.
- Always open a pull request for review before merging.
- Feature branches should be short-lived and focused on a single task.

---

## Git Workflow

### Committing

1. Stage only the files relevant to the task (avoid `git add -A` or `git add .`).
2. Write clear, descriptive commit messages in the imperative mood:
   - Good: `Add user authentication endpoint`
   - Bad: `stuff`, `fix`, `wip`
3. Commit messages should explain **why**, not just **what**.
4. Never skip commit hooks (`--no-verify`).
5. Never amend published commits — always create a new commit.

### Pushing

```bash
git push -u origin <branch-name>
```

- Retry on network failure with exponential backoff: 2s → 4s → 8s → 16s (max 4 retries).
- Never force-push to shared or main branches.

### Pull Requests

- Keep PR titles under 70 characters.
- PR body should include a summary and a test plan.
- Link the relevant issue when applicable.

---

## File & Directory Conventions

> **Note:** Update this section once the project structure is established.

When files are added, follow these general principles:

- Keep related code co-located (feature-based structure preferred over layer-based).
- Avoid creating new files unless strictly necessary — prefer editing existing ones.
- Do not create documentation files (`.md`) unless explicitly requested.
- Do not add helper utilities or abstractions for one-time use cases.

---

## Coding Conventions

> **Note:** Update this section with language-specific linters, formatters, and style rules once a tech stack is chosen.

General principles to follow regardless of language:

- **Minimal changes**: Only modify what is directly requested or clearly necessary.
- **No over-engineering**: Don't add error handling, fallbacks, or validation for scenarios that cannot happen.
- **No premature abstraction**: Three similar lines of code is better than a premature helper.
- **No backwards-compatibility shims**: Remove unused code completely rather than commenting it out.
- **Security first**: Avoid SQL injection, XSS, command injection, and other OWASP Top 10 vulnerabilities. Validate at system boundaries (user input, external APIs) only.

---

## Testing

> **Note:** Update this section once a testing framework is chosen.

- Run the full test suite before committing.
- Do not mark a task complete if tests are failing.
- Do not retry failing tests in a loop — diagnose the root cause.

---

## AI Assistant Instructions

When working in this repository, Claude should:

1. **Read before modifying** — Always read a file before editing it. Never propose changes to code you haven't examined.
2. **Prefer editing over creating** — Modify existing files rather than creating new ones.
3. **Stay focused** — Do not refactor, clean up, or add features beyond what was explicitly requested.
4. **No emojis** — Unless the user explicitly asks for them.
5. **Short responses** — Keep explanations concise. Use file path references in the format `file_path:line_number`.
6. **Confirm before risky actions** — Ask before deleting files, force-pushing, resetting hard, or modifying shared infrastructure.
7. **Use dedicated tools** — Prefer `Read`, `Edit`, `Write`, `Glob`, and `Grep` over shell equivalents (`cat`, `sed`, `find`, `grep`).
8. **Parallelize independent operations** — When multiple tool calls are independent, make them simultaneously.

### Risky Actions — Always Confirm First

- Deleting files or branches
- Force-pushing (`--force`)
- `git reset --hard`
- Dropping database tables or data
- Modifying CI/CD pipelines
- Creating/closing/commenting on PRs or issues
- Posting to external services

---

## Updating This File

As the project evolves, update this file to reflect:

- The actual tech stack and dependencies
- Project-specific linting and formatting commands
- How to run tests and builds locally
- Environment variable requirements
- Architecture decisions and key design patterns
- Any non-obvious conventions specific to this codebase
