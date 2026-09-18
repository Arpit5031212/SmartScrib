from enum import StrEnum, auto
from schemas.modes import Mode

from pydantic import BaseModel


class Confidence(StrEnum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

class ClassifierOutput(BaseModel):
    mode: Mode
    confidence: Confidence
    reasoning: str
    
class ClassifierResult(BaseModel):
    output: ClassifierOutput | None
    needs_clarification: bool
    clarification_message: str | None