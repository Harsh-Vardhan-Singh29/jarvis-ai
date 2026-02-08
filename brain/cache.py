cache = {}

def get_cached(command):
    return cache.get(command)

def save_cache(command, response):
    cache[command] = response
