# Double Commands

LLM-agnostic context loading commands for the Double memory system.

## Claude Code Setup

Commands are in `.claude/commands/*.md`. Use them with:
- `/business` - Load business context
- `/engineering` - Load engineering best practices
- `/research` - Load research intelligence
- `/tasks` - Load task management
- `/memory` - Load ALL context (comprehensive)

**Installation:**
Commands are already in `.claude/commands/` and will auto-load in Claude Code.

## Cursor Setup

Create `.cursorrules` in your project root:

```markdown
# Memory System Rules

When working on this project, reference these memory files:

## Engineering Best Practices
(Customize based on your tech stack)
- General: ~/memory/engineering/everything.md
- Python: ~/memory/engineering/python.md
- TypeScript: ~/memory/engineering/typescript.md
- Databases: ~/memory/engineering/databases.md

## Project Context
- Projects: ~/memory/projects/*.md

## Tasks
- Active: ~/memory/tasks/active.md
- Backlog: ~/memory/tasks/backlog.md

Read these files to understand coding preferences and current context.
```