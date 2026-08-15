# ClineFlow: Universal AI Assistant Memory System

> **Persistent Context Through Intelligent Documentation**
>
> This project uses ClineFlow to maintain persistent memory across AI assistant sessions through automatic journaling and intelligent commit workflows.

## 📚 Core Workflow

### MANDATORY: Every Task Must Have a Journal

**No Exceptions - All Tasks Require Documentation**

1. **Single Task**: Create `docs/journals/[task-name].md`
2. **Multi-Task Continuation**: Add new section to existing journal
3. **Use Template**: See `clineflow/JOURNAL_TEMPLATE.md`
4. **Update Regularly**: Journal progresses with each commit

**Multi-Task Pattern:**
- First task creates journal with Task 1 section
- Subsequent tasks add Task 2, Task 3, etc. sections to SAME journal
- Maintain task history index at top
- Keeps all related work in single source of truth

## 🚀 Intelligent Commit Command

**When user says:** `"commit changes"`, `"commit"`, or `"please commit"`

**Automatically:**
1. ✅ Detect active journal (most recent in `docs/journals/`)
2. ✅ Generate context-aware journal entry from conversation
3. ✅ Append entry to journal file
4. ✅ Stage ALL changes + updated journal
5. ✅ Create descriptive commit message
6. ✅ Execute `git commit`
7. ✅ Confirm completion

**Result**: Single commit with code changes + meaningful journal documentation

## 🏗️ Code Organization Standards

### Module/File Size Rules
- **Ideal Size**: 300-500 lines of code (LOC)
- **Maximum Size**: 1000 LOC (hard limit)
- **Over 1K LOC**: Unacceptable - must be refactored

### Design Principles
- **Single Responsibility**: Each file should have one clear purpose
- **Modular Composition**: Break large files into focused units
- **Code Quality**: No unnecessary code, specific to module purpose only

### Universal Application
These rules apply to ALL languages:
- Python classes
- JavaScript/TypeScript components
- Go packages
- Rust modules
- Java classes
- C++ files
- Any programming language

## 📋 Documentation Requirements

### Journal Structure
- Clear task descriptions
- Implementation status tracking
- Technical decisions explained
- Success criteria defined
- Issues and resolutions documented
- Quick reference for future work

### Commit Messages
- Descriptive and meaningful
- Reference journal entries when relevant
- Explain "why" not just "what"

## 🔄 Cross-Repository Code Access (Optional)

If using ClineFlow's reference system:
- Symlinks in `clineflow/` point to external repositories
- Access code from other projects without duplication
- Changes sync instantly via filesystem symlinks
- See `clineflow/README.md` for configuration details

## 🎯 Workflow Summary

1. **Start Task**: Create or identify journal
2. **Work Iteratively**: Document decisions as you go
3. **Commit Intelligently**: Use "please commit" command
4. **Resume Seamlessly**: Load journal context in next session

## 💡 Best Practices

- Keep journal entries concise but technically dense
- Document the "why" behind technical decisions
- Update journal before major commits
- Use multi-task pattern for related work
- Reference specific files and line numbers when relevant
- Include code snippets for complex explanations

## 🤝 Team Collaboration

- Journals serve as onboarding documentation
- New team members read journals to understand context
- Decision history preserved for entire project lifecycle
- No tribal knowledge - everything documented

---

**This configuration works with any AI coding assistant:**
- Cline
- Cursor
- GitHub Copilot
- Windsurf
- And more

For questions or issues, see: https://github.com/hassanvfx/clineflow
