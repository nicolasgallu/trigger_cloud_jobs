from flask import Flask, request, jsonify
from utils_logs import logger
from google.cloud import run_v2
import os

app = Flask(__name__)
client = run_v2.JobsClient()

PORT =  int(os.environ.get("PORT"))
print(f"THE PORT IS:{PORT}")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("CLOUD_RUN_REGION")
JOB_NAME = os.getenv("JOB_NAME")
JOB_FULL_NAME = f"projects/{PROJECT_ID}/locations/{REGION}/jobs/{JOB_NAME}"


@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    try:
        
        # Create a JobExecution request
        job_execution_request = run_v2.RunJobRequest(
            name=JOB_FULL_NAME
        )

        logger.info(f"Attempting to execute Cloud Run Job: {JOB_FULL_NAME}")
        client.run_job(request=job_execution_request)
    
        logger.info(f"Cloud Run Job execution started")
        return jsonify({"status": "Cloud Run Job execution initiated"}), 202

    except Exception as e:
        logger.error(f"Error initiating Cloud Run Job: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
