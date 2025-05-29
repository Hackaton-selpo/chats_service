import asyncio
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
            letter_id: Optional[str],
    ) -> shared_schemas.AIOutput:
        """
        :param user_prompt: user text
        :return: ai text answer
        """
        # async with httpx.AsyncClient(timeout=200) as client:
        #     ai_answer = await client.get(
        #         f"{self.ai_host}/get_llm_answer",
        #         params={
        #             "letter_id": letter_id,
        #             "prompt": user_prompt,
        #         },
        #     )
        #     ai_text = ai_answer.json()["ai_answer"]
        return shared_schemas.AIOutput(
            type="text",
            body="""
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque mollis finibus enim vel tempus. In hac habitasse platea dictumst. Ut auctor dolor vel nulla euismod fermentum. Nunc mattis laoreet neque, vitae laoreet diam egestas a. Sed ac sodales sapien. Pellentesque venenatis quis augue a tempus. Aenean lobortis enim ante, a porta lorem interdum ut. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nunc posuere est sit amet risus sodales, in fermentum sapien eleifend. Vivamus iaculis nec nunc vitae tempus. Aenean laoreet, ante eu ornare tristique, ex erat laoreet lorem, sit amet tempus metus sapien accumsan ipsum. Ut suscipit augue turpis, sit amet interdum eros mattis nec. Sed vitae lacus quis ipsum dignissim blandit. Aliquam egestas pharetra dui, id facilisis erat gravida eget. Praesent ut est velit. Integer eget diam suscipit, semper dolor quis, laoreet purus. Donec ut congue nunc. Donec ac tortor at ex finibus feugiat in id metus. Phasellus consectetur auctor elit vitae dictum. Praesent ultricies tellus et lobortis convallis. Proin tincidunt lectus vel augue cursus, eget malesuada erat venenatis. Mauris quam ligula, ullamcorper eu turpis in, condimentum bibendum urna. Nam nec aliquet dolor. Nunc vitae est quis lectus finibus volutpat.
                """,
        )

    async def generate_ai_image_answer(
            self,
            user_prompt: str,
            letter_id: Optional[str],
    ) -> shared_schemas.AIOutput:
        """

        :return: bing url to image
        """
        # async with httpx.AsyncClient(timeout=200) as client:
        #     ai_answer = await client.get(
        #         f"{self.ai_host}/get_llm_image",
        #         params={
        #             "letter_id": letter_id,
        #             "prompt": user_prompt,
        #         },
        #     )
        #     service_response = ai_answer.json()
        #     image_url = service_response["url"]
        #     image_title = service_response["title"]
        image_url = "https://i.pinimg.com/736x/74/bb/05/74bb05512ccb07a2a2076e0415b2991b.jpg"
        return shared_schemas.ImageOutput(
            type="image",
            body=image_url,
            title="random title",
        )

    async def generate_ai_audio_answer(
            self,
            user_prompt: str,
            letter_id: Optional[str],
            generate_audio_with_text: bool
    ) -> shared_schemas.AudioOutput:
        """

        :return: url to audio
        """
        # async with httpx.AsyncClient(timeout=200) as client:
        #     ai_answer = await client.get(
        #         f"{self.ai_host}/get_llm_audio",
        #         params={
        #             "letter_id": letter_id,
        #             "prompt": user_prompt,
        #             "generate_audio_with_text": generate_audio_with_text
        #         },
        #     )
        #     service_response = ai_answer.json()
        #     audio_url = service_response["url"]
        #     audio_bg_url = service_response["bg_image"]
        #     audio_title = service_response["title"]

        audio_url = "https://zaycev.fractal.zerocdn.com/37a0f8a1ee458ecbdb6ed6bd9df15c1f:2025052620/track/24854430.mp3"
        audio_bg_url = "https://i.pinimg.com/736x/74/bb/05/74bb05512ccb07a2a2076e0415b2991b.jpg"
        audio_title = "random title"
        return shared_schemas.AudioOutput(
            type="audio",
            body=audio_url,
            bg_image=audio_bg_url,
            title=audio_title,
        )
