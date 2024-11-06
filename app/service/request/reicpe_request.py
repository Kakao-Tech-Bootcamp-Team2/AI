from fastapi import HTTPException
from app.core import setting
import requests
import aiohttp,ssl

async def get_recipe_api(start: int,end: int):
    url = f'http://openapi.foodsafetykorea.go.kr/api/{setting.RECIPE_DB_API_KEY}/COOKRCP01/XML/{start}/{end}'

    # SSL 컨텍스트 설정 / 비동기방식으로 인한 SSL 인증서 오류 발생 해결을 위한 임시 코드
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session :
            async with session.get(url) as response :
                if response.status != 200 :
                    raise {"error" : "API를 불러오지 못했습니다."}
                content = await response.text()
                return content
    except aiohttp.ClientError as e:
        return {"error":"API요청 중 오류가 발생했습니다 : {e}"}