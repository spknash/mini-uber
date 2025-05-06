#!/usr/bin/env python3

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

def run_pytest() -> tuple[int, str, str]:
    """Run pytest and return exit code, stdout, and stderr."""
    try:
        result = subprocess.run(
            ["pytest", "tests", "-v"],
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", f"Failed to run pytest: {str(e)}"

def parse_pytest_output(stdout: str) -> List[Dict[str, Any]]:
    """Parse pytest output and convert to test results format."""
    results = []
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Split output into lines and process each test result
    for line in stdout.split('\n'):
        if not line.strip() or '::' not in line:
            continue
            
        try:
            # Parse test path and result
            test_path, result = line.strip().rsplit(' ', 1)
            test_parts = test_path.split('::')
            
            # Extract module and test name
            file_path = test_parts[0].strip()
            test_name = test_parts[-1] if len(test_parts) > 1 else "unknown"
            
            # Extract module and category from file path
            path_parts = file_path.split('/')
            module = path_parts[1] if len(path_parts) > 1 else "unknown"
            category = path_parts[2] if len(path_parts) > 2 else "unknown"
            
            # Map pytest result to status
            status_map = {
                "PASSED": "passed",
                "FAILED": "failed",
                "SKIPPED": "skipped",
                "ERROR": "error"
            }
            status = status_map.get(result, "unknown")
            
            results.append({
                "module": module,
                "category": category,
                "test_name": test_name,
                "status": status,
                "output": line.strip(),
                "attempted_at": timestamp,
                "completed_at": timestamp
            })
            
        except Exception as e:
            results.append({
                "module": "error",
                "category": "error",
                "test_name": "parse_error",
                "status": "error",
                "output": f"Error parsing test output: {str(e)}\nLine: {line}",
                "attempted_at": timestamp,
                "completed_at": timestamp
            })
    
    # If no results were parsed, add an error entry
    if not results:
        results.append({
            "module": "error",
            "category": "error",
            "test_name": "no_tests",
            "status": "error",
            "output": f"No test results found in output:\n{stdout}",
            "attempted_at": timestamp,
            "completed_at": timestamp
        })
    
    return results

def upload_to_supabase(results: List[Dict[str, Any]]) -> bool:
    """Upload results to Supabase."""
    import requests
    
    try:
        url = "https://xqfwqvbfjhxwqgrdcjck.supabase.co/rest/v1/user_projects"
        headers = {
            "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhxZndxdmJmamh4d3FncmRjamNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI5MjE5NDEsImV4cCI6MjAxODQ5Nzk0MX0.ZNgjwuqmwXGdWwx3xV6EXG8pGHvpAxDOQOADxgMFSXc",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhxZndxdmJmamh4d3FncmRjamNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI5MjE5NDEsImV4cCI6MjAxODQ5Nzk0MX0.ZNgjwuqmwXGdWwx3xV6EXG8pGHvpAxDOQOADxgMFSXc",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        data = {
            "id": "4600c943-a7f9-4efc-ad50-615921f9bf00",
            "tests_status": results
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code not in (200, 201):
            print(f"Error uploading to Supabase. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Failed to upload to Supabase: {str(e)}")
        return False

def main():
    """Main function to run tests and process results."""
    try:
        # Run pytest and collect output
        exit_code, stdout, stderr = run_pytest()
        
        # Parse the output into our format
        results = parse_pytest_output(stdout)
        
        # If there was an error running pytest, add it to results
        if exit_code != 0 and stderr:
            timestamp = datetime.now(timezone.utc).isoformat()
            results.append({
                "module": "error",
                "category": "error",
                "test_name": "pytest_error",
                "status": "error",
                "output": f"Pytest error (exit code {exit_code}):\n{stderr}",
                "attempted_at": timestamp,
                "completed_at": timestamp
            })
        
        # Print results to stdout (for logging)
        print("Test Results:")
        print(json.dumps(results, indent=2))
        
        # Upload results to Supabase
        if upload_to_supabase(results):
            print("Successfully uploaded results to Supabase")
        else:
            print("Failed to upload results to Supabase")
            sys.exit(1)
        
    except Exception as e:
        timestamp = datetime.now(timezone.utc).isoformat()
        error_result = [{
            "module": "error",
            "category": "error",
            "test_name": "script_error",
            "status": "error",
            "output": f"Script error: {str(e)}",
            "attempted_at": timestamp,
            "completed_at": timestamp
        }]
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main() 
