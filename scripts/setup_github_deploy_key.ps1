<#
PowerShell helper: create GitHub repo (via gh), generate an SSH deploy key, add it to the repo, and print the private key contents.

Usage (PowerShell):
  1) Ensure GitHub CLI (gh) is installed and authenticated: `gh auth login`
  2) Run this script with parameters:
     .\setup_github_deploy_key.ps1 -Owner your-username -Repo your-repo -Visibility private

This script will:
  - create the repo if it doesn't exist
  - generate an ed25519 keypair in the current directory (will not overwrite by default)
  - add the public key as a deploy key to the repo with write access
  - print the private key to the console (so you can copy it into GitLab CI variables)
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Owner,

    [Parameter(Mandatory=$true)]
    [string]$Repo,

    [ValidateSet('public','private')]
    [string]$Visibility = 'private',

    [string]$KeyFileName = 'gitlab_to_github_deploy_key'
)

# Ensure gh is available
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI 'gh' is not found in PATH. Install it from https://cli.github.com/ and run 'gh auth login' first."
    exit 2
}

$fullRepo = "$Owner/$Repo"

# Create the repo (will fail if already exists but that's OK)
Write-Host "Creating GitHub repo $fullRepo (visibility=$Visibility) if it doesn't exist..."
$createResult = gh repo create $fullRepo --$Visibility --confirm 2>&1
Write-Host $createResult

# Generate SSH key pair
if (Test-Path $KeyFileName -PathType Leaf -or Test-Path "$KeyFileName.pub" -PathType Leaf) {
    Write-Host "Key files $KeyFileName or $KeyFileName.pub already exist. Skipping key generation."
} else {
    Write-Host "Generating ed25519 keypair -> $KeyFileName / $KeyFileName.pub"
    ssh-keygen -t ed25519 -f $KeyFileName -N "" | Out-Null
}

# Read public key
$pubKey = Get-Content "$KeyFileName.pub" -Raw

Write-Host "Adding deploy key to GitHub repo (write access)..."
# Use gh api to add deploy key with write access
$body = @{ title = "GitLab CI deploy key"; key = $pubKey; read_only = $false } | ConvertTo-Json
$apiResp = gh api -X POST /repos/$Owner/$Repo/keys -f title='GitLab CI deploy key' -f key="$pubKey" -f read_only=false 2>&1
Write-Host $apiResp

Write-Host "Private key (copy this into your GitLab CI variable named GITHUB_SSH_PRIVATE_KEY):"
Write-Host "---BEGIN PRIVATE KEY---"
Get-Content $KeyFileName -Raw
Write-Host "---END PRIVATE KEY---"

Write-Host "To enable the SSH CI job, set the GitLab CI variable MIRROR_SSH=true and ensure GITHUB_REPO is set to $fullRepo."
Write-Host "You can now add the private key value as the CI variable in GitLab (Settings -> CI/CD -> Variables)."

