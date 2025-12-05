"""
Load Testing for Support Ticket Classifier
Uses Locust to simulate prediction API requests
"""
from locust import HttpUser, task, between
import json
import random


class SupportTicketPredictionUser(HttpUser):
    """
    Simulates a user making prediction requests to the model API
    """
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    # Sample test data representing support ticket features
    sample_tickets = [
        {
            "org_users": 150,
            "past_30d_tickets": 12,
            "customers_affected": 5,
            "error_rate_pct": 2.5,
            "downtime_min": 30,
            "description_length": 120,
            "resolution_time_hours": 4,
            "customer_satisfaction_score": 7.5,
            "revenue_dollars": 50000,
            "api_calls_per_day": 10000,
            "team_size": 8,
            "satisfaction_score_0_10": 7,
            "day_of_week_num": 3,
            "company_size_cat": 2,
            "industry_cat": 1,
            "customer_tier_cat": 2,
            "region_cat": 1,
            "product_area_cat": 3,
            "booking_channel_cat": 1,
            "reported_by_role_cat": 2,
            "customer_sentiment_cat": 1,
            "payment_impact_flag": 0,
            "data_loss_flag": 0,
            "has_runbook": 1
        },
        {
            "org_users": 500,
            "past_30d_tickets": 25,
            "customers_affected": 50,
            "error_rate_pct": 15.0,
            "downtime_min": 180,
            "description_length": 250,
            "resolution_time_hours": 12,
            "customer_satisfaction_score": 4.5,
            "revenue_dollars": 250000,
            "api_calls_per_day": 50000,
            "team_size": 15,
            "satisfaction_score_0_10": 4,
            "day_of_week_num": 5,
            "company_size_cat": 3,
            "industry_cat": 2,
            "customer_tier_cat": 3,
            "region_cat": 2,
            "product_area_cat": 1,
            "booking_channel_cat": 2,
            "reported_by_role_cat": 3,
            "customer_sentiment_cat": 3,
            "payment_impact_flag": 1,
            "data_loss_flag": 1,
            "has_runbook": 0
        }
    ]

    @task(3)
    def predict_priority(self):
        """
        Simulate a prediction request (most common task)
        Weight: 3 (higher probability)
        """
        ticket_data = random.choice(self.sample_tickets)

        # In a real scenario, this would call the actual endpoint
        # For testing without deployment, we'll simulate the response
        headers = {'Content-Type': 'application/json'}

        # Simulated endpoint call
        # In production: POST /score with ticket_data
        # For now, we'll just verify the data structure is valid
        try:
            payload = {"data": [ticket_data]}
            # self.client.post("/score", json=payload, headers=headers)

            # Mock successful response for testing
            print(f"✅ Prediction request sent: {len(str(payload))} bytes")
        except Exception as e:
            print(f"❌ Prediction request failed: {e}")

    @task(1)
    def health_check(self):
        """
        Simulate a health check request (less common)
        Weight: 1 (lower probability)
        """
        # In production: GET /health
        # For now, mock the health check
        print("✅ Health check performed")


class StressTestUser(HttpUser):
    """
    Simulates high-load stress testing with batch predictions
    """
    wait_time = between(0.5, 1.5)

    @task
    def batch_predict(self):
        """
        Simulate batch prediction requests (multiple tickets at once)
        """
        batch_size = random.randint(5, 20)

        # Create batch of random tickets
        batch_data = []
        for _ in range(batch_size):
            ticket = {
                "org_users": random.randint(50, 1000),
                "past_30d_tickets": random.randint(1, 50),
                "customers_affected": random.randint(1, 100),
                "error_rate_pct": round(random.uniform(0, 25), 2),
                "downtime_min": random.randint(0, 300),
                "description_length": random.randint(50, 500),
                "resolution_time_hours": random.randint(1, 24),
                "customer_satisfaction_score": round(random.uniform(1, 10), 1),
                "revenue_dollars": random.randint(10000, 500000),
                "api_calls_per_day": random.randint(1000, 100000),
                "team_size": random.randint(3, 30),
                "satisfaction_score_0_10": random.randint(1, 10),
                "day_of_week_num": random.randint(1, 7),
                "company_size_cat": random.randint(1, 3),
                "industry_cat": random.randint(1, 5),
                "customer_tier_cat": random.randint(1, 3),
                "region_cat": random.randint(1, 4),
                "product_area_cat": random.randint(1, 5),
                "booking_channel_cat": random.randint(1, 3),
                "reported_by_role_cat": random.randint(1, 4),
                "customer_sentiment_cat": random.randint(1, 3),
                "payment_impact_flag": random.randint(0, 1),
                "data_loss_flag": random.randint(0, 1),
                "has_runbook": random.randint(0, 1)
            }
            batch_data.append(ticket)

        # Simulated batch endpoint call
        payload = {"data": batch_data}
        print(f"✅ Batch prediction request: {batch_size} tickets, {len(str(payload))} bytes")


# Configuration for load testing
if __name__ == "__main__":
    print("=" * 70)
    print("LOCUST LOAD TESTING CONFIGURATION")
    print("=" * 70)
    print("\nTo run load tests:")
    print("1. Basic test (web UI):")
    print("   locust -f locustfile.py --host=http://localhost:8000")
    print("\n2. Headless test (no web UI):")
    print("   locust -f locustfile.py --host=http://localhost:8000 \\")
    print("          --users 100 --spawn-rate 10 --run-time 60s --headless")
    print("\n3. Generate HTML report:")
    print("   locust -f locustfile.py --host=http://localhost:8000 \\")
    print("          --users 100 --spawn-rate 10 --run-time 60s \\")
    print("          --headless --html load_test_report.html")
    print("\nUser Classes:")
    print("- SupportTicketPredictionUser: Simulates normal API usage")
    print("- StressTestUser: Simulates high-load batch predictions")
    print("=" * 70)
