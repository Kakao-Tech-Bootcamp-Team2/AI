from fastapi import HTTPException
from app.core import setting
import requests

SPOONACULAR_URL = "https://api.spoonacular.com/recipes/findByIngredients" #SPOONACULAR URL주소

def get_spoonacular(query:str) :
    url = SPOONACULAR_URL
    params = {
        "ingredients" : query, #재료 입력
        "apiKey" : setting.SPOONACULAR_API_KEY
    }
    try :
        response = requests.get(url,params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))