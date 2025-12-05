# 🚀 Unified ML Pipeline - Single Complete Workflow

## ✅ What Changed

**OLD (Option B):** Two separate pipelines
- Pipeline 1: Local training (45s)
- Pipeline 2: Azure ML training (15-20 min)

**NEW (Unified):** ONE complete pipeline
- Preprocess locally → Train on Azure ML → Regression test → Version
- Duration: ~15-20 minutes
- **Best of both worlds!**

---

## 📊 Pipeline Flow

```
Commit to GitHub
       ↓
┌─────────────────────────────────────────────────────────┐
│ UNIFIED ML PIPELINE                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Job 1: Data Preprocessing (Local - Fast)                │
│   ✅ Load dataset                                       │
│   ✅ Clean & engineer features                          │
│   ✅ Train/test split                                   │
│   ✅ Upload processed data                              │
│   ⏱️ Duration: ~30 seconds                              │
│                                                          │
│         ↓                                                │
│                                                          │
│ Job 2: Train Models on Azure ML (Cloud - Scalable)      │
│   ✅ Connect to Azure ML workspace                      │
│   ✅ Submit training job to cpu-cluster                 │
│   ✅ Train Iteration 1: Random Forest                   │
│   ✅ Train Iteration 2: XGBoost                         │
│   ✅ Log metrics to Azure ML Studio                     │
│   ✅ Download model artifacts                           │
│   ✅ Register models in Model Registry                  │
│   ⏱️ Duration: ~15-20 minutes (first run)               │
│                                                          │
│         ↓                                                │
│                                                          │
│ Job 3: Regression Testing (Local - Fast Validation)     │
│   ✅ Compare Iteration 2 vs Iteration 1                 │
│   ✅ Check performance threshold (2% drop allowed)      │
│   ❌ FAIL pipeline if regression detected               │
│   ✅ Generate evaluation report                         │
│   ⏱️ Duration: ~5 seconds                               │
│                                                          │
│         ↓                                                │
│                                                          │
│ Job 4: Version Models (Only if passed)                  │
│   ✅ Create version tag                                 │
│   ✅ Generate pipeline summary                          │
│   ✅ Prepare for deployment                             │
│   ⏱️ Duration: ~10 seconds                              │
│                                                          │
│         ↓                                                │
│                                                          │
│ Job 5: Deploy to Online Endpoint (Production)           │
│   ✅ Create/Update Azure ML Online Endpoint             │
│   ✅ Deploy latest model version                        │
│   ✅ Route 100% traffic to new deployment               │
│   ✅ Real-time inference API ready                      │
│   ⏱️ Duration: ~5-10 minutes                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
       ↓
   Production API
   (Real-time predictions)
```

---

## 🎯 Key Features

### 1. **Local Preprocessing**
- Fast data preparation on GitHub Actions VM
- No Azure costs for preprocessing
- Quick iteration during development

### 2. **Cloud Training**
- Scalable Azure ML compute cluster
- Professional MLflow tracking
- Enterprise-grade infrastructure
- Auto-scales to zero (cost optimization)

### 3. **Regression Testing** (CRITICAL!)
- Compares new model vs baseline
- Fails pipeline if >2% performance drop
- Prevents bad models from being deployed
- **Your quality gate!**

### 4. **Automated Versioning**
- Only passed models get versioned
- Timestamp-based version tags
- Audit trail in GitHub Actions logs

---

## 💡 Why This is Better

### OLD (Two Pipelines):
❌ Confusing - which one to look at?
❌ Redundant - training in two places
❌ No connection between them

### NEW (Unified):
✅ **Single source of truth**
✅ **Clear flow**: prep → train → test → deploy
✅ **Best of both**: fast local validation + scalable cloud training
✅ **Production-ready**: enterprise ML pattern
✅ **Cost-optimized**: preprocessing local, training on-demand

---

## 🔍 How It Works

### Job 1: Preprocessing (Local)
```bash
# Runs on GitHub Actions (free)
python preprocess.py
→ Uploads processed_data/ artifact
```
**Why local?** Fast, free, doesn't need GPU/cluster

### Job 2: Train on Azure ML (Cloud)
```python
# Submits job to Azure ML
ml_client.jobs.create_or_update(job)
→ Builds environment (first run: 8 min)
→ Scales compute (0 → 1 node)
→ Trains both iterations
→ Logs to MLflow
→ Downloads metrics
→ Scales compute (1 → 0 node)
```
**Why cloud?** Scalable, reproducible, professional tracking

### Job 3: Regression Test (Local)
```python
# Runs evaluate.py
compare_models(iteration_2, iteration_1)
if performance_drop > 2%:
    sys.exit(1)  # FAIL pipeline ❌
```
**Why local?** Fast validation, no need for cloud resources

### Job 4: Version (Local)
```bash
# Only runs if Job 3 passed
version=v_$(date +%Y%m%d_%H%M%S)
→ Tags models with version
→ Ready for deployment
```
**Why local?** Simple tagging, no cloud needed

---

## 📊 What You'll See

### In GitHub Actions:

```
Unified ML Pipeline #123
├─ ✅ Data Preprocessing (30s)
├─ 🔄 Train Models on Azure ML (15-20 min)
├─ ⏳ Regression Testing (pending)
└─ ⏳ Version & Deploy (pending)
```

### In Azure ML Studio:

```
Jobs → unified-run-123
Status: Running
Experiment: unified-cicd-training
Compute: cpu-cluster (1 node)

Metrics (MLflow):
├─ iteration_1_train_accuracy: 0.8968
├─ iteration_1_test_accuracy: 0.8684
├─ iteration_2_train_accuracy: 0.9532
└─ iteration_2_test_accuracy: 0.9097
```

---

## ⏱️ Timeline

### First Run (Cold Start):
```
0:00 - Commit triggers pipeline
0:30 - Preprocessing completes
1:00 - Job submitted to Azure ML
2:00 - Environment build starts
10:00 - Environment build completes
11:00 - Compute scales up (0→1 nodes)
12:00 - Training starts
13:00 - Iteration 1 completes
14:00 - Iteration 2 completes
15:00 - Metrics logged to MLflow
16:00 - Compute scales down (1→0 nodes)
17:00 - Regression testing starts
17:05 - Regression testing passes
17:10 - Models versioned
17:15 - Pipeline complete ✅
```

### Subsequent Runs (Warm Start):
```
0:00 - Commit triggers pipeline
0:30 - Preprocessing completes
1:00 - Job submitted to Azure ML
2:00 - Uses cached environment (faster!)
3:00 - Compute scales up
4:00 - Training starts
5:00 - Both iterations complete
6:00 - Compute scales down
7:00 - Regression testing passes
7:05 - Models versioned
7:10 - Pipeline complete ✅
```
**Much faster on subsequent runs!**

---

## 🚨 Failure Scenarios

### Scenario 1: Preprocessing Fails
```
Job 1: Data Preprocessing ❌ FAILED
  → Pipeline stops
  → Jobs 2-4 not run
  → No Azure costs incurred
```

### Scenario 2: Azure Training Fails
```
Job 1: Data Preprocessing ✅ PASSED
Job 2: Train on Azure ML ❌ FAILED
  → Pipeline stops
  → Jobs 3-4 not run
  → Check Azure ML Studio logs
```

### Scenario 3: Regression Test Fails (IMPORTANT!)
```
Job 1: Data Preprocessing ✅ PASSED
Job 2: Train on Azure ML ✅ PASSED
Job 3: Regression Testing ❌ FAILED
  → Pipeline stops
  → Job 4 not run
  → Models NOT versioned
  → BAD MODEL BLOCKED! 🛡️
```

### Scenario 4: All Pass
```
Job 1: Data Preprocessing ✅ PASSED
Job 2: Train on Azure ML ✅ PASSED
Job 3: Regression Testing ✅ PASSED
Job 4: Version & Deploy ✅ PASSED
  → Models versioned
  → Ready for deployment
  → SUCCESS! 🎉
```

---

## 💰 Cost Breakdown

### Per Pipeline Run:

| Component | Duration | Cost | Notes |
|-----------|----------|------|-------|
| **Preprocessing** | 30s | £0.00 | GitHub Actions (free) |
| **Azure ML Training** | 15-20 min | £0.50-£1.00 | STANDARD_DS3_v2 compute |
| **Regression Testing** | 5s | £0.00 | GitHub Actions (free) |
| **Versioning** | 10s | £0.00 | GitHub Actions (free) |
| **TOTAL** | ~20 min | **£0.50-£1.00** | Only Azure compute charged |

### Cost Optimization Features:
- ✅ Preprocessing done locally (free)
- ✅ Compute auto-scales to zero
- ✅ Cached environment (faster subsequent runs)
- ✅ Regression testing local (free)
- ✅ Only pay for actual training time

**Estimated monthly cost (20 runs): £10-£20**

---

## 🎓 For Coursework

### This Pipeline Demonstrates:

#### 1. **Model Development**
- ✅ Two iterations with different algorithms
- ✅ Hyperparameter tuning (RF vs XGBoost)
- ✅ Performance comparison

#### 2. **CI/CD Automation**
- ✅ Triggered automatically on commit
- ✅ Sequential job dependencies
- ✅ Artifact management
- ✅ Quality gates

#### 3. **Deployment Strategy**
- ✅ Cloud-based training (Azure ML)
- ✅ Scalable compute infrastructure
- ✅ Environment management (Docker)
- ✅ Version control

#### 4. **Monitoring**
- ✅ MLflow experiment tracking
- ✅ Metrics comparison
- ✅ Live log streaming
- ✅ Cost tracking

#### 5. **Retraining**
- ✅ Automatic on code changes
- ✅ Reproducible training
- ✅ Version-controlled models

#### 6. **Governance**
- ✅ **Regression testing** (prevents bad models)
- ✅ Audit trail (GitHub Actions logs)
- ✅ Access control (secrets management)
- ✅ Cost monitoring

**ALL CW2 requirements met in ONE unified pipeline!** 🎯

---

## 📸 Screenshots for Coursework

After a successful run, capture:

### GitHub Actions:
1. **Workflow overview** - All 4 jobs green
2. **Job 1 logs** - Preprocessing details
3. **Job 2 logs** - Azure ML submission and training
4. **Job 3 logs** - Regression testing results
5. **Job 4 logs** - Versioning and summary
6. **Summary page** - Complete pipeline summary

### Azure ML Studio:
7. **Jobs list** - Your unified-run jobs
8. **Job details** - Training progress
9. **Metrics tab** - MLflow metrics for both iterations
10. **Compute tab** - Auto-scaling to zero

### Side-by-side:
11. **GitHub + Azure** - Both platforms together
12. **Before/after metrics** - Model comparison

---

## 🔧 Troubleshooting

### "Azure ML job fails"
**Check**: Azure ML Studio logs
**Fix**: Look for environment or compute issues

### "Regression test fails"
**Expected**: Model performed worse than baseline
**Action**: Investigate why (data quality, hyperparameters)
**Note**: This is working correctly - it's blocking bad models!

### "Pipeline takes too long"
**First run**: 15-20 min (builds environment)
**Subsequent**: 7-10 min (uses cached environment)
**This is normal and expected!**

---

## ✅ Quick Reference

### Trigger Pipeline:
```bash
git add .
git commit -m "Your message"
git push
```

### Watch Pipeline:
https://github.com/jmcginnity2025/mlops-cw2-fresh/actions

### View Training in Azure:
https://ml.azure.com → Jobs → unified-run-[number]

### Check Costs:
https://portal.azure.com → Cost Management

---

## 🎉 Summary

You now have a **production-grade, unified ML pipeline** that:

✅ Preprocesses data efficiently (local)
✅ Trains models at scale (Azure ML cloud)
✅ Validates quality (regression testing)
✅ Versions automatically (only good models)
✅ Optimizes costs (auto-scaling)
✅ Provides monitoring (MLflow)
✅ Demonstrates MLOps best practices

**This is enterprise-quality ML infrastructure!** 🌟

Perfect for your coursework and portfolio! 🎓
