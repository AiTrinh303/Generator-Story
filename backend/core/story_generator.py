import re
from sqlalchemy.orm import Session
from typing import Dict, Any

try:
    from backend.core.models import StoryLLMResponse, StoryNodeLLM
    from backend.models.story import Story, StoryNode
except ImportError:
    from core.models import StoryLLMResponse, StoryNodeLLM
    from models.story import Story, StoryNode

class StoryGenerator:

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        story_structure = cls._build_local_story(theme)

        story_db = Story(
            title=story_structure["title"],
            session_id=session_id,
        )
        db.add(story_db)
        db.flush()

        root_node_data = story_structure["rootNode"]
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)
        db.commit()
        return story_db

    @staticmethod
    def _clean_text(text: str) -> str:
        if not text:
            return text
        cleaned = re.sub(r'(?m)^\s*#+\s*', '', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    @classmethod
    def _build_local_story(cls, theme: str) -> Dict[str, Any]:
        theme_text = theme.strip().title() or "Magical"
        theme_lower = theme.strip().lower()

        def make_title() -> str:
            if any(word in theme_lower for word in ["castle", "kingdom", "palace"]):
                if theme_lower == "castle":
                    return "The Castle Kingdom Tale"
                return f"The {theme_text} Castle Kingdom Tale"
            if any(word in theme_lower for word in ["ocean", "sea", "water"]):
                if theme_lower == "ocean":
                    return "Ocean Dream"
                return f"{theme_text} Ocean Dream"
            if any(word in theme_lower for word in ["forest", "tree", "wood"]):
                if theme_lower == "forest":
                    return "Forest Tale"
                return f"The {theme_text} Forest Tale"
            if "space" in theme_lower:
                if theme_lower == "space":
                    return "Star Journey"
                return f"{theme_text} Star Journey"
            if "pirate" in theme_lower:
                if theme_lower == "pirate":
                    return "Treasure Voyage"
                return f"{theme_text} Treasure Voyage"
            if "magic" in theme_lower:
                if theme_lower == "magic":
                    return "Sparkle Tale"
                return f"The {theme_text} Sparkle Tale"
            if "garden" in theme_lower:
                if theme_lower == "garden":
                    return "Garden Celebration"
                return f"The {theme_text} Garden Celebration"
            return f"A {theme_text} Story"

        def make_opening() -> str:
            if "space" in theme_lower:
                return (
                    f"A soft glow of stars surrounds you as you step into the {theme_lower} world. "
                    "This story begins with a curious heart, ready to explore bright planets and friendly stars. "
                    "Every choice leads to a caring friend and a gentle surprise."
                )
            if any(word in theme_lower for word in ["ocean", "sea", "water"]):
                return (
                    f"The gentle waves of the {theme_lower} world sing softly as your story begins. "
                    "You feel calm and brave, ready to meet friendly sea creatures and discover hidden wonders. "
                    "This path invites you to share, help, and dream together."
                )
            if any(word in theme_lower for word in ["forest", "tree", "wood"]):
                return (
                    f"The {theme_lower} forest is full of warm light and soft leaves. "
                    "You begin your story among kind animals and whispering trees that invite you to play. "
                    "Every step feels safe and full of caring choices."
                )
            if any(word in theme_lower for word in ["castle", "kingdom", "palace"]):
                return (
                    f"A bright flag waves above the {theme_lower} castle as your story begins. "
                    "The halls are gentle and the people are friendly, ready to share a magical day with you. "
                    "Your first choice is warm and full of hope."
                )
            if "pirate" in theme_lower:
                return (
                    f"A playful pirate ship sails into the {theme_lower} sky of your story. "
                    "The crew is kind and curious, and you start a fun journey filled with treasure and friendship. "
                    "You can choose the kindest adventure."
                )
            if "magic" in theme_lower:
                return (
                    f"A shimmer of magic fills the air, and the {theme_lower} world feels bright and welcoming. "
                    "Your story begins with a gentle spell of wonder and a promise of fun discoveries. "
                    "The choices are full of kindness and joy."
                )
            return (
                f"The {theme_lower} world feels sweet and inviting today. "
                "You begin your story surrounded by friendly faces and a gentle promise of a happy journey. "
                "Every decision helps you learn something wonderful."
            )

        return {
            "title": cls._clean_text(make_title()),
            "rootNode": {
                "content": cls._clean_text(make_opening()),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": f"Follow the {theme_lower} path",
                        "nextNode": {
                            "content": cls._clean_text(
                                f"You choose the {theme_lower} path and find a gentle surprise around every corner. "
                                "A friend asks for your help, and your kind choice will make the story shine. "
                                "This path leads you to a thoughtful moment where your heart can be brave and caring."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Help the friend with a kind idea",
                                    "nextNode": {
                                        "content": cls._clean_text(
                                            "You help the friend, and the whole place feels happier. "
                                            "Your kindness becomes the best treasure, and you end with a joyful feeling. "
                                            "Everyone around you smiles, and the warm ending reminds you that good hearts make every adventure bright."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Keep exploring the lovely path",
                                    "nextNode": {
                                        "content": cls._clean_text(
                                            "You keep exploring and discover a quiet place where you learn something new. "
                                            "This gentle ending reminds you that curiosity and calm are a wonderful part of a story. "
                                            "The peaceful scene helps you feel happy and safe, with kind memories to carry home."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": f"Visit the bright {theme_lower} place",
                        "nextNode": {
                            "content": cls._clean_text(
                                f"The bright {theme_lower} place is filled with smiling friends and warm light. "
                                "You feel safe and excited as a new choice appears in front of you. "
                                "The next step invites you to share joy or discover a lovely secret spot."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Share a happy game with friends",
                                    "nextNode": {
                                        "content": cls._clean_text(
                                            "You share a happy game, and everyone laughs together. "
                                            "This cheerful ending shows that friendship makes every theme more special. "
                                            "You finish with a bright heart and a memory of how much kindness can sparkle."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Find a secret gentle spot",
                                    "nextNode": {
                                        "content": cls._clean_text(
                                            "You find a secret spot and feel peaceful inside. "
                                            "You learn that calm moments can be as magical as exciting choices. "
                                            "The story ends softly, with a warm feeling of comfort and wonder."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content,
            is_root=is_root,
            is_ending=node_data.isEnding,
            is_winning_ending=node_data.isWinningEnding,
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and node_data.options:
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode
                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, is_root=False)
                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id,
                })
            node.options = options_list

        db.flush()
        return node

