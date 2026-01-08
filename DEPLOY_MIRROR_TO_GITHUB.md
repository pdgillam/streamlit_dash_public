# Mirror GitLab -> GitHub and deploy to Streamlit Cloud

This guide shows two safe ways to mirror your GitLab repository to GitHub so you can deploy the mirrored repo to Streamlit Cloud (which currently pulls from GitHub).

Overview
- Option 1 (recommended): Use a GitHub Personal Access Token (PAT) + GitLab CI (pre-configured .gitlab-ci.yml) to mirror `main` automatically.
- Option 2: Use GitLab built-in Push Mirroring (UI) if available on your GitLab plan.
- Option 3: Use SSH deploy key with GitLab CI instead of a PAT.

Prerequisites
- GitLab project with this repo (source)
- A GitHub account and a target repo (can be empty)
- Admin access to GitLab project to add CI/CD variables

Steps (PAT-based mirror using CI) — quick version

1) Create target GitHub repo (empty)

From the web UI
- Go to https://github.com/new and create a repo (private or public). Suggested name: `pdgillam/sample_dash`.

Or using GitHub CLI (PowerShell):

```powershell
# interactive: will open auth flow the first time
gh auth login
# create new private repo
gh repo create pdgillam/sample_dash --private --confirm
```

2) Create a GitHub Personal Access Token (PAT)

- On GitHub: Settings -> Developer settings -> Personal access tokens -> Tokens (classic) -> Generate new token.
- Scopes:
  - For private repo push: select `repo` (full control of private repositories).
  - For public repo only: you can select `public_repo`.
- Copy the token value — you will not be able to see it again.

3) Add variables to GitLab CI/CD settings

In GitLab project: Settings -> CI / CD -> Variables -> Add variable:
- Key: `GITHUB_USER`  Value: your GitHub username
- Key: `GITHUB_REPO`  Value: `owner/repo` (e.g. `alice/streamlit-dashboard`)
- Key: `GITHUB_TOKEN` Value: <your PAT here>

Set the `GITHUB_TOKEN` variable to Masked and Protected (if desired).

4) Pipeline behaviour

The included `.gitlab-ci.yml` will run by default when pushing to branch `main`. If you want to mirror all branches, set a project variable `MIRROR_ALL=true`.

5) Trigger the mirror

- Push to GitLab `main` (or whichever branch your rules are configured to watch). The pipeline will run and push to GitHub.
- Or manually run the pipeline: GitLab -> CI/CD -> Pipelines -> Run pipeline.

6) Confirm on GitHub

- Open the GitHub repo and confirm branches/commits are mirrored.

Optional: Immediate manual one-time push from local

From your local clone (PowerShell):

```powershell
# add github remote and push all branches and tags
git remote add github "https://github.com/your-username/your-repo.git"
git push --all github
git push --tags github
```

(If the repo is private and requires authentication, you can use a PAT in the URL, or authenticate with the GitHub CLI.)

### SSH deploy-key variant (detailed steps)

If you prefer not to use a PAT, use an SSH deploy key for CI to push to GitHub.

1) Generate an SSH key pair locally (PowerShell):

```powershell
# generate an ed25519 keypair without passphrase; adjust filename as desired
ssh-keygen -t ed25519 -f gitlab_to_github_deploy_key -N ""
```

This creates `gitlab_to_github_deploy_key` (private) and `gitlab_to_github_deploy_key.pub` (public).

2) Add the public key to the GitHub repo as a deploy key (writeable)

Web UI:
- GitHub repo -> Settings -> Deploy keys -> Add deploy key
- Title: GitLab CI deploy key
- Paste the contents of `gitlab_to_github_deploy_key.pub`
- Check "Allow write access" and save

OR using GitHub CLI:

```powershell
# Make sure you are authenticated with gh
gh auth login
# Add deploy key (replace owner/repo with your target repo)
gh api -X POST /repos/{owner}/{repo}/keys -f title='GitLab CI deploy key' -f key="$(Get-Content -Raw .\gitlab_to_github_deploy_key.pub)" -f read_only=false
```

3) Add the private key to GitLab CI variables

- In GitLab: Settings -> CI / CD -> Variables -> Add variable:
  - Key: `GITHUB_SSH_PRIVATE_KEY`
  - Value: paste the *contents* of `gitlab_to_github_deploy_key` (the private key)
  - Type: Variable (masked/protected as you prefer)

4) Enable the SSH mirror job in CI

- Set `MIRROR_SSH=true` in GitLab CI variables (or define it in pipeline run)
- Ensure `GITHUB_REPO` is set to `owner/repo` in CI variables

5) Trigger the pipeline (push to GitLab `main` or run pipeline manually). The `mirror_to_github_ssh` job will run and push via SSH using the deploy key.

Notes & security
- Keep the private key secure. Mark its CI variable as Protected to limit it to protected branches.
- Deploy keys are repo-specific; if you want to mirror to multiple repos, create keys per repo.

Deploying to Streamlit Cloud

- On https://share.streamlit.io create a new app and point it to the mirrored GitHub repo `pdgillam/sample_dash` and branch (usually `main`). Select `app.py` (or your entry file) and deploy.
- For private GitHub repos you’ll authorize Streamlit to access the repo.

Troubleshooting

- If you see authentication issues in the pipeline, check that `GITHUB_TOKEN` is correct and not expired.
- If the pipeline logs show the token in plain text, ensure the variable is `Masked` in GitLab.
- If mirroring fails with permission denied for pushing to GitHub, verify PAT scopes or deploy key write access.

If you want, I can:
- Create a `README` snippet in your repository with the exact steps personalized with your repo name.
- Modify the `.gitlab-ci.yml` to only mirror protected branches (e.g., `main`) and to create a lightweight push (`git push --all`) instead of `--mirror`.
- Add an SSH deploy-key variant of the CI job into the repo.

Tell me which of the optional follow-ups you'd like me to implement now (personalized CI, README with commands, or SSH deploy-key CI job).
