
import asyncio
from googletrans import Translator



async def translate_text(text:str):
    async with Translator() as translator:
        result = await translator.translate(text, dest='en')
        return result.text  # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>

