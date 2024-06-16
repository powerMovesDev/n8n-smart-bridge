import os
import subprocess
import threading
import queue
import time

import requests
from dotenv import load_dotenv

from bridge.graph.models.output_models import N8TunnelOutput
from bridge.util.GptModels import GptModels

load_dotenv()
api_url = os.getenv("N8N_API_URL")
api_key = os.getenv("N8N_API_KEY")


def post_workflow_request(workflow_payload):
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'X-N8N-API-KEY': f'{api_key}'
    }
    response = requests.post(f"{api_url}/api/v1/workflows", json=workflow_payload, headers=headers)
    return response.json(), response.status_code


def retrieve_workflow(workflow_id):
    headers = {
        'Content-Type': 'application/json',
        'X-N8N-API-KEY': f'{api_key}'
    }
    response = requests.get(f"{api_url}/api/v1/workflows/{workflow_id}", headers=headers)
    return response.json(), response.status_code


def activate_workflow(workflow_id, override_url=None):
    headers = {
        'Content-Type': 'application/json',
        'X-N8N-API-KEY': f'{api_key}'
    }
    response = requests.post(f"{override_url if override_url else api_url}/api/v1/workflows/{workflow_id}/activate", headers=headers)
    return response.json(), response.status_code


def register_test_webhook(tunnel_url, workflow_id, webhook_node_name='Webhook'):
    headers = {
        'Content-Type': 'application/json',
        'X-N8N-API-KEY': f'{api_key}'
    }
    response = requests.post(f"{tunnel_url}/api/v1/workflows/{workflow_id}/webhooks/{webhook_node_name}/test",
                             headers=headers)
    return response.json(), response.status_code


def read_pipe(pipe, q):
    for line in iter(pipe.readline, b''):
        q.put(line.decode('utf-8'))


def start_n8n_with_tunnel():
    command = ["npx", "n8n", "start", "--tunnel"]
    if os.name == 'nt':  # For Windows
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:  # For Unix/Linux
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    q_stdout = queue.Queue()
    q_stderr = queue.Queue()

    stdout_thread = threading.Thread(target=read_pipe, args=(process.stdout, q_stdout))
    stderr_thread = threading.Thread(target=read_pipe, args=(process.stderr, q_stderr))

    stdout_thread.start()
    stderr_thread.start()

    # Wait for 20 seconds
    print("Waiting for n8n to start...")
    time.sleep(20)

    return process, q_stdout, q_stderr


if __name__ == "__main__":
    process, q_stdout, q_stderr = start_n8n_with_tunnel()

    # Retrieve output and error messages from the queues
    stdout = ""
    while not q_stdout.empty():
        stdout += q_stdout.get()

    stderr = ""
    while not q_stderr.empty():
        stderr += q_stderr.get()

    print("stdout:", stdout)
    print("stderr:", stderr)
    if stdout == "":
        print("Failed to start n8n with tunnel.")
        exit(1)
    tunnel_url_resp = GptModels().gpt_4_omni.with_structured_output(N8TunnelOutput).invoke(
        f"Retrieve the tunnel URL from the following output of the initialization of a tunnel instance of n8 for "
        f"testing:\n{stdout}"
    ).tunnel_url
    print(f"Tunnel URL: {tunnel_url_resp}")
    workflow, status_code = activate_workflow("X6ZxSzxw2Rf1kGKD", tunnel_url_resp)
    print(workflow)
    if status_code != 200:
        print(f"Failed to activate workflow: {workflow}")
        exit(1)
    print("Workflow activated successfully.")

    print(stdout)
    response, status_code = register_test_webhook(tunnel_url_resp, "X6ZxSzxw2Rf1kGKD")
    print(f"Status Code: {status_code}\n", response)

