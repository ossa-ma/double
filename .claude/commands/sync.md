Process all entries in ~/memory/.inbox.md and route to appropriate files.

**Smart Routing:** Load only files relevant to inbox content. Use judgment based on content meaning, not rigid keyword matching.

## Available Files

**Engineering:** (customize based on your tech stack)
- `engineering/everything.md` - General patterns, git, debugging, architecture
- `engineering/python.md` - Python patterns and best practices
- `engineering/typescript.md` - TypeScript, Node.js, frontend
- `engineering/databases.md` - SQL, NoSQL, schemas
- `engineering/deployment.md` - Docker, CI/CD, infrastructure
- `engineering/ai.md` - LLMs, prompting, AI engineering

**Projects:** (customize based on your active projects)
- `projects/project-name.md`

**Business:** (customize based on your business areas)
- `business/ideas.md` - Product ideas, pricing, monetization
- `business/marketing.md` - Growth, marketing strategies
- `business/product.md` - Product decisions

**Research:**
- `research/companies.md` - Company intel
- `research/people.md` - People, contacts

**Tasks:**
- `tasks/active.md` - Current work
- `tasks/backlog.md` - Future work
- `tasks/blocked.md` - Blocked items

## Process

1. **Read inbox** (`~/memory/.inbox.md`) - understand what's captured
2. **Determine relevance** - which files need updating?
   - Use judgment, not keyword matching
   - Some insights span multiple files (e.g., logging applies to both Python and iOS)
   - Cross-domain patterns might go in `everything.md`
   - Project work goes in specific project files
3. **Load only relevant files** - don't load everything, but don't be rigid
4. **Update files** - add content to appropriate sections, update timestamps, cross-reference with [[links]]
5. **Archive** - move processed to `meta/processed/[date].md`, clear inbox
6. **Commit** - `git commit -m "Sync: [brief summary]"`

**Goal:** Efficiency (load less) without rigidity (use actual judgment about relevance).
