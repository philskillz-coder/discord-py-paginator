from discord import ui, User, Interaction
from discord.ext.commands import Bot

from . import buttons

from typing import Dict, Any

class Paginator(ui.View):
    def __init__(
        self,
        client: Bot,
        user: User,
        timeout: int = 180,
        quick_nav: bool = True,
        *args, **kwargs
    ):
        super().__init__(timeout=timeout)
        self.client = client
        self.user = user
        self.page = 1

        self.first_elem_btn = buttons.FirstElement(client, self, user, False)
        self.prev_elem_btn = buttons.PreviousElement(client, self, user, False)
        self.next_elem_btn = buttons.NextElement(client, self, user, False)
        self.last_elem_btn = buttons.LastElement(client, self, user, False)
        self.start_btn = buttons.Start(client, self, user, False)
        self.stop_btn = buttons.Stop(client, self, user, False)
        self.quick_nav_btn = buttons.QuickNav(client, self, user, not quick_nav)

        self.add_item(self.start_btn)

    async def setup(self, *args, **kwargs):
        pass

    async def start(self, *args, **kwargs):
        await self.setup(*args, **kwargs)
        return self

    async def started_pressed(self):
        self.clear_items()

        self.add_item(self.first_elem_btn)
        self.add_item(self.prev_elem_btn)
        self.add_item(self.quick_nav_btn)
        self.add_item(self.next_elem_btn)
        self.add_item(self.last_elem_btn)
        self.add_item(self.stop_btn)

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
