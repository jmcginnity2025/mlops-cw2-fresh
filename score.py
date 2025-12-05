"""
Azure ML Scoring Script for Support Ticket Classifier
Loads the XGBoost model and serves predictions via REST API
"""
import json
import pickle
import numpy as np
import os


def init():
    """
    Initialize the model when the endpoint is created or updated
    This function is called once when the container starts
    """
    global model

    # Azure ML provides the model path via AZUREML_MODEL_DIR environment variable
    model_path = os.getenv("AZUREML_MODEL_DIR", ".")
    model_file = os.path.join(model_path, "iteration_2_model.pkl")

    # Load the trained XGBoost model
    try:
        with open(model_file, "rb") as f:
            model = pickle.load(f)
        print(f"✅ Model loaded successfully from: {model_file}")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        raise


def run(raw_data):
    """
    Make predictions on incoming data

    Args:
        raw_data: JSON string with format: {"data": [[feature1, feature2, ...]]}

    Returns:
        JSON string with predictions: {"predictions": [1, 2, 3, ...]}
    """
    try:
        # Parse input JSON
        data = json.loads(raw_data)

        # Extract feature array
        input_data = np.array(data["data"])

        print(f"📊 Received {len(input_data)} samples for prediction")

        # Make prediction (model outputs 0,1,2)
        predictions = model.predict(input_data)

        # Remap from 0,1,2 back to original labels 1,2,3
        predictions = predictions + 1

        # Return predictions as JSON
        result = {
            "predictions": predictions.tolist(),
            "model": "XGBoost",
            "num_samples": len(predictions)
        }

        print(f"✅ Predictions complete: {predictions.tolist()}")
        return json.dumps(result)

    except Exception as e:
        error_msg = f"Prediction error: {str(e)}"
        print(f"❌ {error_msg}")
        return json.dumps({"error": error_msg})


# Local testing
if __name__ == "__main__":
    print("="*70)
    print("SCORING SCRIPT - LOCAL TESTING")
    print("="*70)

    # Simulate init
    print("\n1. Initializing model...")
    init()

    # Test data (sample support ticket features)
    test_input = {
        "data": [[
            150,  # org_users
            12,   # past_30d_tickets
            5,    # customers_affected
            2.5,  # error_rate_pct
            30,   # downtime_min
            120,  # description_length
            4,    # resolution_time_hours
            7.5,  # customer_satisfaction_score
            50000,  # revenue_dollars
            10000,  # api_calls_per_day
            8,    # team_size
            7,    # satisfaction_score_0_10
            3,    # day_of_week_num
            2,    # company_size_cat
            1,    # industry_cat
            2,    # customer_tier_cat
            1,    # region_cat
            3,    # product_area_cat
            1,    # booking_channel_cat
            2,    # reported_by_role_cat
            1,    # customer_sentiment_cat
            0,    # payment_impact_flag
            0,    # data_loss_flag
            1     # has_runbook
        ]]
    }

    print("\n2. Testing prediction...")
    raw_data = json.dumps(test_input)
    result = run(raw_data)

    print("\n3. Result:")
    print(result)
    print("\n" + "="*70)
    print("✅ Local test successful!")
    print("="*70)
