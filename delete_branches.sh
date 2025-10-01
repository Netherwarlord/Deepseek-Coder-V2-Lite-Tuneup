#!/bin/bash
# Script to delete all branches except 'main' from the repository
# Usage: ./delete_branches.sh [--dry-run]

set -e

REPO_OWNER="Netherwarlord"
REPO_NAME="Deepseek-Coder-V2-Lite-Tuneup"
DRY_RUN=false

# Check for dry-run flag
if [[ "$1" == "--dry-run" ]] || [[ "$1" == "-n" ]]; then
    DRY_RUN=true
    echo "Running in DRY RUN mode (no changes will be made)"
    echo ""
fi

# Fetch all branches
echo "Fetching all branches..."
git fetch --all --prune

# Get all remote branches except main
branches=$(git branch -r | grep -v '\->' | grep -v 'origin/main' | sed 's/origin\///' | xargs)

if [ -z "$branches" ]; then
    echo "No branches to delete. Only 'main' exists."
    exit 0
fi

echo "The following branches will be deleted:"
for branch in $branches; do
    echo "  - $branch"
done

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "Dry run mode - no branches were deleted."
    exit 0
fi

# Ask for confirmation
echo ""
read -p "Are you sure you want to delete these branches? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

# Delete each branch
echo ""
echo "Deleting branches..."
for branch in $branches; do
    if git push origin --delete "$branch" 2>/dev/null; then
        echo "✓ Deleted: $branch"
    else
        echo "✗ Failed to delete: $branch"
    fi
done

echo ""
echo "Branch cleanup complete!"
