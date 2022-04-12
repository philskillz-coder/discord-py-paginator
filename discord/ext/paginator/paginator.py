from discord import ui, User, Interaction, Webhook, Embed, File, Client
from discord.ext.commands import Bot


from . import view_buttons

from typing import Dict, Any, List, Union, Optional, Callable, Coroutine

GCP_TYPE = Callable[[Interaction, int], Coroutine[Any, Any, Dict[str, Any]]]


class Paginator(ui.View):
    def __init__(
            self,
            client: Union[Bot, Client],
            user: User,
            timeout: int = 180,
            quick_nav: bool = True,
            *args, **kwargs
    ):
        super().__init__(timeout=timeout)
        self.client = client
        self.user = user
        self.page = 0

        self.first_elem_btn = view_buttons.FirstElement(client, self, user)
        self.prev_elem_btn = view_buttons.PreviousElement(client, self, user)
        self.next_elem_btn = view_buttons.NextElement(client, self, user)
        self.last_elem_btn = view_buttons.LastElement(client, self, user)

        self.start_btn = view_buttons.Start(client, self, user)
        self.stop_btn = view_buttons.Stop(client, self, user)

        self.quick_nav_btn = view_buttons.QuickNav(client, self, user, not quick_nav)

        self.static_data: Optional[List[Dict[str, Union[str, Embed, List[File]]]]] = kwargs.get("static_data", None)

        if self.static_data is not None:
            self.static_data_pages = len(
                self.static_data
            )  # static data cannot change, so get_page_count does not have to return len every time

        else:
            self.static_data_pages = None

    @classmethod
    def from_list(
            cls,
            client: Union[Bot, Client],
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
        self.add_item(view_buttons.Placeholder())
        self.add_item(view_buttons.Placeholder())
        self.add_item(self.stop_btn)
        self.add_item(view_buttons.Placeholder())
        self.add_item(view_buttons.Placeholder())

    async def run(self, *args, **kwargs):
        await self.add_buttons()
        await self.setup(*args, **kwargs)

        return self

    async def paginator_start(self, interaction: Interaction):
        await self._paginator_start()
        await self.on_start(interaction)

    async def _paginator_start(self):
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
        self.add_item(view_buttons.Placeholder())
        self.add_item(view_buttons.Placeholder())
        self.add_item(self.stop_btn)
        self.add_item(view_buttons.Placeholder())
        self.add_item(view_buttons.Placeholder())

    async def paginator_stop(self, interaction: Interaction):
        await self.on_stop(interaction)
        super().stop()

    async def on_start(self, interaction: Interaction):
        pass

    async def on_stop(self, interaction: Interaction):
        pass

    async def acquire_page_count(self, interaction: Interaction) -> int:
        if self.static_data_pages is None:
            return await self.get_page_count(interaction)

        return self.static_data_pages

    async def get_page_count(self, interaction: Interaction) -> int:
        raise NotImplementedError("get_page_count must be implemented!")

    async def update_page_number(self, interaction: Interaction, page: int):
        count = await self.acquire_page_count(interaction) + 1

        self.page = (page % count)

    async def update_page_content(self, interaction: Interaction):
        await interaction.response.defer()
        contents = await self.acquire_page_content(interaction)

        # noinspection PyTypeChecker
        ws: Webhook = interaction.followup

        await ws.edit_message(
            (await interaction.original_message()).id,
            **contents
        )

    async def acquire_page_content(self, interaction: Interaction):
        if self.static_data is None:
            return await self.get_page_content(interaction, self.page)

        return self.static_data[self.page]

    async def get_page_content(self, interaction: Interaction, page: int) -> Dict[str, Any]:
        raise NotImplementedError("get_page_content must be implemented!")
