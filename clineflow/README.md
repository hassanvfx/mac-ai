# Reference System

Link external repositories for Cline exploration via symlinks. This built-in feature allows Cline to access and explore code from other projects without copying files.

## Quick Start

```bash
# 1. Clone reference repos wherever you prefer
cd ~/projects  # or your preferred location
git clone https://github.com/your-org/backend-api
git clone https://github.com/your-org/frontend-app

# 2. Configure paths (back in your project)
cd ~/your-project
cp .clineflow.example .clineflow.local

# 3. Edit .clineflow.local with your repository paths
nano .clineflow.local

# Add your paths:
#   BACKEND_API_PATH="/Users/yourname/projects/backend-api"
#   FRONTEND_APP_PATH="/Users/yourname/projects/frontend-app"

# 4. Run the built-in setup script
./setup-refs.sh
```

## Usage

Once set up, reference files are accessible in multiple ways:

### Via Multi-Root Workspace (Recommended for @ Mentions)

For full @ mention autocomplete in Cline:

```bash
# Open the generated workspace file
code my-project.code-workspace
```

**Benefits:**
- ✅ **Full @ mention autocomplete** - All repos indexed by VS Code
- ✅ **IntelliSense works** - Code completion across all repositories
- ✅ **Search everywhere** - Find content across all linked repos
- ✅ **Side-by-side editing** - Work on multiple repos simultaneously

**@ Mention examples:**
- `@my-project/src/main.py`
- `@backend-api/api/routes/users.py`
- `@frontend-app/components/Button.tsx`

### Via Symlinks (File Browser Access)

Reference files are also accessible via symlinks at `clineflow/`:

- **File Browser**: Navigate via `clineflow/backend-api/...`
- **Terminal Commands**: All commands work normally with symlinks
- **Live Updates**: Changes in reference repos appear immediately (real symlinks)
- **Quick Access**: No need to switch workspaces for simple file viewing

## How It Works

The `setup-refs.sh` script (installed with ClineFlow):

1. Reads `.clineflow.local` configuration
2. Finds all variables ending with `_PATH`
3. Creates symlinks in `clineflow/` directory
4. **Generates `.code-workspace` file** with all repositories
5. Validates paths and reports status

**Dual Access:** You get both symlinks (for filesystem access) and a workspace file (for VS Code indexing and @ mention completion).

**Variable naming:** Variable names ending with `_PATH` automatically create symlinks. The symlink name is derived from the variable name:
- `BACKEND_API_PATH` → `clineflow/backend-api`
- `FRONTEND_APP_PATH` → `clineflow/frontend-app`
- `MY_TOOL_PATH` → `clineflow/my-tool`

## Integration with Build Tools

Integrate into your existing workflow:

```bash
# Node.js projects (package.json)
{
  "scripts": {
    "predev": "./setup-refs.sh",
    "postinstall": "./setup-refs.sh"
  }
}

# Python projects (Makefile)
.PHONY: dev
dev:
	./setup-refs.sh
	python manage.py runserver

# Go projects (Makefile)
.PHONY: build
build:
	./setup-refs.sh
	go build

# Or use git hooks
echo "./setup-refs.sh" > .git/hooks/post-checkout
chmod +x .git/hooks/post-checkout
```

## Adding New References

1. Clone the new repository to your preferred location
2. Add variable to `.clineflow.example` (optional, for team reference)
3. Add path variable to `.clineflow.local`:
   ```bash
   NEW_REPO_PATH="/path/to/new-repo"
   ```
4. Run `./setup-refs.sh` again - it will automatically create the new symlink

## Troubleshooting

### @ Mentions Not Working?

**Problem:** When typing `@` in Cline, symlinked files don't appear in autocomplete.

**Solution:** Open the workspace file instead of the folder:

```bash
# Close current VS Code window, then:
code my-project.code-workspace
```

**Why:** Symlinks provide filesystem access but VS Code doesn't automatically index them for @ mention completion. The multi-root workspace file tells VS Code to fully index all repositories.

**To regenerate workspace file:**
```bash
./setup-refs.sh  # Safe to run anytime, updates workspace file
```

### Symlinks Not Appearing?

- Check paths in `.clineflow.local` are correct
- Verify referenced repos exist at specified paths
- Ensure you have permission to create symlinks

### Need to Re-link?

```bash
# Remove old symlinks
rm clineflow/backend-api clineflow/frontend-app

# Re-run setup (also updates workspace file)
./setup-refs.sh
```

### Permission Issues?

```bash
# On Windows, symlinks may require admin privileges
# Consider using WSL or Git Bash with admin rights
```

### Workspace File vs Folder

**Opening folder directly:** `code .`
- ✅ Quick access
- ✅ Simple workflow
- ❌ Limited @ mention completion (symlinks not indexed)

**Opening workspace file:** `code project.code-workspace`
- ✅ Full @ mention autocomplete
- ✅ All repos indexed
- ✅ Better search and IntelliSense
- ℹ️ Requires closing and reopening VS Code

## Structure

```
your-project/
├── .clineflow.example           # Template (versioned)
├── .clineflow.local             # Your paths (gitignored)
├── setup-refs.sh                # Setup script
├── my-project.code-workspace    # Generated workspace (gitignored)
│
└── clineflow/
    ├── README.md                # This file
    ├── backend-api/             # → Symlink to your clone
    └── frontend-app/            # → Symlink to your clone
```

**Files automatically gitignored:**
- `.clineflow.local` - Contains developer-specific paths
- `*.code-workspace` - Contains absolute paths specific to each developer
- Symlinks in `clineflow/` - Via `.git/info/exclude` (local-only)

## Benefits

- **Full @ Mention Completion**: Workspace file enables autocomplete for all linked repos
- **No File Duplication**: Reference repos stay in their original location
- **Always Current**: Changes sync instantly via symlinks
- **Dual Access**: File browser via symlinks + full indexing via workspace
- **VSCode Integration**: Search, IntelliSense, and navigation work seamlessly
- **Team Flexibility**: Each developer can place repos anywhere via `.clineflow.local`
- **Idempotent Setup**: Safe to re-run `./setup-refs.sh` anytime

## Advanced Usage

### Workspace-Only Mode

Update workspace file without touching symlinks:

```bash
./setup-refs.sh --workspace-only
```

### Clean Mode

Remove all symlinks (workspace file unaffected):

```bash
./setup-refs.sh --clean
```

### Custom Workspace Settings

The generated workspace file includes VS Code settings optimized for symlink access. You can customize by editing `project-name.code-workspace`:

```json
{
  "folders": [
    { "name": "my-project", "path": "." },
    { "name": "backend-api", "path": "/path/to/backend-api" }
  ],
  "settings": {
    "search.followSymlinks": true,
    "files.watcherExclude": {
      "**/.git/objects/**": true,
      "**/node_modules/**": true
    }
  }
}
```
