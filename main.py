import os
import sys
import traceback
import boto3
import jenkins
import requests
import json

from requests.auth import HTTPBasicAuth

# jenkins
username = sys.argv[1]
token = sys.argv[2]
jenkins_url = sys.argv[3]
job_name = sys.argv[4]
build_number = sys.argv[5]

# s3 bucket
bucket_name = sys.argv[6]
access_key = sys.argv[7]
secret_key = sys.argv[8]

s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)


def fetch_build_info():
    """Function to get last job build summary and upload it to s3 bucket."""
    try:

        if not os.path.exists(f"reports/{job_name}/lastBuildNumber"):
            os.makedirs(f"reports/{job_name}/lastBuildNumber")

        file_path = f"reports/{job_name}/lastBuildNumber/meta.json"
        with open(file_path, "w") as fw:
            fw.write(json.dumps({"lastBuildNumber": build_number}, indent=4))
        s3_client.upload_file(file_path, bucket_name,
                              f"reports/{job_name}/lastBuildNumber/meta.json", ExtraArgs={'ACL': 'public-read'})

        response = requests.get(f"{jenkins_url}/job/{job_name}/{build_number}/testReport/api/json",
                                auth=HTTPBasicAuth(username, token))

        if not os.path.exists(f"reports/{job_name}/{build_number}"):
            os.makedirs(f"reports/{job_name}/{build_number}")
        file_path = f"reports/{job_name}/{build_number}/test_report.json"
        with open(file_path, "w") as fw:
            try:
                fw.write(json.dumps(response.json(), indent=4))
            except json.decoder.JSONDecodeError:
                server = jenkins.Jenkins(jenkins_url, username=username, password=token)
                response = server.get_build_info(job_name, build_number)
                fw.write(json.dumps(response, indent=4))

        s3_client.upload_file(file_path, bucket_name, f"reports/{job_name}/{build_number}/test_report.json")

    except Exception as e:
        file_path = f"reports/{job_name}/{build_number}/error.log"
        with open(file_path, "a+") as fw:
            fw.write(json.dumps(str(traceback.print_exc()), indent=4))
        s3_client.upload_file(file_path, bucket_name, f"reports/{job_name}/{build_number}/error.log")
        return f"Failed with error: {str(e)}"


if __name__ == "__main__":
    fetch_build_info()
