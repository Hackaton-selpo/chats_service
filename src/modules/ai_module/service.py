from typing import Optional

import httpx

from src.shared import schemas as shared_schemas


class AIService:
    ai_host = "http://localhost:8052"

    def __new__(cls, *args, **kwargs):
        """singleton pattern"""
        if not hasattr(cls, "__instance"):
            cls.__instance = super().__new__(cls)
        return cls.__instance

    async def generate_ai_text_answer(
        self,
        user_prompt: str,
        letter_id: Optional[int],
    ) -> shared_schemas.AIOutput:
        """
        :param user_prompt: user text
        :return: ai text answer
        """
        async with httpx.AsyncClient(timeout=200) as client:
            ai_answer = await client.get(
                f"{self.ai_host}/get_llm_answer",
                params={
                    "letter_id": letter_id,
                    "prompt": user_prompt,
                },
            )
            ai_text = ai_answer.json()["ai_answer"]
            return shared_schemas.AIOutput(
                type="text",
                body=ai_text,
            )

    async def generate_ai_image_answer(
        self,
        user_prompt: str,
        letter_id: Optional[int],
    ) -> shared_schemas.AIOutput:
        """

        :return: bing url to image
        """
        return shared_schemas.AIOutput(
            type="image",
            body="https://i.pinimg.com/736x/74/bb/05/74bb05512ccb07a2a2076e0415b2991b.jpg",
        )

    async def generate_ai_audio_answer(
        self,
        user_prompt: str,
        letter_id: Optional[int],
    ) -> shared_schemas.AIOutput:
        """

        :return: url to audio
        """
        return shared_schemas.AIOutput(
            type="audio",
            body="https://zaycev.fractal.zerocdn.com/37a0f8a1ee458ecbdb6ed6bd9df15c1f:2025052620/track/24854430.mp3",
        )
