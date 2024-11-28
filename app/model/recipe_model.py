from pydantic import BaseModel
from typing import Dict,List
import logging

logging.basicConfig(level=logging.INFO)

class Recipe(BaseModel) :
    title : str
    recipe_id : str
    ingredients : Dict[str,List[str]]
    steps : List[str]

    def prepare_text_for_embedding(self) -> str:
        ingredients_text = '\n'.join([
            f"{category}: {', '.join(items)}"
            for category, items in self.ingredients.items()
        ])
        
        logging.info(ingredients_text)
        return ingredients_text

    def to_metadata(self) -> dict:
        # 재료 딕셔너리의 모든 값을 하나의 리스트로 결합
        ingredients_list = []
        for items in self.ingredients.values():
            ingredients_list.extend(items)
        return {
            "title": self.title,
            "ingredients": ingredients_list,  # 문자열의 리스트
            "steps": self.steps
        }