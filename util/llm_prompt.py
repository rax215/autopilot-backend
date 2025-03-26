import logging
from langchain.schema import HumanMessage, SystemMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def llm_interation(prompt,llm):
    try:
        logger.info(f"Interacting with LLM ...")
         # Create messages
        messages = [
            SystemMessage(content="You are a technical code advisor"),
            HumanMessage(content=prompt)
        ]
        
        # Get response
        response = llm.invoke(messages)
        #logger.info(f"llm response: {response.content}")        
        return response.content
    
    except Exception as e:
        logging.error(f"Error llm interaction: {e}")
        return None