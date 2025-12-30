# Double: External Personal Memory for AI

Persistent context for Claude Code, Cursor, and other AI tools. Skips the database, MCP servers, embeddings for simple markdown files and good ol' git.

> **WARNING:** This is a PUBLIC template. Once you clone it and add your notes, DO NOT push your personal version to a public repo. Your memory will contain secrets, API keys, personal information, and your working style. Keep your fork private or use it locally only.

## What is Double?

AI assistants forget everything between sessions. Your setup decisions, coding patterns, project context - gone every time.

Double solves this with organized markdown files that you control. Think of it as a second brain for your AI assistant.

**Why "Double"?** Named after Dostoevsky's novel "The Double" - it's your second self. Not just engineering and research, but business ideas, personal notes, hobbies, writing style. Everything that makes up how you think and work.

## Make It Yours

**This is a template, not a rigid system.** The folder structure, commands, and workflows here are a starting point based on one person's working style. You should heavily customize it:

- Rename folders to match your mental model
- Delete categories you don't need (maybe you don't track business ideas or research)
- Add new ones that fit your work (design/, writing/, client-work/, whatever)
- Modify commands to match your workflow
- Change the rules in `meta/` to fit your style

The only critical parts are:
1. Organized markdown files you control
2. A capture → process → load workflow
3. Using absolute paths (`~/double/`) in commands

Everything else? Change it.

## Folder Structure

```
~/double/
├── business/        # Ideas, metrics, product decisions
├── engineering/     # Technical patterns, best practices, lessons learned
├── tasks/           # Active work, backlog, waiting
├── projects/        # Project-specific context and decisions
├── research/        # Intelligence on companies, people, markets
├── personal/        # Writing style, preferences, workflows
├── meta/            # System rules, processed entries, changelog
└── .claude/
    └── commands/    # Skills that load context
```

## Why `~/double/` at Top Level?

The directory lives at `~/double/` (not nested in a project folder) because the commands need to work from anywhere.

When you run `/handoff` from `/Users/you/projects/blog/`, the command writes to `~/double/.inbox.md` - not `./inbox.md` in your current directory.

This means:
- Commands work regardless of where you are
- No relative path issues
- One centralized memory across all your projects

All commands use absolute paths (`~/double/`) to avoid this entirely.

## Quick Start

**1. Clone the template:**
```bash
git clone https://github.com/ossa-ma/double ~/double
cd ~/double

# IMPORTANT: If you plan to use git, keep it local or make your repo PRIVATE
# Your memory will contain personal info, API keys, and private notes
```

**2. Use the commands:**
- `/handoff` - End of session, capture what matters
- `/sync` - Route insights to organized files
- `/engineering` - Load engineering context (or `/tasks`, `/business`, `/research`)

That's it. Commands auto-load in Claude Code.

## Core Workflow

**End of session:**
```bash
/handoff
```
Claude captures learnings, technical insights, and decisions. Appends to `.inbox.md`.

**Process the inbox:**
```bash
/sync
```
Routes entries to categorized files, archives processed items, commits to git.

**Load context:**
```bash
/engineering  # Load technical knowledge
/tasks        # Load task management
/business     # Load business context
/memory       # Load everything
```

## Additional Commands

- `/new-task` - Quick task capture without opening files
- `/task-done` - Mark tasks complete
- `/project-status` - Overview of active projects
- `/weekly` - Generate weekly review

## Configuration for Other Tools

**Cursor:**
Add `.cursorrules` file pointing to your double directory (see `meta/` for template).

**Gemini CLI:**
Copy `GEMINI.md` template to auto-load context in any directory.

**Any tool:**
Just read the markdown files in `~/double/`. No special configuration needed.

## Rules

- **Single Source of Truth:** Store each fact in one canonical location
- **Date Everything:** Add "Last updated: YYYY-MM-DD" to time-sensitive info
- **Cross-Reference:** Use `[[links]]` instead of duplicating data
- **Human-Readable:** Write for humans first, AI second

## Why Markdown + Git?

- **No dependencies:** No database, no MCP server, no npm packages
- **Human-readable:** `cat ~/double/engineering/python.md` - that's it
- **Portable:** Works with any tool that can read markdown
- **Transparent:** You see exactly what's stored
- **Actual git:** Full version control, not "inspired by" git

---

Read the full explanation: [Double: Claude Code Memory Without the Database](https://ossa-ma.github.io/blog/double)
