#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional

def safe_get_module_category(nodeid: str) -> tuple[str, str]:
    """Extract module and category from test nodeid."""
    try:
        parts = nodeid.split("::", 1)[0].split("/")
        if len(parts) >= 4:
            return parts[1], parts[2]
        return "unknown", "unknown"
    except Exception:
        return "unknown", "unknown"

def process_test_result(test: Dict[str, Any], timestamp: str) -> Dict[str, Any]:
    """Process a single test result into the required format."""
    module, category = safe_get_module_category(test.get("nodeid", ""))
    name = test.get("nodeid", "unknown").split("::")[-1]
    status = "passed" if test.get("outcome") == "passed" else "failed"
    output = test.get("call", {}).get("longrepr", "No detailed output available")
    
    return {
        "module": module,
        "category": category,
        "test_name": name,
        "status": status,
        "output": str(output),
        "attempted_at": timestamp,
        "completed_at": timestamp
    }

def create_error_result(error_type: str, error_message: str, timestamp: str) -> Dict[str, Any]:
    """Create an error result entry."""
    return {
        "module": "error",
        "category": "error",
        "test_name": f"error_{error_type}",
        "status": "error",
        "output": f"Error {error_type}: {error_message}",
        "attempted_at": timestamp,
        "completed_at": timestamp
    }

def main():
    """Main function to process test results."""
    try:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Read the report file
        report_path = Path("test_output/report.json")
        if not report_path.exists():
            json.dump([create_error_result("no_report", "No test report file found", timestamp)], sys.stdout)
            return
            
        with report_path.open() as f:
            report = json.load(f)
        
        # Process test results
        results = []
        for test in report.get("tests", []):
            try:
                result = process_test_result(test, timestamp)
                results.append(result)
            except Exception as e:
                results.append(create_error_result("processing_test", str(e), timestamp))
        
        # Output results as JSON
        json.dump(results, sys.stdout, indent=2)
        
    except Exception as e:
        json.dump([create_error_result("processing_report", str(e), timestamp)], sys.stdout)

if __name__ == "__main__":
    main() 
