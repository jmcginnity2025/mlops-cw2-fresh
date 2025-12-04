# Testing Azure ML Pipeline - After Adding Secrets

## ✅ Prerequisites Check

Before testing, confirm you have:
- [x] Added `AZURE_CREDENTIALS` secret to GitHub
- [x] Added `AZURE_SUBSCRIPTION_ID` secret to GitHub
- [x] Both secrets visible at: https://github.com/jmcginnity2025/mlops-cw2-fresh/settings/secrets/actions

---

## 🧪 Test Method 1: Automatic Trigger (Recommended)

This tests the full automated workflow.

### Step 1: Make a Small Change

```bash
cd "C:\AI Masters\AI Masters\Infrastucture Module - Azure\CW2\mlops-cw2-fresh"

# Add a test comment to trigger pipeline
echo "# Test Azure ML pipeline - $(date)" >> README.md

# Commit and push
git add README.md
git commit -m "Test Azure ML automated pipeline"
git push
```

### Step 2: Watch Both Pipelines

Go to: **https://github.com/jmcginnity2025/mlops-cw2-fresh/actions**

You should see **TWO pipelines** running simultaneously:

1. **ML CI/CD Pipeline** (Local training - already working ✅)
   - Job 1: Data Preprocessing
   - Job 2: Train Models
   - Job 3: Evaluate & Regression Test
   - Job 4: Version & Tag Models
   - **Duration**: ~3-5 minutes

2. **Azure ML Pipeline** (Cloud training - NEW! 🆕)
   - Job 1: Submit Training to Azure ML
   - Job 2: Compare Models
   - Job 3: Pipeline Success
   - **Duration**: ~15-20 minutes (includes environment build)

---

## 🧪 Test Method 2: Manual Trigger

If you prefer not to commit, trigger manually:

### Step 1: Open Workflow Page

Go to: **https://github.com/jmcginnity2025/mlops-cw2-fresh/actions**

### Step 2: Select Azure ML Pipeline

Click on **"Azure ML Pipeline"** in the left sidebar

### Step 3: Run Workflow

1. Click **"Run workflow"** button (top right)
2. Select branch: **main**
3. Click green **"Run workflow"** button

### Step 4: Monitor Execution

Click on the running workflow to see live logs

---

## 📊 What to Expect

### GitHub Actions Side:

**Job 1: Submit Training to Azure ML**
```
✅ Connected to: cw2-mlops-workspace
✅ Dataset: support-tickets-dataset
✅ Job submitted: [job-name]
Status: Running
⏳ Waiting for job to complete...
[Live streaming logs from Azure...]
📊 Final status: Completed
✅ Training completed successfully!
```

**Job 2: Compare Models**
```
Latest run: [job-name]
Status: Completed
✅ Models trained successfully!
✅ Both iterations completed
```

**Job 3: Pipeline Success**
```
================================================
🎉 AZURE ML PIPELINE SUCCESSFUL!
================================================
Training completed in Azure ML
Models logged with MLflow
Ready for deployment
================================================
```

### Azure ML Studio Side:

**1. Jobs Page**
- Go to: https://ml.azure.com → Jobs
- You'll see: `github-run-[number]`
- Status: Running → Completed

**2. Compute Page**
- Go to: https://ml.azure.com → Compute
- `cpu-cluster` will show:
  - Status: Busy (during training)
  - Status: Idle (after completion)
  - Then scales to 0 nodes (cost saving!)

**3. MLflow Tracking**
- Go to: https://ml.azure.com → Jobs → [your job]
- Click on **"Metrics"** tab
- You'll see:
  - `iteration_1_train_accuracy`
  - `iteration_1_test_accuracy`
  - `iteration_1_test_f1`
  - `iteration_2_train_accuracy`
  - `iteration_2_test_accuracy`
  - `iteration_2_test_f1`
  - All logged and tracked!

**4. Models Page**
- Go to: https://ml.azure.com → Models
- Both model files saved:
  - `iteration_1_model.pkl`
  - `iteration_2_model.pkl`

---

## 🔍 Monitoring Tips

### Watch GitHub Actions Live:

1. Go to Actions tab
2. Click on running workflow
3. Click on job (e.g., "Submit Training to Azure ML")
4. You'll see live logs streaming from Azure!

### Watch Azure ML Studio:

1. Open: https://ml.azure.com
2. Navigate to: Jobs → All jobs
3. Find: `github-run-[number]`
4. Click to see:
   - Live logs
   - Metrics being logged
   - Resource utilization
   - Cost tracking

### Best Practice:

**Open both side-by-side:**
- Left monitor: GitHub Actions (shows submission and orchestration)
- Right monitor: Azure ML Studio (shows actual training progress)

---

## ⏱️ Timeline Expectations

### First Run (Cold Start):
```
0:00 - GitHub Actions starts
0:30 - Azure ML receives job
1:00 - Environment build starts (Docker image)
8:00 - Environment build completes
9:00 - Compute scales up (0→1 nodes)
10:00 - Training starts
11:00 - Iteration 1 completes
12:00 - Iteration 2 completes
13:00 - Metrics logged to MLflow
14:00 - Models saved
15:00 - Job completes
15:30 - Compute scales down (1→0 nodes)
```

### Subsequent Runs (Warm Start):
```
0:00 - GitHub Actions starts
0:30 - Azure ML receives job
1:00 - Uses cached environment (faster!)
2:00 - Compute scales up
3:00 - Training starts
4:00 - Iteration 1 completes
5:00 - Iteration 2 completes
6:00 - Job completes
7:00 - Compute scales down
```

**Note**: First run takes longer due to Docker image build!

---

## 🎯 Success Indicators

### In GitHub Actions:

✅ All jobs show green checkmarks
✅ "Submit Training to Azure ML" completed
✅ "Compare Models" passed
✅ Summary shows both iterations trained

### In Azure ML Studio:

✅ Job status: Completed
✅ All metrics logged to MLflow
✅ Both model files saved
✅ Compute scaled back to zero
✅ No errors in logs

---

## 🚨 Troubleshooting

### "Error: AZURE_CREDENTIALS not found"

**Cause**: Secret not added or wrong name

**Fix**:
1. Go to: https://github.com/jmcginnity2025/mlops-cw2-fresh/settings/secrets/actions
2. Verify `AZURE_CREDENTIALS` exists (shows *****)
3. Name must be EXACTLY: `AZURE_CREDENTIALS` (all caps, no spaces)

### "Authentication failed"

**Cause**: JSON credentials malformed

**Fix**:
1. Check ADD_GITHUB_SECRETS.md for correct JSON format
2. Ensure you copied entire JSON (all 10 lines)
3. No extra spaces or line breaks
4. Starts with `{` and ends with `}`

### "Workspace not found"

**Cause**: Wrong subscription ID or workspace deleted

**Fix**:
```bash
# Verify workspace exists
az ml workspace show \
  --name cw2-mlops-workspace \
  --resource-group cw2-mlops-rg
```

### "Dataset not found"

**Cause**: Dataset not uploaded to Azure ML

**Fix**:
```bash
cd "C:\AI Masters\AI Masters\Infrastucture Module - Azure\CW2\mlops-cw2-fresh"
python submit_training_job.py
```

This will re-upload the dataset if missing.

### "Environment build failed"

**Cause**: Missing dependencies in environment.yml

**Check**: Job logs in Azure ML Studio → Errors tab

### Job stuck "Running" for > 30 minutes

**Possible causes**:
- Compute quota exceeded
- Region capacity issues
- Cost limit reached

**Fix**:
```bash
# Check compute status
az ml compute show \
  --name cpu-cluster \
  --workspace-name cw2-mlops-workspace \
  --resource-group cw2-mlops-rg
```

---

## 📸 Screenshots for Coursework

After successful run, capture:

### GitHub Actions:
1. **Actions overview** - Both pipelines listed
2. **Azure ML Pipeline** - All 3 jobs green
3. **Job logs** - "Submit Training to Azure ML" logs
4. **Summary page** - Pipeline success message

### Azure ML Studio:
5. **Jobs page** - Your completed job
6. **Job details** - Status, duration, compute used
7. **Metrics tab** - MLflow metrics for both iterations
8. **Logs tab** - Training output
9. **Models** - Both iteration models saved
10. **Compute** - Showing auto-scale to zero

### Comparison View:
11. **Side-by-side** - GitHub Actions + Azure ML Studio
12. **MLflow dashboard** - Metrics comparison

---

## 🎓 What This Demonstrates for Coursework

### Model Development:
✅ Two iterations trained (Random Forest + XGBoost)
✅ Hyperparameter differences documented
✅ Performance comparison automated

### CI/CD Pipeline:
✅ Automated trigger on git push
✅ GitHub Actions orchestration
✅ Azure ML integration
✅ Sequential job dependencies

### Deployment:
✅ Cloud-based training
✅ Scalable compute (auto-scale)
✅ Environment management (Docker)
✅ Model versioning

### Monitoring:
✅ MLflow metric tracking
✅ Live log streaming
✅ Performance comparison
✅ Resource utilization tracking

### Retraining:
✅ Automatic on new commits
✅ Reproducible training
✅ Version-controlled code
✅ Compute auto-scaling

### Governance:
✅ Git version control
✅ Audit trail (GitHub Actions logs)
✅ Access control (secrets management)
✅ Cost tracking (Azure ML compute)

**All CW2 requirements met!** 🎉

---

## 🔄 After Testing

### If Successful:

1. **Take screenshots** (see list above)
2. **Document results** in coursework report
3. **Keep running** for future commits (fully automated!)
4. **Cost monitoring**: Compute scales to zero = minimal cost

### Cost Optimization:

The pipeline is already optimized:
- Compute scales to 0 when idle
- Only runs when you commit
- Uses smallest viable VM (STANDARD_DS3_v2)
- Efficient environment caching

**Expected cost per run**: ~£0.50-£1.00 (15-20 min training)

### Next Commits:

Every future commit to main will:
1. Trigger local pipeline (GitHub Actions VM - free)
2. Trigger Azure ML pipeline (cloud compute - paid)

If you want to **disable Azure ML pipeline temporarily**:
- Don't commit to main (use feature branches)
- Or comment out the workflow file
- Local pipeline will still run!

---

## ✅ Success Checklist

Before marking complete, verify:

- [ ] GitHub secrets added (2 secrets visible)
- [ ] Pipeline triggered (manually or via commit)
- [ ] GitHub Actions shows both pipelines running
- [ ] Azure ML job appears in studio
- [ ] Training completes successfully
- [ ] MLflow metrics logged
- [ ] Both models saved
- [ ] Compute scales back to zero
- [ ] All jobs green in GitHub Actions
- [ ] Screenshots taken for coursework

---

## 🎉 Next Steps After Success

1. **Document your setup** - Write up the implementation
2. **Analyze metrics** - Compare model performance
3. **Coursework submission** - Include screenshots and analysis
4. **Optional improvements**:
   - Add model deployment step
   - Implement A/B testing
   - Add monitoring dashboards
   - Set up alerts

---

## 💡 Pro Tips

### Faster Testing:

If you want to test multiple times quickly:
```bash
# Quick commit script
echo "test" >> test.txt
git add test.txt
git commit -m "Test run"
git push
```

### Cost Control:

Monitor costs at:
- https://portal.azure.com → Cost Management
- Set budget alerts
- Review compute usage

### Debugging:

If something fails:
1. Check GitHub Actions logs first
2. Then check Azure ML Studio logs
3. Look for specific error messages
4. Check this troubleshooting section

---

## 📞 Need Help?

If you encounter issues:

1. **Check logs** - GitHub Actions and Azure ML Studio
2. **Verify secrets** - Correct format and values
3. **Test connectivity** - Can you access Azure ML manually?
4. **Review setup** - Follow ADD_GITHUB_SECRETS.md step-by-step

---

**Good luck with testing!** 🚀

Once the pipeline runs successfully, you'll have a complete, production-grade MLOps system ready for your coursework submission!
