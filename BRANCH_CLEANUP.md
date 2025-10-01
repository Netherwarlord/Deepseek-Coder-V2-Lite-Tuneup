# Branch Cleanup Guide

This guide explains how to delete all branches except `main` from the repository.

## Current Branches

The repository currently has the following branches:
- `main` (should be kept)
- `copilot/fix-2a74fc0a-2402-48d0-a93c-38534940e595` (should be deleted)
- `copilot/fix-d24c424b-59bc-4496-b7b8-def5e929c94b` (should be deleted)

## Methods to Delete Branches

### Method 1: Using GitHub Web Interface (Recommended for Manual Cleanup)

1. Go to https://github.com/Netherwarlord/Deepseek-Coder-V2-Lite-Tuneup/branches
2. For each branch (except `main`):
   - Click the trash icon next to the branch name
   - Confirm the deletion

### Method 2: Using GitHub Actions Workflow (Automated)

1. Go to the Actions tab in your GitHub repository
2. Select "Delete All Branches Except Main" workflow
3. Click "Run workflow"
4. Confirm and wait for the workflow to complete

This will automatically delete all branches except `main`.

### Method 3: Using the Python Script

You need a GitHub personal access token with `repo` permissions.

**Dry run (preview what will be deleted):**
```bash
python3 delete_branches.py YOUR_GITHUB_TOKEN --dry-run
```

**Actually delete the branches:**
```bash
python3 delete_branches.py YOUR_GITHUB_TOKEN
```

Or using environment variable:
```bash
export GITHUB_TOKEN=YOUR_GITHUB_TOKEN
python3 delete_branches.py
```

### Method 4: Using Git Commands

**From your local machine:**

```bash
# Fetch all branches
git fetch --all

# Delete remote branches (one by one)
git push origin --delete copilot/fix-2a74fc0a-2402-48d0-a93c-38534940e595
git push origin --delete copilot/fix-d24c424b-59bc-4496-b7b8-def5e929c94b

# Or use a loop to delete all non-main branches
for branch in $(git branch -r | grep -v '\->' | grep -v 'origin/main' | sed 's/origin\///'); do
  git push origin --delete "$branch"
done
```

### Method 5: Using GitHub CLI (gh)

If you have GitHub CLI installed:

```bash
# List all branches
gh api repos/Netherwarlord/Deepseek-Coder-V2-Lite-Tuneup/branches

# Delete branches
gh api -X DELETE repos/Netherwarlord/Deepseek-Coder-V2-Lite-Tuneup/git/refs/heads/copilot/fix-2a74fc0a-2402-48d0-a93c-38534940e595
gh api -X DELETE repos/Netherwarlord/Deepseek-Coder-V2-Lite-Tuneup/git/refs/heads/copilot/fix-d24c424b-59bc-4496-b7b8-def5e929c94b
```

## Verification

After deletion, verify that only `main` branch remains:

```bash
# Using git
git ls-remote --heads origin

# Using GitHub CLI
gh api repos/Netherwarlord/Deepseek-Coder-V2-Lite-Tuneup/branches

# Or visit: https://github.com/Netherwarlord/Deepseek-Coder-V2-Lite-Tuneup/branches
```

## Notes

- Branch deletions are permanent and cannot be undone through normal means
- Make sure you don't have any important uncommitted work in the branches being deleted
- The `main` branch will always be preserved
- If you need to recover a deleted branch, you can use the branch's SHA to recreate it within 90 days
