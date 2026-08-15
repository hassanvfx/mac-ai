#!/bin/bash
# ClineFlow Reference System Setup Script
# Creates symlinks to external repositories for Cline exploration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration file
CONFIG_FILE=".clineflow.local"
EXAMPLE_CONFIG=".clineflow.example"
REFS_DIR="clineflow"

# Parse command line arguments
CLEAN_MODE=false
WORKSPACE_ONLY=false

show_help() {
    echo "ClineFlow Reference System Setup"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --clean           Remove all reference symlinks"
    echo "  --workspace-only  Generate/update workspace file only"
    echo "  --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Create symlinks + workspace file"
    echo "  $0 --clean            # Remove all symlinks"
    echo "  $0 --workspace-only   # Update workspace file only"
    echo ""
    exit 0
}

clean_symlinks() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}   Cleaning Reference Symlinks${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ ! -d "$REFS_DIR" ]; then
        echo -e "${YELLOW}⚠ No $REFS_DIR directory found${NC}"
        exit 0
    fi
    
    REMOVED_COUNT=0
    
    # Find and remove symlinks
    for link in "$REFS_DIR"/*; do
        if [ -L "$link" ]; then
            rm "$link"
            echo -e "${GREEN}✓ Removed: $(basename "$link")${NC}"
            REMOVED_COUNT=$((REMOVED_COUNT + 1))
        fi
    done
    
    echo ""
    if [ $REMOVED_COUNT -gt 0 ]; then
        echo -e "${GREEN}✓ Removed $REMOVED_COUNT symlink(s)${NC}"
    else
        echo -e "${YELLOW}⚠ No symlinks found to remove${NC}"
    fi
    echo ""
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN_MODE=true
            shift
            ;;
        --workspace-only)
            WORKSPACE_ONLY=true
            shift
            ;;
        --help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}✗ Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

if [ "$CLEAN_MODE" = true ]; then
    clean_symlinks
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   ClineFlow Reference System Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠ Configuration file not found: $CONFIG_FILE${NC}"
    if [ -f "$EXAMPLE_CONFIG" ]; then
        echo -e "${BLUE}ℹ Creating from example...${NC}"
        cp "$EXAMPLE_CONFIG" "$CONFIG_FILE"
        echo -e "${GREEN}✓ Created $CONFIG_FILE${NC}"
        echo -e "${YELLOW}⚠ Please edit $CONFIG_FILE with your repository paths${NC}"
        echo -e "${BLUE}  Then run this script again.${NC}"
    else
        echo -e "${RED}✗ Example config not found: $EXAMPLE_CONFIG${NC}"
        echo -e "${BLUE}  Please create $CONFIG_FILE manually${NC}"
    fi
    exit 1
fi

# Source the configuration
echo -e "${BLUE}ℹ Loading configuration from $CONFIG_FILE...${NC}"
source "$CONFIG_FILE"

# Create refs directory if it doesn't exist
if [ ! -d "$REFS_DIR" ]; then
    echo -e "${BLUE}ℹ Creating directory: $REFS_DIR/${NC}"
    mkdir -p "$REFS_DIR"
fi

# Track success
SUCCESS_COUNT=0
TOTAL_COUNT=0

# Function to configure git exclusion for symlinks
configure_git_exclude() {
    local exclude_file=".git/info/exclude"
    
    echo ""
    echo -e "${BLUE}ℹ Configuring git to ignore symlinks...${NC}"
    
    # Ensure git directory exists
    if [ ! -d ".git" ]; then
        echo -e "${YELLOW}⚠ Not a git repository - symlinks won't be auto-ignored${NC}"
        echo -e "${BLUE}  This is OK for testing, but in real projects run 'git init' first${NC}"
        return 1
    fi
    
    # Create exclude file if missing
    if [ ! -f "$exclude_file" ]; then
        mkdir -p "$(dirname "$exclude_file")"
        touch "$exclude_file"
    fi
    
    # Check if already configured
    if grep -q "# ClineFlow reference symlinks" "$exclude_file" 2>/dev/null; then
        echo -e "${GREEN}✓ Git exclusion already configured${NC}"
        return 0
    fi
    
    # Add exclusion rules
    cat >> "$exclude_file" << 'EOF'

# ClineFlow reference symlinks (local-only, not committed)
# These are developer-specific paths and should not be in version control
clineflow/*
!clineflow/*.md
!clineflow/.gitattributes
EOF
    
    echo -e "${GREEN}✓ Configured .git/info/exclude to ignore symlinks${NC}"
    echo -e "${BLUE}  (This is local-only and won't affect other developers)${NC}"
    return 0
}

# Function to check for staged symlinks
check_staged_symlinks() {
    # Only check if we're in a git repo
    if [ ! -d ".git" ]; then
        return 0
    fi
    
    # Check for staged symlinks (exclude .md and .gitattributes files)
    local staged_symlinks=$(git diff --cached --name-only 2>/dev/null | grep -E "^clineflow/[^/]+$" | grep -v "\.md$" | grep -v "\.gitattributes$")
    
    if [ -n "$staged_symlinks" ]; then
        echo ""
        echo -e "${RED}════════════════════════════════════════════════════════${NC}"
        echo -e "${RED}⚠  WARNING: Symlinks detected in staged files!${NC}"
        echo -e "${RED}════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${YELLOW}The following symlinks are staged for commit:${NC}"
        echo "$staged_symlinks" | sed 's/^/  - /'
        echo ""
        echo -e "${YELLOW}Symlinks should NOT be committed as they contain${NC}"
        echo -e "${YELLOW}developer-specific paths that won't work for others.${NC}"
        echo ""
        echo -e "${BLUE}To unstage: ${NC}git reset HEAD clineflow/*"
        echo ""
        return 1
    fi
    
    return 0
}

# Function to generate VS Code workspace file
generate_workspace_file() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Generating VS Code Workspace File...${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Detect project name from git or directory
    local project_name
    if [ -d ".git" ]; then
        project_name=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
    else
        project_name=$(basename "$(pwd)")
    fi
    
    local workspace_file="${project_name}.code-workspace"
    
    # Check if config file exists
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${YELLOW}⚠ Configuration file not found: $CONFIG_FILE${NC}"
        echo -e "${BLUE}  Workspace file requires repository paths${NC}"
        return 1
    fi
    
    # Start building workspace JSON
    local folders_json="    {\n      \"name\": \"${project_name}\",\n      \"path\": \".\"\n    }"
    local ref_count=0
    
    # Parse config file for *_PATH variables
    while IFS='=' read -r var_name var_value; do
        # Skip comments and empty lines
        [[ "$var_name" =~ ^#.*$ ]] && continue
        [[ -z "$var_name" ]] && continue
        
        # Check if variable ends with _PATH
        if [[ "$var_name" =~ _PATH$ ]]; then
            # Get the actual path value by sourcing the config
            source "$CONFIG_FILE"
            local target_path="${!var_name}"
            
            if [ -n "$target_path" ] && [ -d "$target_path" ]; then
                # Remove _PATH suffix and convert to readable name
                local folder_name=$(echo "${var_name%_PATH}" | tr '[:upper:]' '[:lower:]' | tr '_' '-')
                
                # Add to folders JSON
                folders_json="${folders_json},\n    {\n      \"name\": \"${folder_name}\",\n      \"path\": \"${target_path}\"\n    }"
                ref_count=$((ref_count + 1))
                
                echo -e "${GREEN}  ✓ Adding: ${folder_name} → ${target_path}${NC}"
            fi
        fi
    done < "$CONFIG_FILE"
    
    if [ $ref_count -eq 0 ]; then
        echo -e "${YELLOW}⚠ No valid repository paths found in $CONFIG_FILE${NC}"
        echo -e "${BLUE}  Workspace file will only include current project${NC}"
    fi
    
    # Generate complete workspace file
    cat > "$workspace_file" << EOF
{
  "folders": [
$(echo -e "$folders_json")
  ],
  "settings": {
    "search.followSymlinks": true,
    "files.watcherExclude": {
      "**/.git/objects/**": true,
      "**/.git/subtree-cache/**": true,
      "**/node_modules/**": true
    }
  }
}
EOF
    
    echo ""
    echo -e "${GREEN}✓ Generated workspace file: ${workspace_file}${NC}"
    echo -e "${BLUE}  Project: ${project_name}${NC}"
    echo -e "${BLUE}  References: ${ref_count} repositor$([ $ref_count -eq 1 ] && echo "y" || echo "ies")${NC}"
    
    return 0
}

# Function to create symlink
create_symlink() {
    local var_name="$1"
    local link_name="$2"
    local target_path="${!var_name}"
    
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    
    if [ -z "$target_path" ]; then
        return # Skip if variable is not set
    fi
    
    echo -e "${BLUE}ℹ Processing: $link_name${NC}"
    
    # Check if target exists
    if [ ! -d "$target_path" ]; then
        echo -e "${YELLOW}  ⚠ Target not found: $target_path${NC}"
        echo -e "${YELLOW}    Skipping $link_name${NC}"
        return
    fi
    
    local link_path="$REFS_DIR/$link_name"
    
    # Remove existing symlink if it exists
    if [ -L "$link_path" ]; then
        echo -e "${BLUE}  ℹ Removing existing symlink${NC}"
        rm "$link_path"
    elif [ -e "$link_path" ]; then
        echo -e "${RED}  ✗ Path exists but is not a symlink: $link_path${NC}"
        echo -e "${RED}    Please remove it manually${NC}"
        return
    fi
    
    # Create symlink
    ln -sf "$target_path" "$link_path"
    echo -e "${GREEN}  ✓ Created symlink: $link_name → $target_path${NC}"
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
}

# Handle workspace-only mode
if [ "$WORKSPACE_ONLY" = true ]; then
    generate_workspace_file
    exit $?
fi

# Parse config file for *_PATH variables and create symlinks
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Creating symlinks...${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

while IFS='=' read -r var_name var_value; do
    # Skip comments and empty lines
    [[ "$var_name" =~ ^#.*$ ]] && continue
    [[ -z "$var_name" ]] && continue
    
    # Check if variable ends with _PATH
    if [[ "$var_name" =~ _PATH$ ]]; then
        # Remove _PATH suffix and convert to lowercase for link name
        link_name=$(echo "${var_name%_PATH}" | tr '[:upper:]' '[:lower:]' | tr '_' '-')
        create_symlink "$var_name" "$link_name"
    fi
done < "$CONFIG_FILE"

# Configure git exclusion
configure_git_exclude

# Check for accidentally staged symlinks
check_staged_symlinks

# Generate workspace file
generate_workspace_file

# Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
if [ $SUCCESS_COUNT -gt 0 ]; then
    echo -e "${GREEN}✓ Setup Complete!${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}Created Symlinks:${NC}"
    echo -e "  $SUCCESS_COUNT symlink(s) in $REFS_DIR/"
    echo ""
    echo -e "${GREEN}Git Configuration:${NC}"
    echo -e "  ✓ Symlinks configured as local-only (not committed)"
    echo -e "  ✓ Located in .git/info/exclude"
    echo ""
    
    # Detect workspace file name
    local project_name
    if [ -d ".git" ]; then
        project_name=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
    else
        project_name=$(basename "$(pwd)")
    fi
    local workspace_file="${project_name}.code-workspace"
    
    echo -e "${GREEN}VS Code Workspace:${NC}"
    echo -e "  ✓ Generated ${workspace_file}"
    echo ""
    echo -e "${BLUE}📚 For @ Mention Completion in Cline:${NC}"
    echo -e "  ${GREEN}code ${workspace_file}${NC}"
    echo ""
    echo -e "  This enables autocomplete for @ mentions:"
    echo -e "  • @${project_name}/your/file.md"
    echo -e "  • @backend-api/src/main.py"
    echo -e "  • @frontend-app/components/Button.tsx"
    echo ""
    echo -e "${BLUE}📂 File Browser Access:${NC}"
    echo -e "  • Symlinks visible in VS Code explorer"
    echo -e "  • Direct path: clineflow/[name]/path/to/file"
    echo ""
    echo -e "${BLUE}🔒 Git Safety:${NC}"
    echo -e "  • Symlinks won't be committed (local-only)"
    echo -e "  • No conflicts with other developers"
    echo -e "  • Each dev has their own repository paths"
    echo ""
else
    echo -e "${YELLOW}⚠ No symlinks created${NC}"
    echo -e "${BLUE}ℹ Make sure $CONFIG_FILE has valid repository paths${NC}"
fi
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
