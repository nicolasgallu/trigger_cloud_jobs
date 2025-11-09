from flask import Flask, request, jsonify
from google.cloud import run_v2
import os

app = Flask(__name__)
client = run_v2.JobsClient()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("CLOUD_RUN_REGION")
JOB_NAME = os.getenv("JOB_NAME")
JOB_FULL_NAME = f"projects/{PROJECT_ID}/locations/{REGION}/jobs/{JOB_NAME}"

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    try:
        request_json = request.get_json(silent=True)
        
        # Extract parameters for the job from the request body
        # For example, if your job expects a 'url' argument
        job_args = []
        if request_json and 'url' in request_json:
            job_args.append(request_json['url'])
        else:
            # Provide a default or handle cases where no URL is given
            job_args.append("https://www.google.com") 
        
        # Create a JobExecution object
        job_execution_request = run_v2.RunJobRequest(
            name=JOB_FULL_NAME,
            overrides=run_v2.RunJobRequest.Overrides(
                args=job_args # Pass arguments to your job
            )
        )

        print(f"Attempting to execute Cloud Run Job: {JOB_FULL_NAME} with args: {job_args}")
        operation = client.run_job(request=job_execution_request)
        
        # The operation is long-running, but we don't need to wait for it here.
        # We just confirm it started.
        print(f"Cloud Run Job execution started: {operation.name}")

        return jsonify({"status": "Cloud Run Job execution initiated", "operation_name": operation.name}), 202

    except Exception as e:
        print(f"Error initiating Cloud Run Job: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
