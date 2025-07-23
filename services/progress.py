class ProgressManager:
    def __init__(self, message):
        self.message = message
        self.msg = None
        self.last_content = None  # для хранения последнего текста

    async def update(self, percent: int, text: str):
        bar = self.render_bar(percent)
        content = f"{bar} {percent}%\n{text}"

        # Если текст не изменился, ничего не делать
        if content == self.last_content:
            return

        self.last_content = content

        if self.msg:
            await self.msg.edit_text(content)
        else:
            self.msg = await self.message.answer(content)

    def render_bar(self, percent: int) -> str:
        full = "█"
        empty = "░"
        bar_length = 20
        filled = int(bar_length * percent / 100)
        return full * filled + empty * (bar_length - filled)
