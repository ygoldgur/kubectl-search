#!/usr/bin/env python3

from kubernetes import client, config
import sys
import pyperclip


def check_pod_args(pod, arg1, arg2):

    # Check if the pod has containers and args
    if not pod.spec.containers:
        return False
    
    container = pod.spec.containers[0]  # Focusing on the first container
    if not container.args:
        return False

    # Normalize arg1 for case-insensitive comparison
    arg1 = arg1.lower()
    # Find arg1 and check if arg2 follows it directly
    for i, arg in enumerate(container.args):
        if "=" in arg:
            split_args = arg.split("=")
            container.args[i] = split_args[0]
            container.args.insert(i + 1, split_args[1])
        
        if arg1 in container.args[i].lower() and i + 1 < len(container.args) and arg2 in container.args[i + 1]:
            return True

    return False

def search(arg1, arg2):
    # Load the kubeconfig file
    config.load_kube_config()

    # Create a client for the CoreV1API
    v1 = client.CoreV1Api()

    # Get all pods across all namespaces
    all_pods = v1.list_namespaced_pod(namespace="default")
    counter = 0

    # Filter pods by label value
    for pod in all_pods.items:

        if check_pod_args(pod, arg1, arg2):
            print(f"{pod.metadata.name}  {pod.metadata.namespace}")
            counter += 1

    if counter == 1:
        # Copy the pod name to clipboard
        pyperclip.copy(pod.metadata.name)
        print("Pod name copied to clipboard")

if __name__ == "__main__":
    
    if len(sys.argv) != 3:

        print("Usage: search <arg1> <arg2>")
        sys.exit(1)
    
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    search(arg1, arg2)