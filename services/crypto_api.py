import aiohttp
import logging
import asyncio

async def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    
    try:
        # Оставляем ssl=False, так как это решило твою проблему
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logging.error(f"API Error status: {response.status}")
                    return None

                data = await response.json()
                return data['bitcoin']['usd']

    except Exception as e:
        logging.error(f"API Exception: {e}")
        return None