#!/usr/bin/env python3
"""Check for Latter-day Saint mentions in 2nd pass JSON files."""

import os
import json
import glob

def check_lds_mentions(json_dir: str = "json/3rd_pass_json"):
    """Check all JSON files for Latter-day Saint or Mormon mentions."""
    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    
    search_terms = ['latter-day saint', 'latter-day saints', 'mormon']
    found_files = []
    
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            for term in search_terms:
                if term in content:
                    found_files.append((os.path.basename(jf), term))
                    break
        except Exception as e:
            print(f"Error reading {jf}: {e}")
    
    if found_files:
        print(f"Found {len(found_files)} file(s) with LDS/Mormon mentions:\n")
        for filename, term in found_files:
            print(f"  - {filename} (matched: '{term}')")
    else:
        print("No files found with Latter-day Saint or Mormon mentions.")
    
    return found_files


if __name__ == "__main__":
    check_lds_mentions()
