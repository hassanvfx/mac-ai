# Working with Cline AI Assistant

💡 **Pro Tip**: Ask Cline *"how can i work with you?"* anytime - Cline will explain the workflow and answer questions!

This guide explains how to work effectively with Cline AI Assistant using the ClineFlow workflow system.

## Table of Contents
- [Getting Started](#getting-started)
- [Reference System](#reference-system)
- [Code Organization Guidelines](#code-organization-guidelines)
- [Journal System](#journal-system)
- [Intelligent Commit Workflow](#intelligent-commit-workflow)
- [Documentation Best Practices](#documentation-best-practices)
- [Code Quality Standards](#code-quality-standards)

---

## Getting Started

### Understanding File Access

Cline can access files in your project using:

**@ Mentions** - For any committed file:
```markdown
✅ @src/components/App.tsx
✅ @clineflow/PROCEDURES.md
✅ @clineflow/backend-api/README.md  (if using reference system)
```

**Direct Paths** - Alternative way:
```markdown
✅ Can you read src/components/App.tsx?
✅ Can you read clineflow/PROCEDURES.md?
```

Both methods work - use whichever feels natural!

---

## Reference System

> 💡 **Pro Tip - Let Cline Do It!**
> 
> You can ask Cline to set this up for you:
> 
> *"I need to setup cline refs to [project-a] and [project-b] which are in ../project-a and ../project-b. Can you help me configure this?"*
> 
> Cline will handle the config file and run the setup script automatically!

### What Is It?

The optional reference system lets Cline explore other repositories without copying files. When set up, Cline can access external codebases just like your project files.

### Setting Up References

```bash
# 1. Clone repos you want to reference
cd ~/projects
git clone https://github.com/your-org/backend-api

# 2. Configure paths
cp .clineflow.example .clineflow.local
nano .clineflow.local

# Add your paths:
BACKEND_API_PATH="/Users/yourname/projects/backend-api"

# 3. Create symlinks
./setup-refs.sh
```

### Using Referenced Files

Once set up, reference files are accessible:
```markdown
✅ @clineflow/backend-api/README.md
✅ @clineflow/backend-api/src/api/routes/users.py
✅ Can you read clineflow/backend-api/docs/API.md?
```

### Benefits

- **No Duplication**: Repos stay in their original location
- **Always Current**: Changes sync instantly via symlinks
- **Full Access**: Cline can explore the entire codebase
- **Team Flexible**: Each developer can place repos anywhere

See `clineflow/README.md` for complete reference system documentation.

---

## Code Organization Guidelines

### File Size Rule

- **Ideal:** Files should be 300-500 lines of code (LOC)
- **Maximum:** 1,000+ LOC is unacceptable
- **Action:** Break down files that exceed limits

### Why This Matters

1. **Maintainability:** Smaller files are easier to understand and modify
2. **Reusability:** Well-factored code can be reused
3. **Testing:** Smaller units are easier to test
4. **Collaboration:** Easier for teams to work in parallel

### How to Modularize

**Example: Breaking Down a Large Component**

```typescript
// ❌ BAD: 1,500 line monolithic component
function MassiveComponent() {
  // Everything in one place
  // Data fetching
  // Business logic  
  // UI rendering
  // Event handlers
  // Styling
}

// ✅ GOOD: Broken into focused pieces
function ParentComponent() {
  return (
    <>
      <HeaderSection />
      <DataDisplay />
      <ActionButtons />
      <FooterSection />
    </>
  );
}
```

**Example: Breaking Down a Large Module**

```python
# ❌ BAD: 2,000 line module with everything
# api.py
class UserAPI:
    def create_user(self): ...
    def update_user(self): ...
    def delete_user(self): ...
    def authenticate(self): ...
    def send_email(self): ...
    def validate_data(self): ...
    # ... 50 more methods

# ✅ GOOD: Focused modules
# api/users.py - User CRUD operations
# api/auth.py - Authentication logic
# api/email.py - Email functionality  
# api/validation.py - Data validation
```

### Single Responsibility Principle

Each file should have one clear purpose:
- ✅ `UserProfile.tsx` - Displays user profile
- ✅ `authService.ts` - Handles authentication
- ✅ `database.py` - Database connection logic
- ❌ `utils.ts` - Everything miscellaneous (too vague)

---

## Journal System

### When to Create Journals

Create a task journal in `docs/journals/[task-name].md` for:
- Features that will take multiple sessions
- Complex implementations with many moving parts
- Features with multiple phases
- Work that requires tracking decisions and progress

### Journal Template

Use `clineflow/JOURNAL_TEMPLATE.md` as your starting point.

### Structure

```markdown
# [Feature Name] Implementation Journal

## Overview
Brief description of the feature and its goals.

## Status Overview

### Phase 1: [Name] - [Status: ✅/🔧/❌]
- [x] Completed task
- [ ] Pending task

### Phase 2: [Name] - [Status]
...

## Journal Entries

### YYYY-MM-DD HH:MM - Entry Title
**What Changed:**
- Specific changes made

**Why:**
Explanation of decisions

**Next Steps:**
- Action items

---

## Known Issues

### Issue Name
**Problem:** Description
**Status:** Investigation/Blocked/Fixed
**Workaround:** Temporary solution

## Quick Reference

### Key Files
- `path/to/file` - Purpose
```

### Best Practices

1. **Update Frequently:** Add entries as you make progress
2. **Be Specific:** Include file names and code snippets
3. **Document Decisions:** Explain WHY you chose an approach
4. **Track Blockers:** Note what's blocking progress
5. **Use for Context:** Reference the journal in new tasks

---

## Intelligent Commit Workflow

### The Magic Command

When ready to commit, simply say:

**`"please commit"`**

That's it! Cline handles everything automatically.

*Note: "commit changes" or just "commit" also work, but "please commit" is the recommended command.*

### What Happens Automatically

1. **📝 Generate Journal Entry**
   - Uses conversation context
   - Creates meaningful entry with decisions and changes

2. **📁 Update Journal**
   - Appends entry to your active journal
   - Maintains proper formatting

3. **🎯 Stage Everything**
   - Stages all code changes
   - Stages the updated journal

4. **💬 Create Commit Message**
   - Generates descriptive message
   - Includes clear bullet points

5. **✅ Execute Commit**
   - Runs `git commit`
   - Confirms completion

### Example Workflow

```markdown
You: "I've finished implementing the user service"
[... work on code ...]
You: "please commit"

Cline: ✅ Committed changes with journal entry

### 2025-11-08 15:30 - Implemented User Service

**Achievement:**
Successfully implemented complete user service with CRUD operations.

**Implementation Details:**
- Created `src/services/userService.ts` - User business logic
- Created `src/api/userRoutes.ts` - REST API endpoints
- Modified `src/database/models.ts` - Added User model
- Created `src/tests/userService.test.ts` - Unit tests

**Technical Decisions:**
Chose async/await pattern for database operations for better readability.
Implemented input validation at the service layer.

**Next Steps:**
- [ ] Add authentication middleware
- [ ] Implement rate limiting
- [ ] Add caching layer

**Status:** Complete

Commit: abc1234
feat(users): implement user service with CRUD operations
```

### Benefits

- **Context-Aware**: Meaningful journal entries
- **Time-Saving**: No manual updates needed
- **Consistent**: Proper documentation every time
- **Historical Record**: Every commit documented

### Requirements

**You MUST have an active journal** before committing:
- For new tasks: Create `docs/journals/[task-name].md` first
- For continuations: Use existing journal

See `clineflow/PROCEDURES.md` SOP-005 for implementation details.

---

## Documentation Best Practices

### Documentation Structure

**For New Features:**

1. **Specification** (`docs/[FEATURE].md`)
   - Overview and requirements
   - Implementation plan
   - API contracts
   - UX flows

2. **Journal** (`docs/journals/[FEATURE].md`)
   - Implementation progress
   - Journal entries
   - Known issues
   - Quick reference

3. **Issue Docs** (`docs/[FEATURE]_[ISSUE].md`)
   - For specific problems requiring investigation

### Documentation Style

- Use emojis for visual scanning (✅ ❌ 🔧 ⚠️ 📝)
- Include code snippets with syntax highlighting
- Add diagrams for complex flows
- Keep "Quick Reference" sections
- Update status regularly

---

## Code Quality Standards

### No Unnecessary Code

Every line should serve a specific purpose:

```typescript
// ❌ BAD: Unused imports and dead code
import { useState, useEffect, useMemo } from 'react';
import { someUnusedUtil } from './utils';

function MyComponent() {
  const [unusedState, setUnusedState] = useState(false);
  
  if (false) {
    console.log('Dead code');
  }
  
  return <div>Hello</div>;
}

// ✅ GOOD: Clean, purposeful code
import { useState } from 'react';

function MyComponent() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

### Implement Only What's Needed

Don't add features "just in case":

```typescript
// ❌ BAD: Over-engineered with unused features
interface UserCardProps {
  user: User;
  onEdit?: () => void;      // Not used anywhere
  onDelete?: () => void;    // Not used anywhere
  showActions?: boolean;    // Not needed
  variant?: 'compact' | 'full'; // Not needed
}

// ✅ GOOD: Implements only what's needed now
interface UserCardProps {
  user: User;
}
```

### Type Safety

```typescript
// ❌ BAD: Using any defeats type safety
function processData(data: any) {
  return data.value.toUpperCase();
}

// ✅ GOOD: Proper types
interface DataItem {
  value: string;
  id: number;
}

function processData(data: DataItem): string {
  return data.value.toUpperCase();
}
```

---

## Working with Large Tasks

### Task Size Management

When a task becomes too large (context window approaching limits):

1. **Create a Journal:** Document progress
2. **Summarize State:** Write comprehensive summary of:
   - What's been completed
   - What's remaining
   - Key technical decisions
   - Important file locations
3. **Create New Task:** Use journal as context
4. **Include Verbatim Quotes:** Preserve exact context

### Multi-Task Pattern

```markdown
# Task 1: Initial Implementation
1. Created docs/journals/feature.md
2. Implemented Phase 1
3. Context window at 80%

# Task 2: Continuation  
1. Loaded context from docs/journals/feature.md
2. Implemented Phase 2
3. Updated journal
```

---

## Getting Help

### Understanding Cline

💡 **Ask Cline directly**: *"how can i work with you?"* - Get explanations anytime!

### For Feature Questions

1. Check existing documentation in `docs/`
2. Review similar implemented features
3. Check reference repos (if using reference system)

### For Technical Issues

1. Check if documented in `docs/[FEATURE]_ISSUE.md` files
2. Review journal entries for similar problems
3. Check git history for related changes

### For Cline Behavior

- This document explains Cline's capabilities
- Use `.clinerules` for quick reference
- See `clineflow/PROCEDURES.md` for detailed procedures

---

## Cline-Specific Tips

### Plan Mode vs Act Mode

- **Plan Mode:** Discussion, planning, gathering requirements
- **Act Mode:** Actual code changes and file operations

### Tool Usage

- Cline reads files before modifying them
- Uses `replace_in_file` for targeted edits
- Uses `write_to_file` for new files or complete rewrites
- Waits for confirmation after each tool use

### Communication Style

- Cline is direct and technical
- Doesn't start with "Great" or "Certainly"
- Provides clear explanations with examples
- Focuses on accomplishing tasks efficiently

---

**Last Updated:** November 8, 2025
