import threading


def run_with_timeout(func, timeout=20):
    """
    Runs a function with timeout protection.
    If the function takes too long, Jarvis won't freeze.
    """

    result = {"value": None}

    def target():
        try:
            result["value"] = func()
        except Exception as e:
            result["value"] = f"Skill error: {e}"

    thread = threading.Thread(target=target)
    thread.start()

    thread.join(timeout)

    if thread.is_alive():
        return "Command timed out."

    return result["value"]