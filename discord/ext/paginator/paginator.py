from discord import ui, User
from discord.ext.commands import Bot

from . import buttons

from typing import Dict, Any

class Paginator(ui.View):
    def __init__(
            self,
            client: Bot,
            user: User,
            timeout: int = 180
    ):
        super().__init__(timeout=timeout)
        self.client = client
        self.user = user
        self.page = 1

        self.first_elem_btn = buttons.FirstElement(client, self, user)
        self.prev_elem_btn = buttons.PreviousElement(client, self, user)
        self.next_elem_btn = buttons.NextElement(client, self, user)
        self.last_elem_btn = buttons.LastElement(client, self, user)
        self.start_btn = buttons.Start(client, self, user, False)
        self.stop_btn = buttons.Stop(client, self, user, False)

        self.add_item(self.first_elem_btn)
        self.add_item(self.prev_elem_btn)
        self.add_item(self.start_btn)
        self.add_item(self.next_elem_btn)
        self.add_item(self.last_elem_btn)

        for item in self.children:
            item.parent = self

    async def start(self):
        self.clear_items()

        self.first_elem_btn.disabled = False
        self.prev_elem_btn.disabled = False
        self.next_elem_btn.disabled = False
        self.last_elem_btn.disabled = False

        self.add_item(self.first_elem_btn)
        self.add_item(self.prev_elem_btn)
        self.add_item(self.stop_btn)
        self.add_item(self.next_elem_btn)
        self.add_item(self.last_elem_btn)

    async def get_page_count(self) -> int:
        return 1

    async def set_page(self, page: int):
        count = await self.get_page_count()
        if page < 1:
            page = count

        if page > count:
            page = 1

        self.page = page

    async def get_page_content(self) -> Dict[str, Any]:
        return await self.get_content(self.page)

    async def get_content(self, page: int) -> Dict[str, Any]:
        return {"content": f"**Page {page}/{await self.get_page_content()}**"}
