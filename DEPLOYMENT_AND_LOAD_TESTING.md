# Deployment and Load Testing Setup

## Overview

The pipeline now includes **7 complete jobs**:

1. ✅ **Data Preprocessing** (local)
2. ✅ **Model Training** (Azure ML cloud)
3. ✅ **Regression Testing** (local quality gate)
4. ✅ **Model Versioning** (local)
5. ✅ **Endpoint Deployment** (Azure ML cloud) - **NEW**
6. ✅ **Load Testing** (Locust) - **NEW**
7. ✅ **Pipeline Summary** (final report) - **NEW**

---

## Job 5: Deploy to Azure ML Online Endpoint

### What it does:
- Creates/updates Azure ML Managed Online Endpoint
- Registers the XGBoost model (iteration 2) to Model Registry
- Deploys model to endpoint with scoring script
- Routes 100% traffic to the deployment
- Exposes REST API for real-time predictions

### Key Components:

#### 1. **Scoring Script** ([score.py](score.py))
```python
def init():
    # Load model when endpoint starts
    global model
    model = pickle.load("iteration_2_model.pkl")

def run(raw_data):
    # Make predictions
    predictions = model.predict(input_data)
    return json.dumps({"predictions": predictions})
```

#### 2. **Endpoint Configuration**
- **Name**: `support-ticket-classifier`
- **Instance type**: `Standard_DS2_v2`
- **Instance count**: 1
- **Authentication**: API key
- **Deployment strategy**: Blue-green (blue deployment)

#### 3. **Model Registry**
- Model name: `support-ticket-classifier`
- Version: GitHub run number
- Artifacts: iteration_2_model.pkl

### Outputs:
- Scoring URI (REST endpoint URL)
- API key for authentication
- Endpoint info artifact

---

## Job 6: Load Testing with Locust

### What it does:
- Downloads endpoint URI and API key
- Creates Locust test file with real endpoint configuration
- Simulates 50 concurrent users
- Runs for 60 seconds
- Generates HTML report and CSV statistics

### Test Configuration:

| Parameter | Value |
|-----------|-------|
| Users | 50 |
| Spawn rate | 5 users/second |
| Duration | 60 seconds |
| Target | Azure ML Online Endpoint |

### Locust Test Scenario:

#### **SupportTicketPredictionUser**
Simulates normal API usage:
```python
@task
def predict_priority(self):
    # Send prediction request with support ticket features
    payload = {"data": [ticket_features]}
    response = self.client.post("/score", json=payload, headers=auth_headers)
```

### Sample Request Format:
```json
{
  "data": [[
    150,    // org_users
    12,     // past_30d_tickets
    5,      // customers_affected
    2.5,    // error_rate_pct
    30,     // downtime_min
    ...     // (24 features total)
  ]]
}
```

### Sample Response Format:
```json
{
  "predictions": [2],
  "model": "XGBoost",
  "num_samples": 1
}
```

### Outputs:
- `load_test_report.html` - Visual report with charts
- `load_test_results_stats.csv` - Request statistics
- `load_test_results_failures.csv` - Error logs
- GitHub Actions summary with metrics

---

## Job 7: Pipeline Summary

### What it does:
- Aggregates results from all previous jobs
- Generates comprehensive pipeline report
- Shows training metrics, deployment status, and load test results
- Final success/failure notification

---

## Files Added/Modified

### New Files:
1. **`locustfile.py`** - Standalone Locust test file for local testing
2. **`score.py`** - Azure ML scoring script for endpoint
3. **`DEPLOYMENT_AND_LOAD_TESTING.md`** - This documentation

### Modified Files:
1. **`.github/workflows/unified-ml-pipeline.yml`**
   - Added Job 5: Deploy to Online Endpoint
   - Added Job 6: Load Testing with Locust
   - Added Job 7: Pipeline Summary
   - Updated job dependencies

2. **`environment.yml`**
   - Added `locust` dependency

3. **`requirements.txt`**
   - Added `locust>=2.0.0`

---

## How the Flow Works

```
┌─────────────────────────────────────────────────────────────┐
│ Job 1: Data Preprocessing (local) ~30s                     │
└───────────────────┬─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Job 2: Train Models (Azure ML cloud) ~15-20 min            │
│   - Train RF baseline + XGBoost                            │
│   - Log to MLflow + Azure ML Studio                        │
└───────────────────┬─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Job 3: Regression Testing (local) ~5s                      │
│   - Quality gate: 2% threshold                             │
│   - FAIL if performance drops                              │
└───────────────────┬─────────────────────────────────────────┘
                    ↓ (only if passed)
┌─────────────────────────────────────────────────────────────┐
│ Job 4: Version Models (local) ~10s                         │
│   - Create version tag                                     │
│   - Upload versioned artifacts                             │
└───────────────────┬─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Job 5: Deploy to Endpoint (Azure ML cloud) ~5-10 min       │
│   - Register model in Model Registry                       │
│   - Create/update endpoint                                 │
│   - Deploy with scoring script                             │
│   - Route traffic (blue-green)                             │
└───────────────────┬─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Job 6: Load Testing (Locust) ~60s                          │
│   - Get endpoint URI + API key                             │
│   - Simulate 50 users × 60s                                │
│   - Generate HTML report                                   │
└───────────────────┬─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Job 7: Pipeline Summary                                    │
│   - Aggregate all metrics                                  │
│   - Generate final report                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Local Testing

### Test the scoring script locally:
```bash
# Navigate to the repo
cd mlops-cw2-fresh

# Run local scoring test
python score.py
```

### Test Locust locally (without endpoint):
```bash
# Install locust
pip install locust

# Run Locust web UI
locust -f locustfile.py --host=http://localhost:8000

# Open browser to http://localhost:8089
```

### Test Locust in headless mode:
```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 10 \
  --spawn-rate 2 \
  --run-time 30s \
  --headless \
  --html report.html
```

---

## Key Metrics Tracked

### From Load Testing:
- **Request rate** (requests/second)
- **Response time** (min/median/max/95th percentile)
- **Failure rate** (%)
- **Total requests**
- **Concurrent users**

### From Deployment:
- **Endpoint URI**
- **Model version**
- **Deployment status**
- **Traffic routing**

---

## Expected Load Test Results

For a healthy endpoint, you should see:

| Metric | Expected Value |
|--------|---------------|
| Failure rate | < 1% |
| Median response time | < 500ms |
| 95th percentile | < 2000ms |
| Requests/sec | 10-20 |
| Total requests | ~500-1000 |

---

## Troubleshooting

### If deployment fails:
1. Check Azure ML quota for compute instances
2. Verify scoring script syntax
3. Ensure model file exists in iteration_2/
4. Check environment.yml has all dependencies

### If load testing fails:
1. Verify endpoint is deployed and ready
2. Check API key is valid
3. Ensure scoring URI is correct
4. Validate request payload format

---

## Cost Considerations

### Deployment costs:
- **Online Endpoint**: ~$0.10-0.20/hour (Standard_DS2_v2)
- **Model storage**: Minimal (<1GB)
- **API calls**: Free tier available

### Optimization tips:
- Use auto-scaling (0→1→0 instances)
- Delete endpoint after testing if not needed
- Monitor usage in Azure Portal

---

## Next Steps

1. **Push to GitHub** to trigger the complete pipeline
2. **Monitor in GitHub Actions** - Check all 7 jobs
3. **View deployment** in Azure ML Studio
4. **Download load test report** from artifacts
5. **Test endpoint manually** using the scoring URI

---

## Production Checklist

Before deploying to production:

- [ ] Load test passes with <1% failure rate
- [ ] Response times meet SLA requirements
- [ ] API authentication is secure
- [ ] Monitoring/alerting is configured
- [ ] Auto-scaling rules are set
- [ ] Backup/rollback plan exists
- [ ] Cost budget is approved

---

## References

- **Locust Documentation**: https://docs.locust.io/
- **Azure ML Endpoints**: https://learn.microsoft.com/azure/machine-learning/how-to-deploy-managed-online-endpoints
- **GitHub Actions**: https://docs.github.com/actions

---

**✅ Your pipeline now includes full production deployment with load testing!**
