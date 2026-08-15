# System Procedures for Working with Cline

This document contains detailed system rules and standard operating procedures for Cline AI Assistant using the ClineFlow workflow system.

## Table of Contents
- [Code Organization Standards](#code-organization-standards)
- [Journal System Procedures](#journal-system-procedures)
- [Documentation Requirements](#documentation-requirements)
- [Code Quality Guidelines](#code-quality-guidelines)
- [File Access Procedures](#file-access-procedures)
- [Task Management](#task-management)

---

## Code Organization Standards

### File Size Requirements

**Absolute Rules:**
- Files SHOULD be 300-500 lines of code (LOC) ideally
- Files over 1,000 LOC are **unacceptable** and must be refactored
- When reviewing/creating files, always check line count
- If a file exceeds limits, it MUST be broken down

### Modularization Strategy

**When to Break Down Code:**
1. File exceeds 500 LOC
2. File has multiple distinct responsibilities
3. Logic can be reused elsewhere
4. Testing becomes difficult

**How to Modularize:**

```typescript
// Pattern 1: Extract Sub-Components (React/Vue/etc)
function LargeComponent() {
  return (
    <Container>
      <HeaderSection />
      <MainContent />
      <FooterSection />
    </Container>
  );
}

// Pattern 2: Extract Custom Hooks (React)
function useComponentLogic() {
  const [state, setState] = useState();
  // Complex logic here
  return { state, actions };
}

// Pattern 3: Extract Service Layer (Any Language)
// services/userService.ts
export class UserService {
  async createUser(data: UserData): Promise<User> {
    // Business logic
  }
}

// Pattern 4: Extract Utilities
// utils/validation.ts
export function validateEmail(email: string): boolean {
  // Validation logic
}
```

### Code Structure

```typescript
// 1. Imports (grouped logically)
import React, { useState, useEffect } from 'react';
import { externalLibrary } from 'external-lib';
import { internalUtil } from './utils';

// 2. Type Definitions
interface ComponentProps {
  id: string;
  onAction: (id: string) => void;
}

// 3. Implementation
export function Component({ id, onAction }: ComponentProps) {
  // State
  const [local, setLocal] = useState();
  
  // Effects
  useEffect(() => {
    // Side effects
  }, []);
  
  // Handlers
  const handleClick = () => {
    onAction(id);
  };
  
  // Render
  return <div onClick={handleClick}>Content</div>;
}
```

---

## Journal System Procedures

### When to Create a Journal

**Required for:**
- Features spanning multiple development sessions
- Complex features with 3+ phases
- Features requiring significant architectural decisions
- Work that may need context transfer to new tasks

**Not Required for:**
- Simple bug fixes
- Single-file updates
- Minor tweaks

### Journal Creation Process

**Step 1: Create Journal File**
```bash
# Location: docs/journals/[feature-name].md
# Use lowercase with hyphens
# Example: docs/journals/user-authentication.md
```

**Step 2: Use Template**
Copy structure from `clineflow/JOURNAL_TEMPLATE.md`

**Step 3: Initialize Sections**
- Write overview
- Create phase breakdown with checkboxes
- Add initial journal entry
- Set up quick reference

**Step 4: Update Regularly**
- Add entry after each significant change
- Update phase checkboxes as tasks complete
- Document all decisions and why they were made
- Track blockers and issues

### Journal Entry Format

```markdown
### YYYY-MM-DD HH:MM - [Entry Title]

**Achievement/Change:**
Brief description of what was accomplished or changed.

**Implementation Details:**
- Created `path/to/file.ts` - Purpose
- Modified `another/file.ts` - What changed
- Key code snippet or approach used

**Why This Approach:**
Explanation of technical decisions made.

**Testing/Verification:**
How to verify the changes work.

**Next Steps:**
- [ ] Specific next action
- [ ] Another action

**Status:** [In Progress / Blocked / Complete]

---
```

### Using Journals for Task Continuation

When approaching context window limits:

1. **Summarize in Journal:**
   - Document all completed work
   - List remaining tasks
   - Note key technical decisions
   - Include file locations and snippets

2. **Create New Task:**
   ```markdown
   # Context from Previous Task
   
   As documented in docs/journals/[feature].md:
   
   ## Completed
   - Phase 1: [Brief summary]
   - Phase 2: [Brief summary]
   
   ## Current State
   [Direct quotes from journal about where work left off]
   
   ## Next Steps
   Starting Phase 3: [Description]
   See journal for complete technical details.
   ```

3. **Reference Verbatim:**
   Include exact quotes from previous conversation to preserve context

---

## Documentation Requirements

### Documentation Hierarchy

**Level 1: Feature Specifications**
- Location: `docs/[FEATURE].md`
- Purpose: Complete feature design and requirements
- Audience: Developers, product managers, Cline
- Contents: Overview, requirements, implementation plan, API contracts, workflows

**Level 2: Implementation Journals**
- Location: `docs/journals/[feature].md`
- Purpose: Track implementation progress and decisions
- Audience: Developers, Cline (for task continuation)
- Contents: Phase tracking, journal entries, known issues, quick reference

**Level 3: Issue Documents**
- Location: `docs/[FEATURE]_[ISSUE].md`
- Purpose: Deep-dive investigations of specific problems
- Audience: Developers debugging similar issues
- Contents: Problem description, investigation, root cause, solution

### Documentation Style Guide

**Use Emojis for Scanning:**
- ✅ Complete
- ❌ Failed/Blocked
- 🔧 In Progress
- ⚠️ Warning/Caution
- 📝 Note/Documentation
- 🎯 Goal/Target
- 💡 Tip/Best Practice

**Code Snippets:**
```typescript
// Always use syntax highlighting
// Include file paths in comments
// Keep snippets focused and relevant

// Example from src/components/Example.tsx
function Example() {
  return <div>Clear, focused example</div>;
}
```

**Structure:**
- Use clear headings (##, ###)
- Break up long sections
- Include table of contents for long docs
- Add "Last Updated" dates

---

## Code Quality Guidelines

### No Unnecessary Code

**Rule:** Every line must serve a purpose for THIS file/component.

**Check Before Committing:**
- Remove unused imports
- Remove commented-out code
- Remove unused variables
- Remove dead code paths
- Remove debug console.logs

**Example Review:**
```typescript
// ❌ REMOVE
import { unusedUtil } from './utils'; // Not used
const DEBUG = false; // Dead code
if (DEBUG) { console.log('debug'); } // Dead code

// ✅ KEEP
import { neededUtil } from './utils'; // Actually used
const result = neededUtil(data); // Used below
```

### Implement Only What's Needed

**Rule:** Implement only what's needed NOW, not what MIGHT be needed.

**Don't Add:**
- "Future-proof" features not in current requirements
- Optional parameters that have no current use case
- Commented-out "alternative implementations"
- Overly generic abstractions

**Example:**
```typescript
// ❌ BAD: Over-engineered
interface UserCardProps {
  user: User;
  variant?: 'compact' | 'full' | 'minimal'; // Not needed yet
  showAvatar?: boolean; // Not needed yet
  onEdit?: () => void; // Not in requirements
  theme?: 'light' | 'dark'; // Not needed yet
}

// ✅ GOOD: Implements current requirements only
interface UserCardProps {
  user: User;
}
```

### Type Safety

**Requirements:**
- Use proper typing (TypeScript, type hints, etc.)
- Define interfaces/types for all public APIs
- Avoid `any` type or equivalent
- Use type imports where appropriate

**Example:**
```typescript
// ✅ GOOD
interface MessageProps {
  message: Message;
  isCurrentUser: boolean;
  onDelete?: (id: string) => void;
}

export function MessageBubble({ 
  message, 
  isCurrentUser,
  onDelete 
}: MessageProps) {
  // Implementation
}
```

---

## File Access Procedures

### Accessing ClineFlow Files

**ClineFlow documentation files** in `clineflow/` are accessible:

**Using @ Mentions:**
```markdown
✅ @clineflow/PROCEDURES.md
✅ @clineflow/WORKING_WITH_CLINE.md
✅ @clineflow/JOURNAL_TEMPLATE.md
```

**Using Direct Paths:**
```markdown
✅ Can you read clineflow/PROCEDURES.md?
✅ Can you read clineflow/WORKING_WITH_CLINE.md?
```

Both methods work - use whichever is natural!

### Accessing Reference System Files

**If using the optional reference system**, linked repositories are accessible:

**Using @ Mentions:**
```markdown
✅ @clineflow/backend-api/README.md
✅ @clineflow/backend-api/src/api/routes/users.py
```

**Using Direct Paths:**
```markdown
✅ Can you read clineflow/backend-api/docs/API.md?
✅ Can you read clineflow/frontend-app/src/components/App.tsx?
```

### Finding Available Reference Files

If reference system is set up, explore the linked repositories just like project files.

---

## Task Management

### Before Starting Any Task

**Checklist:**
1. **Read essential context:**
   - Review any existing documentation in `docs/`
   - Check for related feature implementations
   - Review project architecture if documented

2. **Assess task size:**
   - Small (< 2 hours): Proceed directly
   - Medium (2-8 hours): Consider creating journal
   - Large (> 8 hours): Create journal before starting

3. **Check for existing documentation:**
   - Look for related docs in `docs/`
   - Check for similar implemented features
   - Review existing journals if applicable

### During Task Execution

**Progress Tracking:**
1. Update journal after major changes
2. Mark checkboxes as tasks complete
3. Document technical decisions
4. Note any blockers or issues

**Code Quality:**
1. Keep files under 500 LOC ideally
2. Remove unnecessary code
3. Follow language/framework best practices
4. Write clear comments for complex logic

**Communication:**
1. Be direct and technical
2. Provide clear explanations
3. Include code examples
4. Focus on task completion

### Completing Tasks

**Before Using attempt_completion:**
1. **Verify all tool uses succeeded:**
   - Check user's responses for errors
   - Confirm files were created/modified successfully
   - Verify commands executed without errors

2. **Update documentation:**
   - Update journal with final entry
   - Mark all checkboxes complete
   - Add "Completion" journal entry

3. **Provide clear result:**
   - Summarize what was accomplished
   - List files created/modified
   - Provide testing instructions if applicable

**Example Completion:**
```xml
<attempt_completion>
<result>
Successfully implemented user authentication system:

Files Created:
- src/auth/AuthService.ts - Authentication business logic
- src/auth/AuthProvider.tsx - React context provider
- src/api/authEndpoints.ts - API integration layer

Files Modified:
- src/App.tsx - Added auth routing logic
- src/types/User.ts - Extended User interface

All functionality tested and working as expected.
Ready for integration testing.
</result>
</attempt_completion>
```

---

## Standard Operating Procedures

### SOP-001: Starting a New Feature

1. Check for existing documentation
2. Create feature spec doc if needed: `docs/[FEATURE].md`
3. Create implementation journal: `docs/journals/[feature].md`
4. Outline phases in journal
5. Begin implementation, updating journal regularly

### SOP-002: Modifying Existing Code

1. Read current file
2. Check line count
3. If > 500 LOC, plan modularization
4. Make changes using replace_in_file for targeted edits
5. Verify changes with user before proceeding
6. Update related documentation if needed

### SOP-003: Debugging Issues

1. Check if issue is documented
2. Review journal entries for similar problems
3. Check git history for related changes
4. Check reference repos if using reference system
5. Document investigation in journal or issue doc
6. Implement fix
7. Document solution

### SOP-004: Approaching Context Limits

1. Check current context usage (shown in environment_details)
2. If > 70%, prepare for task continuation:
   - Update journal with current state
   - Document remaining work clearly
   - Note key technical decisions
   - Include verbatim quotes from conversation
3. Use new_task tool with comprehensive context
4. New task references journal for complete picture

### SOP-005: Intelligent Commit Workflow

**Trigger:** User says **"please commit"** (recommended) or "commit changes" or "commit"

**Purpose:** Automatically create git commit with context-aware journal entry

**Procedure:**

1. **Identify Active Journal**
   - Check docs/journals/ for most recently modified .md file
   - OR use journal mentioned in current task context
   - IF no journal exists: Inform user and request journal creation first

2. **Generate Journal Entry**
   Using full conversation context, create entry:
   ```markdown
   ### YYYY-MM-DD HH:MM - [Entry Title from Context]
   
   **Achievement:**
   [Clear description of what was accomplished]
   
   **Implementation Details:**
   - Created/Modified `file.ts` - Purpose and significance
   - Key changes with brief explanation
   - Important code decisions made
   
   **Technical Decisions:**
   [Why this approach was chosen over alternatives]
   
   **Files Changed:**
   - `path/to/file1.ts` - [+50 -20 lines] Description
   - `path/to/file2.tsx` - [+30 lines] Description
   
   **Next Steps:**
   - [ ] Remaining task items
   - [ ] Follow-up work needed
   
   **Status:** [In Progress / Complete / Blocked]
   
   ---
   ```

3. **Append to Journal**
   - Read current journal content
   - Append new entry at end of Journal Entries section
   - Save file

4. **Stage Everything**
   ```bash
   git add .
   git add docs/journals/[journal-name].md
   ```

5. **Generate Commit Message**
   Format:
   ```
   type(scope): brief description
   
   - Key change 1 with context
   - Key change 2 with context
   - Key change 3 with context
   ```
   
   Types: feat, fix, refactor, docs, style, test, chore

6. **Execute Commit**
   ```bash
   git commit -m "[generated message]"
   ```

7. **Confirm to User**
   ```
   ✅ Committed changes with journal entry
   
   Commit: [first 7 chars of hash]
   Files: [count] changed, [insertions](+), [deletions](-)
   ```

**Important Notes:**
- Journal entry MUST be meaningful, not just file lists
- Use conversation context to explain WHY changes were made
- Commit message MUST be descriptive with clear bullet points
- Always wait for git command confirmation before reporting success

### SOP-006: Task Journal Management

**Purpose:** Ensure every task has proper documentation through journals

**When to Create Journal:**
- MANDATORY for all significant tasks
- Not required for trivial fixes

**Multi-Task Journal Pattern:**
When continuing work from previous task:

```markdown
# [Feature Name] - Implementation Journal Index

## Task History
- **Task 1** (2025-11-08): Initial implementation - [Details](#task-1)
- **Task 2** (2025-11-08): Bug fixes - [Details](#task-2)
- **Task 3** (2025-11-09): Polish - [Details](#task-3)

## Current Status
[Summary from most recent task]

---

## Task 1 - Initial Implementation
[Complete task 1 journal entries]

---

## Task 2 - Bug Fixes  
[Complete task 2 journal entries]
```

**Journal Entry Best Practices:**
- Be specific and technical
- Explain WHY, not just WHAT
- Include code snippets for clarity
- Document alternatives considered
- Track blockers and their resolutions
- Update checkboxes as work progresses

**Benefits:**
- Preserves context for task continuation
- Documents technical decisions
- Enables knowledge transfer
- Supports debugging
- Creates project history

---

### SOP-007: Multi-line Git Commits

**Purpose:** Ensure multi-line commit messages never cause command hangs or failures

**The Problem:**
Using `-m` with newlines in bash can cause git commands to hang waiting for input:
```bash
# ❌ NEVER DO THIS - Can hang!
git commit -m "title
bullet 1
bullet 2"
```

**The Solution: Heredoc with EOF**

**Always use this pattern for multi-line commits:**
```bash
git commit -F - << 'EOF'
type(scope): short descriptive title

- Detailed bullet point 1 with context
- Detailed bullet point 2 with reasoning  
- Detailed bullet point 3 with impact

Result: Clear summary of the overall change
EOF
```

**Why This Works:**
- `-F -` tells git to read message from stdin
- `<< 'EOF'` starts a heredoc (quotes prevent variable expansion)
- Content goes between the markers
- `EOF` ends the heredoc
- **Never hangs** - deterministic input, no waiting

**Pattern Breakdown:**
1. **Title line:** `type(scope): description`
   - Types: feat, fix, refactor, docs, style, test, chore
   - Keep under 72 characters
   
2. **Blank line:** Required separator

3. **Bullet points:** Explain the changes
   - Start with `-` for consistency
   - Be specific and technical
   - Explain WHY, not just WHAT
   
4. **Result line:** Summary statement (optional but recommended)

**Example:**
```bash
git add src/auth/ && git commit -F - << 'EOF'
feat(auth): implement JWT authentication system

- Add AuthService with token generation and validation
- Create AuthContext for React state management
- Implement secure token storage using httpOnly cookies
- Add refresh token rotation for enhanced security

Result: Complete authentication system ready for production
EOF
```

**Benefits:**
- ✅ Never hangs or waits for input
- ✅ Handles all special characters correctly
- ✅ Standard Unix pattern
- ✅ Works consistently across all shells
- ✅ Supports detailed, meaningful commit messages

**When to Use:**
- **Always** when commit message has multiple lines
- When commit message includes special characters
- When you want detailed commit history
- For any commit requiring explanation beyond the title

**Integration with SOP-005 (Intelligent Commits):**
When implementing automatic commits, use heredoc pattern to ensure reliability.

---

### SOP-008: Feature Branch Management

**Purpose:** Ensure all development work happens on feature branches, never directly on main/master

**Trigger:** Before starting ANY task that will modify code or files

**Procedure:**

1. **Check Current Branch**
   ```bash
   git branch --show-current
   ```

2. **If on main/master/develop:**
   - Create feature branch immediately
   - Branch naming convention (standard Git Flow):
     ```bash
     # For new features
     git checkout -b feature/short-description
     
     # For bug fixes
     git checkout -b fix/short-description
     
     # For documentation
     git checkout -b docs/short-description
     
     # For refactoring
     git checkout -b refactor/short-description
     ```
   
   - Examples:
     - `feature/user-authentication`
     - `fix/login-timeout`
     - `docs/api-endpoints`
     - `refactor/payment-service`

3. **If already on feature branch:**
   - Verify branch name matches current task
   - If working on different task, create new branch:
     ```bash
     git checkout main
     git pull
     git checkout -b feature/new-task
     ```

4. **Proceed with task**
   - All commits go to feature branch
   - When complete, merge to main via PR/MR

**Integration with Other SOPs:**

- **SOP-001 (Starting New Feature):** Add branch check as first step
- **SOP-002 (Modifying Code):** Verify on correct branch before changes
- **SOP-005 (Intelligent Commits):** Commit message should reference branch
- **SOP-006 (Task Journals):** Journal should note which branch work is on

**Benefits:**
- ✅ Protects main branch from direct commits
- ✅ Enables code review via pull requests
- ✅ Clear separation of features
- ✅ Easy to abandon or rollback work
- ✅ Supports parallel development

**Common Patterns:**

**Solo Developer:**
```bash
# Start task
git checkout -b feature/task-name
# Work and commit
git commit -m "..."
# When done
git checkout main
git merge feature/task-name
git push
git branch -d feature/task-name
```

**Team with PRs:**
```bash
# Start task
git checkout -b feature/task-name
# Work and commit
git commit -m "..."
# Push feature branch
git push -u origin feature/task-name
# Create PR on GitHub/GitLab
# After PR merge, delete branch
git checkout main
git pull
git branch -d feature/task-name
```

**Important Notes:**
- Never commit directly to main/master/develop
- Feature branches should be short-lived (days, not weeks)
- Regularly sync with main: `git checkout main && git pull && git checkout feature/branch && git rebase main`
- Delete branches after merging to keep repo clean

---

### SOP-009: VERSION and CHANGELOG Management

**Purpose:** Maintain accurate version tracking and comprehensive change documentation for all releases.

**Critical Rules:**
1. **VERSION file MUST be in `template/` directory**
   - Ensures distribution with new installations
   - Enables update scripts to check/update version
   - Users see correct current version

2. **Update VERSION on every release**
   - Format: `YYYY.MM.DD.patch`
   - Example: `2025.11.17.0`
   - Increment patch for same-day releases

3. **Update CHANGELOG.md with every release**
   - Add new section at top with version and date
   - Document: Added, Fixed, Changed, Documentation
   - Keep Previous Releases section

4. **VERSION must exist in both locations:**
   - Root `VERSION` - For repository tracking
   - `template/VERSION` - For user distribution

**Implementation Checklist:**

✅ **Before Creating Release:**
- [ ] Update root `VERSION` file
- [ ] Copy `VERSION` to `template/VERSION`
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Commit: `chore: bump version to YYYY.MM.DD.patch and update CHANGELOG`
- [ ] Push to main

✅ **Verification:**
```bash
# Ensure VERSION exists in both locations
ls VERSION template/VERSION

# Verify they match
diff VERSION template/VERSION

# Check CHANGELOG has new version section
head -n 20 CHANGELOG.md
```

**Common Mistake to Avoid:**
- ❌ DON'T update only root VERSION - users won't get it
- ✅ DO copy VERSION to template/ directory
- ✅ DO include VERSION in TEMPLATE_FILES array in update.sh

**Why This Matters:**
- Users running `update.sh` check their local VERSION
- If VERSION isn't in template/, it never gets distributed
- Users see old version even after updates
- Breaks the update feedback loop

**Integration with Other SOPs:**
- Works with SOP-008 (Feature Branches) for release workflow
- Complements installation and update system

---

**Last Updated:** November 17, 2025
