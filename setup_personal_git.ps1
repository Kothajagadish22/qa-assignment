# =============================================================================
# Personal Git setup — THIS FOLDER ONLY (does NOT change global/company config)
# =============================================================================
# Run from: C:\Users\Anakin\Desktop\Assigment
#   .\setup_personal_git.ps1
#
# Or with your details:
#   .\setup_personal_git.ps1 -GitHubUsername "your-github-username" -GitName "Your Name" -GitEmail "you@gmail.com"
# =============================================================================

param(
    [string]$GitHubUsername = "Kothajagadish22",
    [string]$GitName = "Kothajagadish22",
    [string]$GitEmail = "19pa1a0345@vishnu.edu.in"
)

$ErrorActionPreference = "Stop"
$RepoRoot = $PSScriptRoot
Set-Location $RepoRoot

Write-Host ""
Write-Host "=== Personal Git setup (local to this folder only) ===" -ForegroundColor Cyan
Write-Host ""

# --- Collect personal details ---
if (-not $GitHubUsername) {
    $GitHubUsername = Read-Host "Your personal GitHub username (e.g. anakin-dev)"
}
if (-not $GitName) {
    $GitName = Read-Host "Your personal Git name (e.g. Anakin Skywalker)"
}
if (-not $GitEmail) {
    $GitEmail = Read-Host "Your personal Git email (must match GitHub account)"
}

# --- Init repo if needed ---
if (-not (Test-Path ".git")) {
    git init
    Write-Host "Created new git repo in: $RepoRoot" -ForegroundColor Green
} else {
    Write-Host "Git repo already exists." -ForegroundColor Yellow
}

# --- LOCAL config only (never touches global/company settings) ---
git config --local user.name "$GitName"
git config --local user.email "$GitEmail"

# Default branch
git config --local init.defaultBranch main

# Optional: use a dedicated SSH key for this repo only (uncomment after creating the key)
# $sshKey = "$env:USERPROFILE\.ssh\id_ed25519_personal_github"
# if (Test-Path $sshKey) {
#     git config --local core.sshCommand "ssh -i `"$sshKey`" -o IdentitiesOnly=yes"
#     Write-Host "Using personal SSH key: $sshKey" -ForegroundColor Green
# }

Write-Host ""
Write-Host "--- Verification (local vs global) ---" -ForegroundColor Cyan
Write-Host "LOCAL  (this folder only):"
Write-Host "  user.name  = $(git config --local user.name)"
Write-Host "  user.email = $(git config --local user.email)"
Write-Host ""
Write-Host "GLOBAL (other folders - unchanged):"
Write-Host "  user.name  = $(git config --global user.name)"
Write-Host "  user.email = $(git config --global user.email)"
Write-Host ""

# --- Remote (only if repo has no origin yet) ---
$existingRemote = git remote get-url origin 2>$null
if (-not $existingRemote) {
    $repoName = Read-Host "GitHub repo name for this project (e.g. qa-assignment)"
    if ($repoName) {
        Write-Host ""
        Write-Host "Add remote AFTER you create the repo on GitHub:" -ForegroundColor Yellow
        Write-Host "  HTTPS: git remote add origin https://github.com/$GitHubUsername/$repoName.git"
        Write-Host "  SSH:   git remote add origin git@github.com:$GitHubUsername/$repoName.git"
        Write-Host ""
        $addNow = Read-Host "Create remote now? (y/n)"
        if ($addNow -eq "y") {
            $useSsh = Read-Host "Use SSH? (y/n, default HTTPS)"
            if ($useSsh -eq "y") {
                git remote add origin "git@github.com:$GitHubUsername/$repoName.git"
            } else {
                git remote add origin "https://github.com/$GitHubUsername/$repoName.git"
            }
            Write-Host "Remote 'origin' added." -ForegroundColor Green
        }
    }
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Write-Host "This folder uses your PERSONAL identity. All other folders still use company global config."
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Create a PUBLIC repo on github.com/$GitHubUsername (no README/license)"
Write-Host "  2. git add ."
Write-Host "  3. git commit -m `"QA Assignment: SauceDemo UI + FakeStoreAPI automation`""
Write-Host "  4. git push -u origin main"
Write-Host "  5. GitHub Actions runs ONLY on that repo (see .github/workflows/ci.yml)"
Write-Host ""
