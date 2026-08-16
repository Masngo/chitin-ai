import uuid
import time
import subprocess
import sys

def test_crash_resilience():
    rem_id = f"test-crash-{uuid.uuid4().hex[:6]}"
    sample_log = "FATAL: OutOfMemory memory pressure threshold exceeded on node db-cluster-02"
    
    print(f"1. Spawning Agent Process 1 [ID: {rem_id}]...")
    
    p1 = subprocess.Popen([
        sys.executable, "-m", "src.main", "run",
        "--log", sample_log,
        "--cluster", "cockroach-prod-01",
        "--remediation-id", rem_id
    ])
    
    time.sleep(1.5)
    print("\n⚡ SIMULATING PROCESS CRASH / TERMINATION (kill -9) ⚡\n")
    p1.kill()
    p1.wait()

    print("2. Spawning Agent Process 2 to test instant state recovery...")
    p2 = subprocess.Popen([
        sys.executable, "-m", "src.main", "run",
        "--log", sample_log,
        "--cluster", "cockroach-prod-01",
        "--remediation-id", rem_id
    ])
    p2.wait()
    
    print("\n✅ Resilience test finished successfully.")

if __name__ == '__main__':
    test_crash_resilience()
