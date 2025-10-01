import json
import glob
import os

def combine_json_batches(output_filename=".data/training_dataset_final.json"):
    """
    Finds all 'training_dataset_batch_*.json' files in the .data directory,
    combines them, removes exact duplicates based on the 'instruction' field,
    and saves the unique pairs to a new JSON file.
    """
    batch_files = sorted(glob.glob(".data/training_dataset_batch_*.json"))
    
    if not batch_files:
        print("Error: No batch files found with the pattern '.data/training_dataset_batch_*.json'")
        return

    print(f"Found {len(batch_files)} batch files to combine.")

    combined_data = []
    seen_instructions = set()
    total_pairs = 0
    duplicate_count = 0

    for file_path in batch_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        total_pairs += 1
                        # Use the 'instruction' field as the unique identifier
                        instruction = item.get('instruction')
                        if instruction and instruction not in seen_instructions:
                            seen_instructions.add(instruction)
                            combined_data.append(item)
                        else:
                            duplicate_count += 1
                else:
                    print(f"Warning: File '{file_path}' does not contain a JSON array and will be skipped.")
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from '{file_path}'. File will be skipped.")
        except Exception as e:
            print(f"An error occurred while processing '{file_path}': {e}")

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=4)
        
        print(f"\nProcessed {total_pairs} total pairs from {len(batch_files)} files.")
        print(f"Removed {duplicate_count} duplicate pairs.")
        print(f"Successfully combined {len(combined_data)} unique instruction pairs into '{output_filename}'.")
        print("You are now ready for Phase 3: Fine-Tuning on AWS.")

    except Exception as e:
        print(f"\nAn error occurred while writing the final file: {e}")


if __name__ == "__main__":
    combine_json_batches()

