def get_message_type(message_text: str) -> str:
    if message_text.endswith("mp3"):
        return "audio"
    elif (
        message_text.endswith("png")
        or message_text.endswith("jpg")
        or message_text.endswith("jpeg")
    ):
        return "image"
    else:
        return "text"
