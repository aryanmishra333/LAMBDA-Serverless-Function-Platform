import os
import time
import uuid
from backend.db.models import log_execution,get_function_code
import docker

client = docker.from_env()

container_pool = {}

def get_or_create_container(file_path, language, use_gvisor=False):
    """
    Fetch an existing container from the pool or create a new one.
    """
    container_key = f"{file_path}_{language}_{use_gvisor}"
    
    if container_key in container_pool:
        print(f"Reusing container for {container_key}")
        return container_pool[container_key]
    else:
        print(f"Creating new container for {container_key}")
        container = create_new_container(file_path, language, use_gvisor)
        container_pool[container_key] = container
        return container


def create_new_container(file_path, language, use_gvisor=False):
    """
    Create a new container for executing the function.
    """
    container_name = f"lambda_{uuid.uuid4().hex}"
    if language == "python":
        base_image = "lambda_base_python"
    elif language == "javascript" or language == "node":
        base_image = "lambda_base_node"
    elif language == "verilog":
        base_image = "lambda_base_verilog"
    else:
        base_image = "lambda_base_python"  # default fallback
    
    file_ext = file_path.split('.')[-1]
    container_path = f"/app/code.{file_ext}"
    
    try:
        if use_gvisor:
            if language == "verilog":
                command = ["iverilog", "-o", "/app/output", container_path, "&&", "/app/output"]
            elif language == "python":
                command = ["python3", container_path]
            else:
                command = ["node", container_path]
                
            container = client.containers.run(
                image=base_image,
                command=command,
                volumes={os.path.abspath(file_path): {"bind": container_path, "mode": "ro"}},
                name=container_name,
                network_disabled=True,
                detach=True,
                mem_limit='128m',
                stderr=True,
                runtime='runsc'
            )
        else:
            if language == "verilog":
                command = ["/bin/bash", "-c", f"iverilog -o /app/output {container_path} && /app/output"]
            elif language == "python":
                command = ["python3", container_path]
            else:
                command = ["node", container_path]
                
            container = client.containers.run(
                image=base_image,
                command=command,
                volumes={os.path.abspath(file_path): {"bind": container_path, "mode": "ro"}},
                name=container_name,
                network_disabled=True,
                detach=True,
                mem_limit='128m',
                stderr=True,
            )
        return container
    except Exception as e:
        raise Exception(f"Error creating container: {str(e)}")


def run_function_in_container(function_id, language, timeout, use_gvisor=False):
    code = get_function_code(function_id)
    if language == "python":
        file_ext = "py"
    elif language == "javascript" or language == "node":
        file_ext = "js"
    elif language == "verilog":
        file_ext = "v"
    else:
        file_ext = "py"  # default fallback
        
    temp_file_path = f"/tmp/temp_{uuid.uuid4().hex}.{file_ext}"

    with open(temp_file_path, "w") as f:
        f.write(code)

    container = get_or_create_container(temp_file_path, language, use_gvisor)
    
    try:
        start_time = time.time()

        result = container.wait(timeout=timeout)
        logs = container.logs().decode()

        time.sleep(0.5)
        stats = container.stats(stream=False)

        memory_usage = stats.get("memory_stats", {}).get("usage", 0)
        cpu_percent = calculate_cpu_percent(stats)

        end_time = time.time()
        exec_time = round(end_time - start_time, 4)

        log_execution(function_id, exec_time, memory_usage, cpu_percent, status="success")

        performance_data = {
            "result": logs,
            "status": "success",
            "exec_time": exec_time,
            "mem_usage": memory_usage,
            "cpu_percent": cpu_percent,
            "runtime": "gVisor" if use_gvisor else "Docker"
        }

        return performance_data

    except Exception as e:
        return {"error": f"Error running the function: {str(e)}"}

    finally:
        try:
            container.remove(force=True)
        except Exception as cleanup_error:
            print(f"Error cleaning up container: {cleanup_error}")
    

def calculate_cpu_percent(stats):
    cpu_total = stats.get("cpu_stats", {}).get("cpu_usage", {}).get("total_usage", 0)
    precpu_total = stats.get("precpu_stats", {}).get("cpu_usage", {}).get("total_usage", 0)
    system_total = stats.get("cpu_stats", {}).get("system_cpu_usage", 1)
    presystem_total = stats.get("precpu_stats", {}).get("system_cpu_usage", 1)

    cpu_delta = cpu_total - precpu_total
    system_delta = system_total - presystem_total
    cpu_percent = round((cpu_delta / system_delta) * 100.0, 2) if system_delta > 0 else 0.0
    return cpu_percent
