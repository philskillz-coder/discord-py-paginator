from discord import ui, User, Interaction
from discord.ext.commands import Bot

from . import buttons, modals

from typing import Dict, Any

def asyncinit(cls):
    __new__ = cls.__new__

    async def init(obj, *arg, **kwarg):
        await obj.__init__(*arg, **kwarg)
        return obj

    def new(cls, *arg, **kwarg):
        obj = __new__(cls, *arg, **kwarg)
        coro = init(obj, *arg, **kwarg)
        #coro.__init__ = lambda *_1, **_2: None
        return coro

    cls.__new__ = new
    return cls

@asyncinit
class Paginator(ui.View):
    async def __init__(
        self,
        client: Bot,
        user: User,
        interaction: Interaction,
        timeout: int = 180,
        quick_nav: bool = True,
        *args, **kwargs
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

        self.quick_nav = modals.QuickNav(self, user)

        self.add_item(self.start_btn)

        await self.setup(*args, **kwargs)
        await self.wait()
        await interaction.delete_original_message()

    async def setup(self, *args, **kwargs):
        pass

    async def started_pressed(self):
        self.clear_items()

        self.first_elem_btn.disabled = False
        self.prev_elem_btn.disabled = False
        self.next_elem_btn.disabled = False
        self.last_elem_btn.disabled = False

        self.add_item(self.first_elem_btn)
        self.add_item(self.prev_elem_btn)
        self.add_item(self.quick_nav)
        self.add_item(self.next_elem_btn)
        self.add_item(self.last_elem_btn)

        if self.quick_nav:
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
