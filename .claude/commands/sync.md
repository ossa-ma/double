Process all entries in ~/memory/.inbox.md and route to appropriate files.

**Smart Routing:** Only load files relevant to inbox content. Analyze entries first, load target files only.

## Routing Map

Scan inbox entries for keywords/context to determine targets:

**Engineering:**
- iOS/Swift/SwiftUI → `engineering/ios-swift.md`
- Python/FastAPI/async/Pydantic → `engineering/python.md`
- Git/Docker/logging/debugging → `engineering/everything.md`
- Deployment/infra → `engineering/deployment.md`

**Projects:**
- rlog/reading log → `projects/rlog.md`
- Other project names → `projects/[name].md`

**Business:**
- Ideas/pricing/monetization → `business/ideas.md`
- Marketing/growth → `business/marketing.md`

**Research:**
- Company info → `research/companies.md`
- People/contacts → `research/people.md`

**Tasks:**
- Action items → `tasks/active.md`
- Future work → `tasks/backlog.md`

## Process

1. **Read inbox** (`~/memory/.inbox.md`)
2. **Analyze & route** - scan all entries, determine which files are needed
3. **Load target files only** - don't load unrelated domains
4. **Update files:**
   - Add content to appropriate sections
   - Update timestamps
   - Cross-reference with [[links]]
5. **Archive:** Move processed to `meta/processed/[date].md`, clear inbox
6. **Commit:** `git commit -m "Sync: [brief summary]"`

## Output

Show:
- Files updated (list)
- New insights added (count per domain)
