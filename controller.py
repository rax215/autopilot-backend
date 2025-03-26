from browser_use import Agent
import time
import os
import logging
from flask import jsonify
from util.util import get_llm
from util.history_cleaner import clean_history
from util.code_generator import generate_typescript_code
from util.llm_prompt import llm_interation

# Configure logging
logging.basicConfig(level=logging.ERROR)

timestamp = ''

async def process_data(data):
    if not data.get('llmProvider'):
        return jsonify({"error": "Missing llmProvider"}), 400
    if not data.get('model'):
        return jsonify({"error": "Missing model"}), 400
    if not data.get('apiKey'):
        return jsonify({"error": "Missing apiKey"}), 400

    llm = await get_llm(data['llmProvider'], data['model'], data['apiKey'])
    if(data.get('generatePlaywrightScript') == True):
        history_file = await execute_agent(data['prompt'], llm)
        playwrightscript =  await generate_testcase(data['prompt'], llm, history_file)
        return {
        "generatedScript": playwrightscript        
        }
    else:
        resp = await llm_interation(data['prompt'], llm)
        return {"response": resp}


async def execute_agent(prompt, llm):
    try:
        agent = Agent(task=prompt, llm=llm)
        global timestamp
        timestamp = int(time.time())
        history = await agent.run()

        history_file = os.path.join('temp/history', f"{timestamp}.json")
        agent.save_history(history_file)
        return jsonify({"status": "success", "history": history}), 200
    except Exception as e:
        logging.error(f"Error executing agent: {e}")
        return history_file

async def generate_testcase(prompt, llm, history_file):
    global timestamp
    cleaned_history_file = clean_history(history_file, f'temp/cleanedHistory/{timestamp}.json')
    typescript_code = generate_typescript_code(cleaned_history_file, timestamp, llm)
    return format(typescript_code)

def format(typescript_code):
    typescript_code = "\n".join(
                                    line for line in typescript_code.split("\n")
                                    if not line.strip().startswith("```typescript") and not line.strip() == "```"
                                ).strip()
    return typescript_code