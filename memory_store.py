import json

def load_memory():
    try:
        with open('memory.json', 'r') as f:
            memory = json.load(f)
            if isinstance(memory, list):
                return memory
            else:
                return []
    except:
        return []


def save_memory(memory):
    # Ensure we're saving only a list
    if isinstance(memory, list):
        with open('memory.json', 'w') as f:
            json.dump(memory, f)
    else:
        raise ValueError("Expected a list to save in memory.json")