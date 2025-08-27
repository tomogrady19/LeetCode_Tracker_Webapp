import httpx
from fastapi import HTTPException
from models import LeetCodeStats

api_url = "https://leetcode-stats.tashif.codes/{username}"


async def fetch_leetcode_stats(username: str) -> LeetCodeStats:
    url = api_url.format(username=username)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10)

            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="LeetCode user not found")

            response.raise_for_status()
            stats = response.json()

            if not stats or stats.get('status') != 'success':
                raise HTTPException(status_code=400, detail="Failed to get data from LeetCode API")

            return LeetCodeStats(
                username=username,
                easy=stats.get('easySolved', 0),
                medium=stats.get('mediumSolved', 0),
                hard=stats.get('hardSolved', 0),
                total=stats.get('totalSolved', 0)
            )

        except httpx.TimeoutException:
            raise HTTPException(status_code=408, detail="LeetCode API timed out")
        except httpx.RequestError:


            raise HTTPException(status_code=503, detail="Could not connect to LeetCode API")
