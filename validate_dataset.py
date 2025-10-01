import json
import os
import subprocess
import time
import re

# --- USER CONFIGURATION ---
# IMPORTANT: You must create a separate, blank Xcode project for each platform
# and provide the correct paths below.

DATASET_FILE_PATH = "training_dataset_final.json"

# --- Validation Harness Project Paths ---
# Create one simple project for each platform and fill in the paths.
# The script will detect the platform and choose the correct project.

HARNESS_CONFIG = {
    "ios": {
        "project_path": "/path/to/your/ValidationHarness_iOS/ValidationHarness_iOS.xcodeproj",
        "swift_file": "/path/to/your/ValidationHarness_iOS/ValidationHarness_iOS/ContentView.swift"
    },
    "macos": {
        "project_path": "/path/to/your/ValidationHarness_macOS/ValidationHarness_macOS.xcodeproj",
        "swift_file": "/path/to/your/ValidationHarness_macOS/ValidationHarness_macOS/ContentView.swift"
    },
    "visionos": {
        "project_path": "/path/to/your/ValidationHarness_visionOS/ValidationHarness_visionOS.xcodeproj",
        "swift_file": "/path/to/your/ValidationHarness_visionOS/ValidationHarness_visionOS/ContentView.swift"
    },
    "watchos": {
        "project_path": "/path/to/your/ValidationHarness_watchOS/ValidationHarness_watchOS.xcodeproj",
        "swift_file": "/path/to/your/ValidationHarness_watchOS/ValidationHarness_watchOS Watch App/ContentView.swift" # Note the different path for watchOS apps
    },
    "tvos": {
        "project_path": "/path/to/your/ValidationHarness_tvOS/ValidationHarness_tvOS.xcodeproj",
        "swift_file": "/path/to/your/ValidationHarness_tvOS/ValidationHarness_tvOS/ContentView.swift"
    }
}


# --- SCRIPT LOGIC ---

def detect_platform(swift_code, instruction):
    """Detects the target platform based on keywords in the code or instruction."""
    instruction = instruction.lower()
    if "visionos" in instruction or "realitykit" in swift_code or "immersive" in swift_code:
        return "visionos"
    if "watchos" in instruction or "complication" in swift_code or "digitalcrown" in swift_code:
        return "watchos"
    if "macos" in instruction or "menubar" in swift_code or "nsviewrepresentable" in swift_code:
        return "macos"
    if "tvos" in instruction or "focus" in swift_code:
        return "tvos"
    # Default to iOS if no other specific platform is detected
    return "ios"

def validate_swift_code(swift_code, platform):
    """Writes Swift code to the appropriate file and compiles for the detected platform."""
    config = HARNESS_CONFIG.get(platform)
    if not config:
        return False, f"Configuration for platform '{platform}' not found."

    project_path = config["project_path"]
    swift_file = config["swift_file"]

    try:
        with open(swift_file, "w", encoding="utf-8") as f:
            f.write(swift_code)
    except IOError as e:
        return False, f"Error writing to Swift file: {e}"

    # Select the correct build destination based on the platform
    destination = {
        "ios": "platform=iOS Simulator,name=iPhone 15 Pro",
        "macos": "platform=macOS,arch=arm64",
        "visionos": "platform=visionOS Simulator,name=Apple Vision Pro",
        "watchos": "platform=watchOS Simulator,name=Apple Watch Series 9 (45mm)",
        "tvos": "platform=tvOS Simulator,name=Apple TV 4K (3rd generation)"
    }.get(platform)

    command = [
        "xcodebuild",
        "-project", project_path,
        "-scheme", os.path.basename(project_path).replace(".xcodeproj", ""),
        "-destination", destination,
        "build"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return True, "Build Succeeded"
        else:
            return False, result.stdout + "\n" + result.stderr
    except Exception as e:
        return False, f"An unexpected error occurred during build: {e}"

def main():
    if not os.path.exists(DATASET_FILE_PATH):
        print(f"Error: Dataset file not found at '{DATASET_FILE_PATH}'")
        return

    # Basic check to ensure paths are configured
    for p, conf in HARNESS_CONFIG.items():
        if "/path/to/your" in conf["project_path"]:
            print(f"ERROR: Please configure the paths in the HARNESS_CONFIG section at the top of the script.")
            print(f"Path for '{p}' is not set.")
            return

    with open(DATASET_FILE_PATH, "r", encoding="utf-8") as f:
        all_pairs = json.load(f)

    good_pairs, bad_pairs = [], []
    total_count = len(all_pairs)
    print(f"Starting validation for {total_count} pairs...")
    start_time = time.time()

    for i, pair in enumerate(all_pairs):
        swift_code = pair.get("output", "")
        instruction = pair.get("instruction", "")
        
        platform = detect_platform(swift_code, instruction)
        print(f"Validating pair {i + 1}/{total_count} (Platform: {platform.upper()})... ", end="", flush=True)
        
        is_valid, log = validate_swift_code(swift_code, platform)
        
        if is_valid:
            print("PASSED")
            good_pairs.append(pair)
        else:
            print("FAILED")
            bad_pairs.append({"instruction": instruction, "failed_output": swift_code, "error_log": log})
    
    end_time = time.time()
    print(f"\nValidation complete in {end_time - start_time:.2f} seconds.")

    clean_filename = "training_dataset_clean.json"
    failed_filename = "failed_pairs.json"

    with open(clean_filename, "w", encoding="utf-8") as f:
        json.dump(good_pairs, f, indent=4)
    print(f"✅ Successfully wrote {len(good_pairs)} valid pairs to '{clean_filename}'.")

    with open(failed_filename, "w", encoding="utf-8") as f:
        json.dump(bad_pairs, f, indent=4)
    print(f"❌ Isolated {len(bad_pairs)} failed pairs in '{failed_filename}' for review.")

if __name__ == "__main__":
    main()

