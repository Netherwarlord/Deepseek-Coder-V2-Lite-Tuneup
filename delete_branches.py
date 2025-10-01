#!/usr/bin/env python3
"""
Script to delete all branches except 'main' from the GitHub repository.

This script uses the GitHub API to delete all branches except 'main'.
You need to have a GitHub personal access token with repo permissions.

Usage:
    python3 delete_branches.py <github_token>

Or set the GITHUB_TOKEN environment variable:
    export GITHUB_TOKEN=your_token_here
    python3 delete_branches.py
"""

import os
import sys
import requests


def delete_branches(owner, repo, token, dry_run=False):
    """
    Delete all branches except 'main' from the specified GitHub repository.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        token: GitHub personal access token
        dry_run: If True, only show what would be deleted without actually deleting
    """
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get all branches
    url = f'https://api.github.com/repos/{owner}/{repo}/git/refs/heads'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching branches: {response.status_code}")
        print(response.text)
        return False
    
    branches = response.json()
    
    # Filter out 'main' branch
    branches_to_delete = [b for b in branches if not b['ref'].endswith('/main')]
    
    if not branches_to_delete:
        print("No branches to delete. Only 'main' exists.")
        return True
    
    print(f"Found {len(branches_to_delete)} branch(es) to delete:")
    for branch in branches_to_delete:
        branch_name = branch['ref'].replace('refs/heads/', '')
        print(f"  - {branch_name}")
    
    if dry_run:
        print("\nDry run mode - no branches were deleted.")
        return True
    
    print("\nDeleting branches...")
    success_count = 0
    failed_count = 0
    
    for branch in branches_to_delete:
        branch_ref = branch['ref']
        branch_name = branch_ref.replace('refs/heads/', '')
        
        delete_url = f'https://api.github.com/repos/{owner}/{repo}/git/{branch_ref}'
        delete_response = requests.delete(delete_url, headers=headers)
        
        if delete_response.status_code == 204:
            print(f"✓ Deleted: {branch_name}")
            success_count += 1
        else:
            print(f"✗ Failed to delete {branch_name}: {delete_response.status_code}")
            print(f"  {delete_response.text}")
            failed_count += 1
    
    print(f"\nSummary: {success_count} deleted, {failed_count} failed")
    return failed_count == 0


def main():
    # Repository details
    owner = "Netherwarlord"
    repo = "Deepseek-Coder-V2-Lite-Tuneup"
    
    # Get token from command line or environment variable
    token = None
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print("Error: GitHub token not provided.")
        print("Usage: python3 delete_branches.py <github_token>")
        print("Or set GITHUB_TOKEN environment variable")
        sys.exit(1)
    
    # Check if dry run
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    if dry_run:
        print("Running in DRY RUN mode (no changes will be made)\n")
    else:
        print("WARNING: This will DELETE all branches except 'main'")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)
    
    success = delete_branches(owner, repo, token, dry_run)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
