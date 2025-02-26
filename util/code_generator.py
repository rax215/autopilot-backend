import logging
import json
from pathlib import Path
from langchain.schema import HumanMessage, SystemMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_typescript_code(cleaned_history, timestamp, llm):
    try:
        logger.info(f"Generating typescript code ...")
        # Extract interacted elements
        extract_interacted_elements(cleaned_history, timestamp)

        logger.info('Extraction completed')
        # Read the cleaned history
        with open(cleaned_history, 'r') as f:
            history_content = f.read()
        logger.info('history read completed')    
        # Read the prompt template
        with open('prompt/playwright_code_prompt.txt', 'r') as f:
            prompt_template = f.read()
        logger.info('TS prompt completed')    
        # Replace placeholder in prompt with history content
        final_prompt = prompt_template.replace('{json_file_content}', history_content)
        
        # Log the final prompt
        logger.debug(f"\n=== Final Prompt Sent to LLM ===")
        logger.debug(final_prompt)
        logger.debug("=== End of Prompt ===\n")

         # Create messages
        messages = [
            SystemMessage(content="You are a Playwright TypeScript code generator. Generate only the code with no additional text."),
            HumanMessage(content=final_prompt)
        ]
        
        # Get response
        response = llm.invoke(messages)
        logger.debug(f"Generated typescript code: {response.content}")
        
        return response.content
        
    except Exception as e:
        logger.error(f"Error generating typescript code: {e}")
        return None

def extract_interacted_elements(cleaned_history, timestamp):
    try:
        logger.info(f"Extracting interacted elements from history: {cleaned_history}")
        with open(cleaned_history, 'r') as f:
            history_data = json.load(f)
            interacted_elements = []
            # Iterate through history and extract interacted elements
            history_entries = history_data.get('history', [])
            logger.debug(f"Found {len(history_entries)} history entries")
            
            for entry in history_entries:
                state = entry.get('state', {})
                elements = state.get('interacted_element', [])
                logger.debug(f"Found {len(elements)} elements in history entry")
                
                for element in elements:
                    if element and isinstance(element, dict):  # Skip None values and ensure it's a dictionary
                        # Extract required attributes
                        element_data = {
                            'tag_name': element.get('tag_name'),
                            'xpath': element.get('xpath'),
                            'attributes': element.get('attributes'),
                            'css_selector': element.get('css_selector'),
                            'entire_parent_branch_path': element.get('entire_parent_branch_path')
                        }
                        interacted_elements.append(element_data)
                        logger.debug(f"Added element with tag {element_data['tag_name']}")
                        # Create output file path in the same timestamp folder as cleaned history
            history_folder = Path(cleaned_history).parent
            elements_file_path = history_folder / f'elements_{timestamp}.json'
            
            # Save extracted elements to new JSON file
            with open(elements_file_path, 'w') as f:
                json.dump({'interacted_elements': interacted_elements}, f, indent=2)
            
            logger.info('Extraction completed')
            # Verify the file was saved correctly
            if elements_file_path.exists():
                logger.debug(f"Successfully saved {len(interacted_elements)} interacted elements to {elements_file_path}")
            else:
                logger.error(f"Failed to save elements file at {elements_file_path}")
                raise FileNotFoundError(f"Elements file was not created at {elements_file_path}")
            
    except Exception as e:
        logger.error(f"Error extracting interacted elements: {e}")
        return None