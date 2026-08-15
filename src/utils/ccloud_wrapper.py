import subprocess
import json
import shlex

def execute_ccloud_command(command_str: str) -> dict:
    """
    Executes a ccloud CLI command safely and returns JSON output.
    Example: execute_ccloud_command("ccloud cluster list --format json")
    """
    try:
        args = shlex.split(command_str)
        # Force json output if supported
        if "--format" not in args:
            args.extend(["--format", "json"])
            
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True
        )
        
        try:
            return {"status": "SUCCESS", "data": json.loads(result.stdout)}
        except json.JSONDecodeError:
            return {"status": "SUCCESS", "data": result.stdout.strip()}
            
    except subprocess.CalledProcessError as e:
        return {
            "status": "ERROR",
            "error": e.stderr.strip() or str(e),
            "returncode": e.returncode
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}
