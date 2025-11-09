from flask import Flask, request, jsonify
from logger import logger
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
        # No need to parse request_json if the job doesn't take args
        
        # Create a JobExecution request without overrides if no args are needed
        job_execution_request = run_v2.RunJobRequest(
            name=JOB_FULL_NAME
            # No 'overrides' needed if your job doesn't take dynamic arguments
        )

        logger.info(f"Attempting to execute Cloud Run Job: {JOB_FULL_NAME}")
        operation = client.run_job(request=job_execution_request)
    
        logger.info(f"Cloud Run Job execution started: {operation.name}")
        return jsonify({"status": "Cloud Run Job execution initiated", "operation_name": operation.name}), 202

    except Exception as e:
        logger.error(f"Error initiating Cloud Run Job: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
