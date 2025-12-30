# Double: External Personal Memory for AI

Persistent context for Claude Code, Cursor, and other AI tools. Skips the database, MCP servers, embeddings for simple markdown files and good ol' git.

> **WARNING:** This is a PUBLIC template. Once you clone it and add your notes, DO NOT push your personal version to a public repo. Your memory will contain secrets (both dark personal secrets and security risk secrets), personal information and your working style. Keep it local or push to a NEW private repo.
>
> **DO NOT use GitHub's "Fork" button** - forks of public repos cannot be made private. Use `git clone` instead (see Quick Start below).

## What is Double?

AI assistants forget everything between sessions. Your engineering decisions (which I think are especially important), coding patterns, project context.

Double solves this with organised markdown files that you control. Think of it as a second brain for your AI assistant.

**Why "Double"?** Named after Dostoevsky's novel "The Double" - it's your second self. Not just engineering and research, but business ideas, personal notes, hobbies, workflow preferences.

## Make It Yours

**This is a template, not a rigid system.** The folder structure, commands, and workflows here are a starting point based on one person's working style. You should heavily customise it:

- Rename folders to match your mental model
- Delete categories you don't need (maybe you don't track business ideas or research)
- Add new ones that fit your work (design/, writing/, client-work/, whatever)
- Modify commands to match your workflow
- Change the rules in `meta/` to fit your style

The only critical parts are:
1. Organised markdown files you control
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

## Why `~/double/` in Your Home Directory?

The directory lives at `~/double/` in your home directory (not nested in a project folder or `.claude/` directory) because the commands need to work from anywhere.

When you run `/handoff` from `/Users/you/projects/blog/`, the command writes to `~/double/.inbox.md` - not `./inbox.md` in your current directory.

This means:
- Commands work regardless of where you are
- No relative path issues
- One centralised memory across all your projects
- I've found its less likely to accidentally commit to project repos!

All commands use absolute paths (`~/double/`) to avoid this entirely.

Also no sandbox issues from what I've found: Claude Code already has filesystem access, so ~/double/ doesn't add new attack surface. The commands are markdown files Claude reads, not executable scripts, so no injection risk.

## Quick Start

**1. Clone the template to your home directory:**

> **IMPORTANT:** Clone to `~/double/` (your home directory), NOT inside a project folder or `.claude/` directory.

```bash
git clone https://github.com/ossa-ma/double ~/double
cd ~/double

# IMPORTANT: If you plan to use git, keep it local or make your repo PRIVATE
# Your memory will contain personal info, API keys, and private notes
```

**2. Make commands available globally:**

Claude Code discovers commands from `~/.claude/commands/` (available everywhere) and `.claude/commands/` (project-specific). To use the Double commands from any directory, copy them to your personal commands directory:

```bash
cp ~/double/.claude/commands/*.md ~/.claude/commands/
```

**Advanced: Auto-sync with individual file symlinks**

If you want double commands to auto-update and still keep non-double personal commands separate:

```bash
# Symlink each double command individually
for file in ~/double/.claude/commands/*.md; do
  ln -s "$file" ~/.claude/commands/$(basename "$file")
done
```

Benefits:
- Auto-sync for double commands
- Can add other commands to `~/.claude/commands/` that stay separate
- Note: Need to re-run when adding new commands to double

See [Claude Code Slash Commands docs](https://code.claude.com/docs/en/slash-commands) for more details on how command discovery works.

**3. Use the commands:**
- `/handoff` - End of session, capture what matters
- `/sync` - Route insights to organised files
- `/engineering` - Load engineering context (or `/tasks`, `/business`, `/research`)

That's it. Commands are now available in Claude Code from any directory.

## Core Workflow

### `/handoff` - End of session
```markdown
Synthesize this session into a handoff entry for `~/double/.inbox.md`.

**Critical:** Only capture **reusable insights**, not one-off decisions.

## What to Capture

### Always Include:
- **Learnings:** Patterns, principles, or insights that apply beyond this specific task
  - Writing: Style insights, what worked/didn't work
  - Code: Architecture decisions, why X over Y
  - Research: Key findings, mental models
- **Technical Content:** New knowledge that should go in engineering files
- **Decisions with Rationale:** Only if the "why" is reusable

### Never Include UNLESS RELATED TO CODING:
- Specific edits ("moved section X to Y")
- Task completion status ("finished blog post")
- One-off decisions without broader insight
- Obvious next steps

## Format

[YYYY-MM-DD HH:MM] Session: [Brief description]

Learnings:
- [Reusable insight with context]
- [Pattern or principle discovered]

Technical Content:
- [New knowledge for engineering files]

Decisions:
- [Decision + why it matters beyond this task]

Next:
- [Only non-obvious next steps]

Append the handoff to `~/double/.inbox.md`. Document WHAT WAS LEARNED, not just what files changed.
```

### `/sync` - Process the inbox
```markdown
Process all entries in ~/double/.inbox.md and route to appropriate files.

Steps:
1. Read ~/double/.inbox.md in full
2. For each entry, determine target domain:
   - Technical decisions/learnings → ~/double/engineering/[relevant].md
   - Tasks/TODOs → ~/double/tasks/active.md or ~/double/tasks/backlog.md
   - Project updates → ~/double/projects/[relevant].md
   - Business insights → ~/double/business/[relevant].md
   - People/team info → ~/double/research/people.md
   - Company intel → ~/double/research/companies.md

3. Update target files:
   - Add new sections if needed
   - Preserve existing structure
   - Update "Last updated" timestamps
   - Cross-reference related files using [[links]]

4. Archive processed entries:
   - Move entries to ~/double/meta/processed/[today's date].md
   - Clear ~/double/.inbox.md

5. Git operations:
   git add .
   git commit -m "Daily sync: [date] - [2-3 word summary]"
   git push

Show summary:
- Files updated: [list]
- Tasks added: [count]
- Decisions captured: [count]
```

### `/engineering` - Load context
```markdown
You are now working on engineering/coding tasks. Load and reference the following context:

**General Engineering:** `~/double/engineering/everything.md`
**Python:** `~/double/engineering/python.md`
**TypeScript:** `~/double/engineering/typescript.md`
**Databases:** `~/double/engineering/databases.md`
**AI/ML:** `~/double/engineering/ai.md`
**Evals:** `~/double/engineering/evals.md`
**Research:** `~/double/engineering/research.md`
**Deployment:** `~/double/engineering/deployment.md`
**Analytics:** `~/double/engineering/analytics.md`

When writing code:
- Follow established patterns and preferences
- Avoid documented antipatterns
- Suggest updates when you discover new patterns
- Reference relevant best practices from these files

Read the contents of these files now to understand coding preferences and patterns.
```

Similar commands exist for `/tasks`, `/business`, `/research`, and `/memory` (loads everything).

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

Read the full explanation: [Double: Claude Code Memory Without MCPs and DBs](https://ossa-ma.github.io/blog/double)
