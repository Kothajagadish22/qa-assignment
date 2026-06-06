# Personal GitHub — This Folder Only

Your **global** git is still your company account:

```
user.name  = kothajagadish-a11y
user.email = kotha.jagadish@anakin.company
```

This project uses **local** git config inside `Assigment/` only. Other folders are **not affected**.

## Quick setup (recommended)

```powershell
cd C:\Users\Anakin\Desktop\Assigment
.\setup_personal_git.ps1
```

Enter your **personal** GitHub username, name, and email when prompted.

## What stays isolated

| Setting | Scope | Affects other folders? |
|---------|--------|-------------------------|
| `git config --local user.email` | This folder only | No |
| `git remote origin` | This folder only | No |
| `.github/workflows/ci.yml` | Runs on **your GitHub repo** when you push | No |
| Company global config | Everywhere else | Unchanged |

GitHub Actions does **not** run on your PC or other projects. It only runs on GitHub when you push **this** repo.

## Step-by-step

### 1. Run the setup script

```powershell
.\setup_personal_git.ps1
```

### 2. Create a public repo on your personal GitHub

1. Log in to your **personal** GitHub account
2. **New repository** → name e.g. `qa-assignment`
3. Set visibility to **Public**
4. Do **not** add README, .gitignore, or license (we already have them)

### 3. Add remote and push

```powershell
git remote add origin https://github.com/YOUR_USERNAME/qa-assignment.git
git add .
git commit -m "QA Assignment: SauceDemo UI + FakeStoreAPI automation"
git branch -M main
git push -u origin main
```

### 4. Verify GitHub Actions

After push, open your repo on GitHub → **Actions** tab.  
The workflow `.github/workflows/ci.yml` should run automatically.

## Login: personal vs company GitHub

If `git push` uses the wrong account:

**Option A — HTTPS (simplest)**  
When prompted, sign in with your **personal** GitHub account.  
Windows Credential Manager stores it per URL.

**Option B — SSH (best for two accounts)**  
Create a personal key and use it only for this repo:

```powershell
ssh-keygen -t ed25519 -C "your-personal-email@gmail.com" -f "$env:USERPROFILE\.ssh\id_ed25519_personal_github"
```

Add the `.pub` file to GitHub → Settings → SSH keys.

Then in this folder only:

```powershell
git config --local core.sshCommand "ssh -i $env:USERPROFILE\.ssh\id_ed25519_personal_github -o IdentitiesOnly=yes"
git remote set-url origin git@github.com:YOUR_USERNAME/qa-assignment.git
```

## Verify local config

```powershell
git config --local --list    # this folder only
git config --global --list   # company (unchanged)
```

## Files not pushed (in .gitignore)

- `.venv/` — virtual environment
- `report.html` — generated test report
- `.pytest_cache/` — pytest cache
