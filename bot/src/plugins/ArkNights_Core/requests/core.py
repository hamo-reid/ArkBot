import asyncio
from typing import List

import httpx
from pydantic import BaseModel
from fake_useragent import UserAgent

ua = UserAgent()

class GetRequest(BaseModel):
    url: str
    params: dict = None
    headers: dict = None

async def async_get(req_list: List[GetRequest]) -> List[httpx.Response]:
    req_tasks = []
    async with httpx.AsyncClient(timeout=None, verify=False) as client:
        for req in req_list:
            req_tasks.append(
                asyncio.create_task(
                    client.get(
                        req.url,
                        params=req.params,
                        headers=req.headers,

                    )
                )
            )
        results = await asyncio.gather(*req_tasks)
    return results
