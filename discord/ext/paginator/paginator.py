from discord import ui, User, Interaction, Webhook
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

        self.first_elem_btn = buttons.FirstElement(client, self, user, True)
        self.prev_elem_btn = buttons.PreviousElement(client, self, user, True)
        self.next_elem_btn = buttons.NextElement(client, self, user, True)
        self.last_elem_btn = buttons.LastElement(client, self, user, True)

        self.start_btn = buttons.Start(client, self, user, True)
        self.stop_btn = buttons.Stop(client, self, user, True)

        self.quick_nav_btn = buttons.QuickNav(client, self, user, not quick_nav)
        self.placeholder_btn = buttons.Placeholder

    async def setup(self, *args, **kwargs):
        pass

    async def add_buttons(self):
        self.start_btn.disabled = False
        self.stop_btn.disabled = False

        self.add_item(self.first_elem_btn)
        self.add_item(self.prev_elem_btn)
        self.add_item(self.start_btn)
        self.add_item(self.next_elem_btn)
        self.add_item(self.last_elem_btn)
        self.add_item(self.placeholder_btn())
        self.add_item(self.placeholder_btn())
        self.add_item(self.stop_btn)
        self.add_item(self.placeholder_btn())
        self.add_item(self.placeholder_btn())

    async def start(self, *args, **kwargs):
        await self.add_buttons()
        await self.setup(*args, **kwargs)

        return self

    async def started_pressed(self):
        self.clear_items()

        self.first_elem_btn.disabled = False
        self.next_elem_btn.disabled = False
        self.prev_elem_btn.disabled = False
        self.last_elem_btn.disabled = False
        self.first_elem_btn.disabled = False
        self.first_elem_btn.disabled = False

        self.start_btn.disabled = True
        self.quick_nav_btn.disabled = False

        self.add_item(self.first_elem_btn)
        self.add_item(self.prev_elem_btn)
        self.add_item(self.quick_nav_btn)
        self.add_item(self.next_elem_btn)
        self.add_item(self.last_elem_btn)
        self.add_item(self.placeholder_btn())
        self.add_item(self.placeholder_btn())
        self.add_item(self.stop_btn)
        self.add_item(self.placeholder_btn())
        self.add_item(self.placeholder_btn())

    async def get_page_count(self) -> int:
        return 1

    async def set_page(self, page: int):
        count = await self.get_page_count()
        if page < 1:
            page = count

        if page > count:
            page = 1

        self.page = page

    async def update_contents(self, interaction: Interaction):
        await interaction.response.defer()
        contents = await self.get_page_content(interaction, self.page)
        ws: Webhook = interaction.followup

        await ws.edit_message(
            (await interaction.original_message()).id,
            **await self.get_page_content(interaction, self.page)
        )

    async def get_page_content(self, interaction: Interaction, page: int) -> Dict[str, Any]:
        return {"content": f"**Page {page}/{await self.get_page_content()}**"}



