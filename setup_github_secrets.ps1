# PowerShell script to create Azure Service Principal for GitHub Actions

Write-Host "=========================================="
Write-Host "Creating Azure Service Principal"
Write-Host "=========================================="

# Variables
$subscriptionId = "d5156f99-abd5-4af9-9e2d-a875ef22df46"
$resourceGroup = "cw2-mlops-rg"
$spName = "github-actions-mlops-cw2"

Write-Host ""
Write-Host "Creating service principal..."
Write-Host "This will give GitHub Actions permission to access Azure ML"
Write-Host ""

# Create service principal
$sp = az ad sp create-for-rbac `
  --name $spName `
  --role contributor `
  --scopes "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup" `
  --sdk-auth

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "SUCCESS! Copy the JSON output below:"
    Write-Host "=========================================="
    Write-Host ""
    Write-Host $sp
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "NEXT STEPS:"
    Write-Host "=========================================="
    Write-Host ""
    Write-Host "1. Go to: https://github.com/jmcginnity2025/mlops-cw2-fresh/settings/secrets/actions"
    Write-Host ""
    Write-Host "2. Click 'New repository secret'"
    Write-Host ""
    Write-Host "3. Add these TWO secrets:"
    Write-Host ""
    Write-Host "   Secret 1:"
    Write-Host "   Name: AZURE_CREDENTIALS"
    Write-Host "   Value: <paste the ENTIRE JSON above>"
    Write-Host ""
    Write-Host "   Secret 2:"
    Write-Host "   Name: AZURE_SUBSCRIPTION_ID"
    Write-Host "   Value: $subscriptionId"
    Write-Host ""
    Write-Host "=========================================="
} else {
    Write-Host ""
    Write-Host "ERROR: Failed to create service principal"
    Write-Host "Check that you have permission to create service principals"
}
