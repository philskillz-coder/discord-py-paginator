from discord import ui, User, Interaction, Webhook, Embed, File
from discord.ext.commands import Bot

from . import buttons

from typing import Dict, Any, List, Union, Optional


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

        self.static_data: Optional[List[Dict[str, Union[str, Embed, List[File]]]]] = kwargs.get("static_data", None)

        if self.static_data is not None:
            self.static_data_pages = len(
                self.static_data)  # static data cannot change, so get_page_count does not have to return len every time

        else:
            self.static_data_pages = None

    @classmethod
    def from_list(
            cls,
            client: Bot,
            user: User,
            timeout: int = 180,
            quick_nav: bool = True,
            data: List[Dict[str, Union[str, Embed, List[File]]]] = None
    ):
        return cls(
            client=client,
            user=user,
            timeout=timeout,
            quick_nav=quick_nav,
            static_data=data
        )

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

    async def run(self, *args, **kwargs):
        await self.add_buttons()
        await self.setup(*args, **kwargs)

        return self

    async def start(self, interaction: Interaction):
        await self._start(interaction)
        await self.on_start(interaction)

    async def stop(self, interaction: Interaction):
        await self.on_stop(interaction)
        super().stop()

    async def _start(self):
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

    async def on_start(self, interaction: Interaction):
        pass

    async def on_stop(self, interaction: Interaction):
        pass


    async def _get_page_count(self, interaction: Interaction) -> int:
        if self.static_data_pages is not None:
            return self.static_data_pages
        
        return await self.get_page_count(interaction)
    
    async def get_page_count(self, interaction: Interaction) -> int:
        raise NotImplementedError("get_page_count must be implemented!")

    async def set_page(self, interaction: Interaction, page: int):
        count = await self._get_page_count(interaction)
        if page < 1:
            page = count

        if page > count:
            page = 1

        self.page = page

    async def _get_update_contents(self, interaction: Interaction):
        if self.static_data is None:
            contents = await self.get_page_content(interaction, self.page)
        
        else:
            contents = self.static_data[self.page-1]

        return contents

    async def get_page_content(self, interaction: Interaction, page: int) -> Dict[str, Any]:
        raise NotImplementedError("get_page_content must be implemented!")

    async def update_contents(self, interaction: Interaction):
        await interaction.response.defer()
        contents = await self._get_update_contents(interaction)
        ws: Webhook = interaction.followup

        await ws.edit_message(
            (await interaction.original_message()).id,
            **contents
        )



