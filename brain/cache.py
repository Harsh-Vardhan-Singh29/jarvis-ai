cache = {}

def get_cached(command):
    return cache.get(command)

def save_cache(command, response):
    # 🔒 Never cache empty / whitespace responses
    if not response or not response.strip():
        return
    cache[command] = response.strip()
