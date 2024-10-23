from pydantic_settings import BaseSettings
import os

class Setting(BaseSettings) : 
    SPOONACULAR_API_KEY : str
    EDAMAM_APPLICATION_ID : str
    EDAMAM_API_KEY : str

    class Config :
        env_file = os.getenv("ENV_FILE",".env")

setting = Setting()