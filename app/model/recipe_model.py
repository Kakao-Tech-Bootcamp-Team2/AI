from pydantic import BaseModel
from typing import Dict,List

class Recipe(BaseModel) :
    recipe_id : int
    title : str
    ingredients : Dict[str,List[str]]
    steps : List[str]

    def prepare_text_for_embedding(self) -> str:
        ingredients_text = '\n'.join([
            f"{category}: {', '.join(items)}"
            for category, items in self.ingredients.items()
        ])
        steps_text = '\n'.join([
            f"단계 {i+1}: {step}"
            for i, step in enumerate(self.steps)
        ])
        full_text = f"{self.title}\n\n재료:\n{ingredients_text}\n\n조리 단계:\n{steps_text}"
        return full_text

    def to_metadata(self) -> dict:
        return {
            "recipe_id": self.recipe_id,
            "title": self.title,
            "ingredients": self.ingredients,
            "steps": self.steps
        }