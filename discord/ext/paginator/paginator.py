from discord import ui, User, Interaction, Webhook, Embed, File, Client
from discord.ext.commands import Bot


from . import view_buttons

from typing import Dict, Any, List, Union, Optional, Callable, Coroutine

GCP_TYPE = Callable[[Interaction, int], Coroutine[Any, Any, Dict[str, Any]]]


class Paginator(ui.View):
    __CONFIG__: Dict = {                # DO NOT CHANGE THIS! You can add custom config attrs in Paginator.CONFIG
        "view_timeout": 180,            # paginator view timeout

        "use_quick_nav": True,          # paginator quick nav enabled?
        "use_first_elem_button": True,
        "use_prev_elem_button": True,
        "use_next_elem_button": True,
        "use_last_elem_button": True,
        "use_placeholders": True
    }
    CONFIG = __CONFIG__.copy()          # will count for all instances of your paginator

    @staticmethod
    def parse_config(config: Dict) -> Dict:
        if config is None:
            return Paginator.CONFIG

        _config = Paginator.CONFIG.copy()
        _config.update(config)
        return _config

    def gcv(self, config_key: str, config_default_value: Optional[Any] = None, /):
        return self.config.get(config_key, config_default_value)


    def __init__(
            self,
            client: Union[Bot, Client],
            user: User,
            config: Optional[Dict] = None,
            *args, **kwargs
    ):
        super().__init__(timeout=self.gcv("view_timeout", 180))
        self.config = self.parse_config(config)

        self.client = client
        self.user = user
        self.page = 0

        self.first_elem_btn = view_buttons.FirstElement(client, self, user, self.gcv("use_first_elem_button", True))
        self.prev_elem_btn = view_buttons.PreviousElement(client, self, user, self.gcv("use_prev_elem_button", True))
        self.next_elem_btn = view_buttons.NextElement(client, self, user, self.gcv("use_next_elem_button", True))
        self.last_elem_btn = view_buttons.LastElement(client, self, user, self.gcv("use_last_elem_button", True))

        self.start_btn = view_buttons.Start(client, self, user, True)
        self.stop_btn = view_buttons.Stop(client, self, user, True)

        self.quick_nav_btn = view_buttons.QuickNav(client, self, user, not self.gcv("use_quick_nav", True))

        self.static_data: Optional[List[Dict[str, Any]]] = kwargs.get("static_data")
        self.static_data_pages = len(self.static_data or []) or None

    @classmethod
    def from_list(
            cls,
            client: Union[Bot, Client],
            user: User,
            config: Optional[Dict] = None,
            data: List[Dict[str, Any]] = None
    ):
        return cls(
            client=client,
            user=user,
            config=config,
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
        if self.gcv("use_placeholders", True):
            self.add_item(view_buttons.Placeholder())
            self.add_item(view_buttons.Placeholder())
        self.add_item(self.stop_btn)
        if self.gcv("use_placeholders", True):
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

        if self.gcv("use_first_elem_button", True):
            self.first_elem_btn.disabled = False

        if self.gcv("use_next_elem_button", True):
            self.next_elem_btn.disabled = False

        if self.gcv("use_prev_elem_button", True):
            self.prev_elem_btn.disabled = False

        if self.gcv("use_last_elem_button", True):
            self.last_elem_btn.disabled = False

        self.start_btn.disabled = True

        if self.gcv("use_quick_nav", True):
            self.quick_nav_btn.disabled = False

        self.add_item(self.first_elem_btn)
        self.add_item(self.prev_elem_btn)
        self.add_item(self.quick_nav_btn)
        self.add_item(self.next_elem_btn)
        self.add_item(self.last_elem_btn)
        if self.gcv("use_placeholders", True):
            self.add_item(view_buttons.Placeholder())
            self.add_item(view_buttons.Placeholder())
        self.add_item(self.stop_btn)
        if self.gcv("use_placeholders", True):
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
        count = await self.acquire_page_count(interaction)

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
