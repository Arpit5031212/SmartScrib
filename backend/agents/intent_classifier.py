import json
import logging
from langchain_ollama import ChatOllama
from schemas.classifier import ClassifierOutput, ClassifierResult, Confidence
from config.settings import get_settings
from schemas.modes import Mode, MODE_DESCRIPTIONS
from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)
settings = get_settings()

classifier = ChatOllama(
    model=settings.ollama_llm_model,
    base_url=settings.ollama_base_url,
    client_kwargs={
        "headers": {
            "Authorization": f"Bearer {settings.ollama_api_key}"
        }
    }
)

def built_system_prompt() -> str:
    modes = ", ".join(mode.value for mode in Mode)
    
    mode_descriptions = "\n".join(
        f"- {mode.value}: {description}"
        for mode, description in MODE_DESCRIPTIONS.items()
    )
    
    output_schema = {
        "mode": f"one of the modes from: {modes}",
        "confidence": f"one of: {', '.join(confidence.value for confidence in Confidence)}",
        "reasoning": "a brief explanation of why you chose this mode"
    }
    
    prompt = f"""You are an intent classifier for the text-based agent SmartScribe, a document generation assistant. Your job is to classify the user's message into one of the following modes: {modes}.
    Always respond with JSON object only. No explanation outside the JSON.
    The JSON should have the following format:
    {json.dumps(output_schema, indent=2)}
    Here are the descriptions of each mode:
    {mode_descriptions}
    Classify the user's message into one of the modes based on the content and intent.
    """
    
    return prompt

SYSTEM_PROMPT = built_system_prompt()

def _parse_response(response:str) -> ClassifierOutput:
    try:
        content = response.strip()
        if content.startswith("```json"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:].strip()
        
        parsed = json.loads(content)
        data = ClassifierOutput.model_validate(parsed)
        return data
    except Exception as e:
        logger.exception(f"Error parsing classifier response: {e}")
        raise

async def classify_intent(message: str) -> ClassifierResult:
    system_msg = SystemMessage(content=SYSTEM_PROMPT)
    human_msg = HumanMessage(content=message)
    message_list = [system_msg, human_msg]
    
    response = await classifier.ainvoke(messages=message_list)
    try:
        parsed_output = _parse_response(response.content)
        if parsed_output.confidence == Confidence.LOW:
            logger.warning(f"Low confidence in intent classification for message: {message}")
            return ClassifierResult(
                output=None,
                needs_clarification=True,
            clarification_message="I'm not sure what you'd like to do. Are you trying to document a meeting, log a task, create a timesheet, rewrite text, take notes, or generate a report?"
        )
        return ClassifierResult(output=parsed_output, needs_clarification=False, clarification_message=None)
    except Exception as e:
        logger.exception(f"Error in intent classification: {e}")
        return ClassifierResult(
            output=None,
            needs_clarification=True,
            clarification_message="I had trouble understanding your request. Could you please clarify what you'd like to do?"
        )