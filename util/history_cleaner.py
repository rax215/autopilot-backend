import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_history(input_file, output_file):
    with open(input_file, 'r') as f:
        history_data = json.load(f)

        for entry in history_data['history']:
            if 'state' in entry and 'screenshot' in entry['state']:
                entry['state'].pop('screenshot')

            if 'state' in entry and 'interacted_elements' in entry['state']:
                for element in entry['state']['interacted_elements']:
                    if element and isinstance(element, dict):
                        if 'page_coordinates' in element:
                            element.pop('page_coordinates')
                        if 'viewport_coordinates' in element:
                            element.pop('viewport_coordinates')
                        if 'viewport_info' in element:
                            element.pop('viewport_info')

    with open(output_file, 'w') as f:
        json.dump(history_data, f, indent=2)

    logger.info(f"History cleaned and saved to {output_file}")
    return output_file