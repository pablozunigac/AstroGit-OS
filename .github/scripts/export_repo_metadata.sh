#!/usr/bin/env bash

set -euo pipefail

# -----------------------------------------------------------------------------
# AstroGit-OS - Consolidated Repository Metadata Extractor
# Script: .github/scripts/export_repo_metadata.sh
# Output: .github/scripts/export_repo_metadata.json
# -----------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_FILE="${SCRIPT_DIR}/export_repo_metadata.json"

echo "🔍 Extracting complete metadata from AstroGit-OS..."

if ! command -v gh &> /dev/null; then
    echo "❌ Error: 'gh' CLI is not installed."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Error: 'git' is not installed."
    exit 1
fi

REPO_NAME=$(gh repo view --json nameWithOwner -q .nameWithOwner)

python3 - "$REPO_NAME" "$OUTPUT_FILE" <<'EOF'
import sys
import json
import subprocess

repo_name = sys.argv[1]
output_file = sys.argv[2]

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return None

def run_json(cmd):
    out = run_cmd(cmd)
    if out:
        try:
            return json.loads(out)
        except Exception:
            return out
    return []

print(" ├─ Extracting general data & repo branches...")
repo_info = run_json(f"gh repo view {repo_name} --json name,owner,description,isPrivate,defaultBranchRef,stargazerCount,forkCount")
branches = run_json(f"gh api repos/{repo_name}/branches --paginate")

print(" ├─ Extracting tags & milestones...")
labels = run_json(f"gh api repos/{repo_name}/labels --paginate")
milestones = run_json(f"gh api repos/{repo_name}/milestones --paginate")

print(" ├─ Extracting issues & comments...")
issues = run_json(f"gh issue list --repo {repo_name} --state all --limit 1000 --json number,title,body,state,labels,assignees,milestone,createdAt,updatedAt,closedAt,comments")

print(" ├─ Extracting pull requests & reviews...")
prs = run_json(f"gh pr list --repo {repo_name} --state all --limit 1000 --json number,title,body,state,labels,assignees,milestone,createdAt,updatedAt,closedAt,mergedAt,comments,reviews")

print(" ├─ Mapping file tree & commits...")
file_tree = (run_cmd("git ls-tree -r --name-only HEAD") or "").splitlines()
commits_raw = run_cmd("git log --oneline -n 100")
commits = commits_raw.splitlines() if commits_raw else []

data = {
    "repository": repo_info,
    "branches": branches,
    "labels": labels,
    "milestones": milestones,
    "file_tree": file_tree,
    "recent_commits": commits,
    "issues": issues,
    "pull_requests": prs
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

EOF

echo "✅ Successful extraction. File available in ${OUTPUT_FILE}"