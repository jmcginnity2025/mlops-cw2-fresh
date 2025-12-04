# Add GitHub Secrets - Step by Step

## ✅ Service Principal Created!

Your credentials have been generated. Now add them to GitHub:

---

## 🔐 **Step 1: Copy the Credentials**

Copy this ENTIRE JSON (from setup_github_secrets.ps1 output):

**⚠️ USE YOUR ACTUAL CREDENTIALS FROM setup_github_secrets.ps1 OUTPUT!**

```json
{
  "clientId": "YOUR-CLIENT-ID-HERE",
  "clientSecret": "YOUR-CLIENT-SECRET-HERE",
  "subscriptionId": "YOUR-SUBSCRIPTION-ID-HERE",
  "tenantId": "YOUR-TENANT-ID-HERE",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

---

## 🔑 **Step 2: Add Secrets to GitHub**

### Go to GitHub Secrets Page:
👉 **https://github.com/jmcginnity2025/mlops-cw2-fresh/settings/secrets/actions**

Or manually:
1. Go to your repo: https://github.com/jmcginnity2025/mlops-cw2-fresh
2. Click **Settings** (top right)
3. Click **Secrets and variables** (left sidebar)
4. Click **Actions**
5. Click **New repository secret** (green button)

---

### Add Secret #1: AZURE_CREDENTIALS

1. Click **"New repository secret"**
2. Fill in:
   - **Name**: `AZURE_CREDENTIALS`
   - **Value**: Paste the ENTIRE JSON above (all 10 lines)
3. Click **"Add secret"**

**Screenshot check:**
- Name field shows: `AZURE_CREDENTIALS`
- Value field shows the JSON starting with `{` and ending with `}`

---

### Add Secret #2: AZURE_SUBSCRIPTION_ID

1. Click **"New repository secret"** again
2. Fill in:
   - **Name**: `AZURE_SUBSCRIPTION_ID`
   - **Value**: Your subscription ID (from the JSON above)
3. Click **"Add secret"**

---

## ✅ **Step 3: Verify Secrets Were Added**

You should now see **2 secrets** listed:
- ✅ `AZURE_CREDENTIALS`
- ✅ `AZURE_SUBSCRIPTION_ID`

**Important:** GitHub will show `***` for the values - this is normal (they're hidden for security)

---

## 🧪 **Step 4: Test the Azure ML Pipeline**

Once secrets are added, trigger the pipeline:

### Option A: Make a Small Change
```bash
cd "C:\AI Masters\AI Masters\Infrastucture Module - Azure\CW2\mlops-cw2-fresh"

# Make a small change
echo "# Test Azure ML pipeline" >> README.md

# Commit and push
git add README.md
git commit -m "Test Azure ML automated pipeline"
git push
```

### Option B: Manual Trigger
1. Go to: https://github.com/jmcginnity2025/mlops-cw2-fresh/actions
2. Click on **"Azure ML Pipeline"** (left sidebar)
3. Click **"Run workflow"** (right side)
4. Click green **"Run workflow"** button

---

## 📊 **Step 5: Watch the Pipeline**

Go to: https://github.com/jmcginnity2025/mlops-cw2-fresh/actions

You should see **TWO pipelines running**:
1. ✅ **ML CI/CD Pipeline** (local training - already worked)
2. 🆕 **Azure ML Pipeline** (cloud training - new!)

Click on the Azure ML Pipeline to watch:
- Submit training job to Azure
- Training runs on your cpu-cluster
- Logs to MLflow
- Returns results

**Expected time**: ~15-20 minutes (includes environment build)

---

## 🎯 **What Will Happen**

### GitHub Actions Will:
1. Connect to your Azure ML workspace
2. Get the dataset (already uploaded)
3. Submit training job to cpu-cluster
4. Wait for completion
5. Download results
6. Compare models
7. Pass/Fail based on performance

### Azure ML Will:
1. Build environment from environment.yml
2. Start compute cluster
3. Run train_azure.py
4. Train both iterations
5. Log metrics to MLflow
6. Save models
7. Scale compute back to zero

---

## 🔍 **How to Monitor**

### In GitHub:
- Actions tab: https://github.com/jmcginnity2025/mlops-cw2-fresh/actions
- Watch workflow progress
- See job logs

### In Azure ML Studio:
- Jobs page: https://ml.azure.com
- See training progress
- View MLflow metrics
- Check compute status

---

## 🚨 **Troubleshooting**

### "Error: AZURE_CREDENTIALS not found"
→ Make sure you added the secret correctly in GitHub
→ Name must be EXACTLY: `AZURE_CREDENTIALS` (all caps)

### "Authentication failed"
→ Check the JSON was pasted correctly (all 10 lines)
→ No extra spaces or characters

### "Workspace not found"
→ Make sure you're using the correct subscription ID
→ Verify workspace exists: `az ml workspace show --name cw2-mlops-workspace --resource-group cw2-mlops-rg`

### Pipeline doesn't trigger
→ Make sure secrets are in the "Actions" section (not "Codespaces")
→ Try manual trigger (Option B above)

---

## 📸 **For Your Coursework**

After the Azure ML pipeline runs, take screenshots of:

1. **GitHub Secrets page** (showing 2 secrets exist)
2. **GitHub Actions tab** (both pipelines running)
3. **Azure ML Pipeline logs** (showing submission to Azure)
4. **Azure ML Studio** (showing training job)
5. **MLflow metrics** (comparison of models)

---

## ✅ **Checklist**

Before moving on, confirm:
- [ ] Service principal created (output shows JSON)
- [ ] AZURE_CREDENTIALS secret added to GitHub
- [ ] AZURE_SUBSCRIPTION_ID secret added to GitHub
- [ ] Both secrets visible in GitHub settings
- [ ] Ready to test pipeline

---

## 🎉 **Next Steps**

Once secrets are added:
1. Test the pipeline (see Step 4)
2. Watch it run in both GitHub and Azure
3. Verify MLflow tracking
4. Take screenshots for coursework

**Let me know once you've added the secrets and we'll test it!**
