from ping3 import ping
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_host(host):
    """
    Pings a host and returns True if reachable, False otherwise.
    """
    try:
        result = ping(host, timeout=4)
        return result is not None
    except Exception:
        # Handle exceptions that may occur during ping
        return False
    
def ping_hosts(hosts, max_workers=20):
    """
    Pings a dictionary of hosts concurrently and returns a dictionary with the
    hostnames as keys and ping results as values.

    Args:
        hosts (dict): A dictionary where keys are hostnames and values are IPs.
        max_workers (int): The maximum number of threads to use.

    Returns:
        dict: A dictionary with hostnames as keys and ping results (True/False) as values.
    """
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_host = {
            executor.submit(ping_host, ip): name for name, ip in hosts.items()
        }
        for future in as_completed(future_to_host):
            name = future_to_host[future]
            try:
                result = future.result()
            except Exception:
                result = False
            results[name] = result
    return results
