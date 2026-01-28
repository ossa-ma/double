Show current status of all projects.

Read all files in ~/memory/projects/ directory.

For each project extract:
- Project name
- Status (Active/Blocked/Paused/Completed)
- Last updated date (from git or file timestamp)
- Open tasks (search ~/memory/tasks/active.md for references to this project)
- Recent activity (from git log or project file content)
- Blockers (from ~/memory/tasks/blocked.md)

Display as formatted table:

```
PROJECT STATUS DASHBOARD
========================

Project: [Name]
Status: [Active/Blocked/Paused]
Last Updated: [date] ([X] days ago)
Open Tasks: [count]
  - [task 1]
  - [task 2]
Blockers: [list or "None"]
Recent Activity: [summary from last week]

---

[Repeat for each project]

RECOMMENDATIONS
===============
Stale projects (2+ weeks): [list]
Active projects needing attention: [list]
Healthy projects: [list]
```

Suggest actions for stale or blocked projects.
