import json
import sys

def bandit_json_to_sarif(bandit_json_path, sarif_output_path):
    with open(bandit_json_path, 'r') as f:
        data = json.load(f)

    results = []
    for result in data.get("results", []):
        results.append({
            "ruleId": result["test_id"],
            "message": {"text": result["issue_text"]},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": result["filename"]},
                    "region": {
                        "startLine": result["line_number"]
                    }
                }
            }]
        })

    sarif_report = {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "bandit",
                    "rules": []
                }
            },
            "results": results
        }]
    }

    with open(sarif_output_path, 'w') as f:
        json.dump(sarif_report, f, indent=2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    bandit_json_to_sarif(args.input, args.output)
