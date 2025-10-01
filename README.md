# Deepseek-Coder-V2-Lite-Tuneup

Training dataset management and validation tools for SwiftUI code generation.

## Project Overview

This repository contains tools for managing, combining, and validating training datasets for fine-tuning AI models on SwiftUI code generation across multiple Apple platforms (iOS, macOS, visionOS, watchOS, tvOS).

## Tools

### Dataset Management
- **`gui.py`** - GUI application for managing training dataset batches
- **`combiner.py`** - Combines multiple batch files and removes duplicates
- **`validate_dataset.py`** - Validates Swift code across different Apple platforms

### Branch Management
- **`delete_branches.sh`** - Quick shell script to delete all non-main branches
- **`delete_branches.py`** - Python script using GitHub API to delete branches
- **`.github/workflows/delete_branches.yml`** - GitHub Actions workflow for automated cleanup

For detailed instructions on cleaning up branches, see [BRANCH_CLEANUP.md](BRANCH_CLEANUP.md).

## Quick Start

### Managing Training Data

1. **Move a batch file:**
   ```bash
   python3 gui.py
   ```
   Click "Move Batch" to import a new training dataset batch.

2. **Check uniqueness:**
   Click "Check Uniqueness" to see how many unique instructions exist.

3. **Build final dataset:**
   Click "Build Final Dataset" to combine all batches into `training_dataset_final.json`.

4. **Validate dataset:**
   Click "Validate Dataset" to compile and test all Swift code examples.

### Branch Cleanup

To delete all branches except `main`:

**Quick method (recommended):**
```bash
./delete_branches.sh --dry-run  # Preview what will be deleted
./delete_branches.sh            # Actually delete branches
```

**Using GitHub Actions:**
1. Go to Actions tab in GitHub
2. Select "Delete All Branches Except Main"
3. Click "Run workflow"

For more methods and details, see [BRANCH_CLEANUP.md](BRANCH_CLEANUP.md).

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── delete_branches.yml    # Branch cleanup workflow
├── trainingData/                   # Training dataset batches
├── gui.py                          # Dataset management GUI
├── combiner.py                     # Batch combiner script
├── validate_dataset.py             # Code validation script
├── delete_branches.sh              # Branch cleanup shell script
├── delete_branches.py              # Branch cleanup Python script
├── BRANCH_CLEANUP.md               # Branch cleanup guide
└── README.md                       # This file
```

## Requirements

- Python 3.x
- Git
- Xcode (for validation)
- `requests` library (for Python script): `pip install requests`

## License

See repository license file for details.
