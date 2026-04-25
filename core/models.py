from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class StoryOptionLLM(BaseModel):
    text: str = Field (description="The text of the story option shown to the user.")
    nextNode: Dict[str, Any] = Field (description="The next node content and its options.")

class StoryNodeLLM(BaseModel):
    content: str = Field (description="The main content of the story node.")
    isEnding: bool = Field (description="Whether this node is an ending point in the story.") 
    isWinningEnding: bool = Field (description="Whether this node is a winning ending point in the story.")
    options: Optional[List[StoryOptionLLM]] = Field (default=None, description="The options available at this story node, if any.")

class StoryLLMResponse(BaseModel):
    title: str = Field (description="The title of the story.")    
    rootNode: StoryNodeLLM = Field (description="The root node of the story.")