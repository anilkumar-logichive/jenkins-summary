import os
import traceback
import boto3
import jenkins
import requests
import json

from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

# jenkins
username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
jenkins_url = os.getenv("JENKINS_URL")

# server
port = os.getenv("PORT")
host = os.getenv("HOST")

# s3 bucket
bucket_name = os.getenv("S3_BUCKET")
access_key = os.getenv("ACCESS_KEY")
secret_key = os.getenv("SECRET_KEY")


s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)


def get_latest_build():
    """Function to get the latest build of jobs and update the last build number to s3 bucket."""
    try:
        server = jenkins.Jenkins(jenkins_url, username=username, password=password)
        jobs = server.get_all_jobs(folder_depth=None)
        for job in jobs:
            job_name = job['name']
            build_number = server.get_job_info(job_name)['nextBuildNumber'] - 1
            if not os.path.exists(f"reports/{job_name}/lastBuildNumber"):
                os.makedirs(f"reports/{job_name}/lastBuildNumber")

            file_path = f"reports/{job_name}/lastBuildNumber/meta.json"
            with open(file_path, "w") as fw:
                fw.write(json.dumps({"lastBuildNumber": build_number}, indent=4))
            resp = s3_client.upload_file(file_path, bucket_name,
                                  f"reports/{job_name}/lastBuildNumber/meta.json")
            print(resp)
            fetch_build_info(job_name, build_number, server)
        return 'success'
    except Exception as e:
        return f"Failed with error: {str(e)}"


def fetch_build_info(job_name, build_number, server):
    """Function to get all job build summary and upload it to s3 bucket."""
    try:
        response = requests.get(f"{jenkins_url}/job/{job_name}/{build_number}/testReport/api/json",
                                auth=HTTPBasicAuth(username, password))

        if not os.path.exists(f"reports/{job_name}/{build_number}"):
            os.makedirs(f"reports/{job_name}/{build_number}")
        file_path = f"reports/{job_name}/{build_number}/test_report.json"
        with open(file_path, "w") as fw:
            try:
                fw.write(json.dumps(response.json(), indent=4))
            except json.decoder.JSONDecodeError as e:
                response = server.get_build_info(job_name, build_number)

                fw.write(json.dumps(response, indent=4))
            except Exception as e:
                fw.write(json.dumps(str(traceback.print_exc()), indent=4))
        s3_client.upload_file(file_path, bucket_name, f"reports/{job_name}/{build_number}/test_report.json")

    except Exception as e:
        return f"Failed with error: {str(e)}"


if __name__ == "__main__":
    get_latest_build()
