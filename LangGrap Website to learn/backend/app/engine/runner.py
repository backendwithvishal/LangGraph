import sys
import io
import time
import traceback
import multiprocessing
from typing import Dict, Any, Optional

def _exec_target(code: str, conn):
    """Worker target for executing arbitrary python code in an isolated process."""
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = stdout_capture
    sys.stderr = stderr_capture

    try:
        # Provide common LangGraph environment
        exec_globals = {
            "__name__": "__main__",
        }
        exec(code, exec_globals)
        out = stdout_capture.getvalue()
        err = stderr_capture.getvalue()
        conn.send({"success": True, "stdout": out, "stderr": err, "error": None})
    except Exception as e:
        out = stdout_capture.getvalue()
        err = stderr_capture.getvalue()
        conn.send({
            "success": False,
            "stdout": out,
            "stderr": err,
            "error": f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        })
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        conn.close()

class CodeRunner:
    @staticmethod
    def run_code(code: str, timeout_seconds: int = 10) -> Dict[str, Any]:
        start_time = time.time()
        
        # In-process execution with captured stdout/stderr for speed and portability
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        sys.stdout = stdout_capture
        sys.stderr = stderr_capture

        try:
            exec_globals = {
                "__name__": "__main__",
            }
            exec(code, exec_globals)
            out = stdout_capture.getvalue()
            err = stderr_capture.getvalue()
            exec_time = round((time.time() - start_time) * 1000, 2)
            
            return {
                "success": True,
                "stdout": out if out else "(Executed successfully with no stdout output)",
                "stderr": err,
                "result": None,
                "error": None,
                "execution_time_ms": exec_time
            }
        except Exception as e:
            out = stdout_capture.getvalue()
            err = stderr_capture.getvalue()
            exec_time = round((time.time() - start_time) * 1000, 2)
            
            return {
                "success": False,
                "stdout": out,
                "stderr": err,
                "result": None,
                "error": f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}",
                "execution_time_ms": exec_time
            }
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
