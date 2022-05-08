from discord import ui, User, Interaction, Webhook, Client, ButtonStyle
from discord.ext.commands import Bot


from . import view_buttons

from typing import Dict, Any, List, Union, Optional, Callable, Coroutine

GCP_TYPE = Callable[[Interaction, int], Coroutine[Any, Any, Dict[str, Any]]]


class Paginator(ui.View):
    __CONFIG__: Dict = {                # DO NOT CHANGE THIS! You can add custom config attrs in Paginator.CONFIG
        "paginator_view_timeout": 180,
        "paginator_ephemeral": True,    # this setting overwrites ephemeral= from get_page_content. if None, not overwritten
        "paginator_delete_when_finished": True,  # only works when paginator is not ephemeral
        "paginator_delete_delay": 10,

        "start_button_enabled": True,  # option not changable!
        "start_button_style": ButtonStyle.success,
        "start_button_label": "Start",
        "start_button_emoji": None,

        "stop_button_enabled": True,  # option not changable!
        "stop_button_style": ButtonStyle.danger,
        "stop_button_label": "Quit",
        "stop_button_emoji": None,

        "quick_navigation_button_enabled": True,
        "quick_navigation_button_style": ButtonStyle.blurple,
        "quick_navigation_button_label": "Nav",
        "quick_navigation_button_emoji": None,
        "quick_navigation_error_message": "%s is not a number!",  # False means no message
        "quick_navigation_error_ephemeral": True,

        "first_element_button_enabled": True,
        "first_element_button_style": ButtonStyle.secondary,
        "first_element_button_label": "\U000025c0 \U000025c0",  # None means no label
        "first_element_button_emoji": None,

        "prev_element_button_enabled": True,
        "prev_element_button_style": ButtonStyle.secondary,
        "prev_element_button_label": "\U000025c0",
        "prev_element_button_emoji": None,

        "next_element_button_enabled": True,
        "next_element_button_style": ButtonStyle.secondary,
        "next_element_button_label": "\U000025b6",
        "next_element_button_emoji": None,

        "last_element_button_enabled": True,
        "last_element_button_style": ButtonStyle.secondary,
        "last_element_button_label": "\U000025b6 \U000025b6",
        "last_element_button_emoji": None,

        "placeholder_button_enabled": True,
        "placeholder_button_style": ButtonStyle.secondary,
        "placeholder_button_label": "\U0001f6ab",
        "placeholder_button_emoji": None,
    }
    CONFIG = __CONFIG__.copy()          # will count for all instances of your paginator

    @staticmethod
    def parse_config(config: Dict) -> Dict:
        if config is None:
            return Paginator.CONFIG

        _config = Paginator.CONFIG.copy()
        _config.update(config)
        return _config

    def __init__(
            self,
            client: Union[Bot, Client],
            user: User,
            config: Optional[Dict] = None,
            *args, **kwargs
    ):
        config = self.parse_config(config)
        self.config = config
        super().__init__(timeout=config["view_timeout"])

        self.client = client
        self.user = user
        self.page = 0

        self.first_elem_btn = view_buttons.FirstElement(
            config["first_element_button_style"],
            config["first_element_button_label"],
            config["first_element_button_emoji"],
            client=client,
            parent=self,
            user=user,
            using=config["first_element_button_enabled"]
        )

        self.prev_elem_btn = view_buttons.PreviousElement(
            config["prev_element_button_style"],
            config["prev_element_button_label"],
            config["prev_element_button_emoji"],
            client=client,
            parent=self,
            user=user,
            using=config["prev_element_button_enabled"]
        )

        self.next_elem_btn = view_buttons.NextElement(
            config["next_element_button_style"],
            config["next_element_button_label"],
            config["next_element_button_emoji"],
            client=client,
            parent=self,
            user=user,
            using=config["next_element_button_enabled"]
        )

        self.last_elem_btn = view_buttons.LastElement(
            config["last_element_button_style"],
            config["last_element_button_label"],
            config["last_element_button_emoji"],
            client=client,
            parent=self,
            user=user,
            using=config["last_element_button_enabled"]
        )

        self.start_btn = view_buttons.Start(
            config["start_button_style"],
            config["start_button_label"],
            config["start_button_emoji"],
            client=client,
            parent=self,
            user=user,
            using=True
        )

        self.stop_btn = view_buttons.Stop(
            config["stop_button_style"],
            config["stop_button_label"],
            config["stop_button_emoji"],
            client=self.client,
            parent=self,
            user=user,
            using=True
        )

        self.quick_nav_btn = view_buttons.QuickNav(
            config["quick_navigation_button_style"],
            config["quick_navigation_button_label"],
            config["quick_navigation_button_emoji"],
            client=self.client,
            parent=self,
            user=user,
            using=config["quick_navigation_button_enabled"]
        )

        self.static_data: Optional[List[Dict[str, Any]]] = kwargs.get("static_data")
        self.static_data_page_count = len(self.static_data or []) or kwargs.get("static_page_count") or None


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

    # noinspection PyArgumentList
    async def add_buttons(self):
        placeholder_config = (
            self.config["placeholder_button_style"],
            self.config["placeholder_button_label"],
            self.config["placeholder_button_emoji"]
        )

        self.add_item(self.first_elem_btn)
        self.add_item(self.prev_elem_btn)
        self.add_item(self.start_btn)
        self.add_item(self.next_elem_btn)
        self.add_item(self.last_elem_btn)
        if self.config["placeholder_button_enabled"]:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))
        self.add_item(self.stop_btn)
        if self.config["placeholder_button_enabled"]:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))

    async def run(self, *args, **kwargs):
        await self.add_buttons()
        await self.setup(*args, **kwargs)

        return self

    async def paginator_start(self, interaction: Interaction):
        await self._paginator_start()
        await self.on_start(interaction)

    # noinspection PyArgumentList
    async def _paginator_start(self):
        self.clear_items()

        if self.config["first_element_button_enabled"]:
            self.first_elem_btn.disabled = False

        if self.config["prev_element_button_enabled"]:
            self.prev_elem_btn.disabled = False

        if self.config["next_element_button_enabled"]:
            self.next_elem_btn.disabled = False


        if self.config["last_element_button_enabled"]:
            self.last_elem_btn.disabled = False

        self.quick_nav_btn.disabled = self.config["quick_navigation_button_enabled"]

        placeholder_config = (
            self.config["placeholder_button_style"],
            self.config["placeholder_button_label"],
            self.config["placeholder_button_emoji"]
        )

        self.add_item(self.first_elem_btn)
        self.add_item(self.prev_elem_btn)
        self.add_item(self.quick_nav_btn)
        self.add_item(self.next_elem_btn)
        self.add_item(self.last_elem_btn)
        if self.config["placeholder_button_enabled"]:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))
        self.add_item(self.stop_btn)
        if self.config["placeholder_button_enabled"]:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))

    async def paginator_stop(self, interaction: Interaction):
        if self.config["paginator_delete_when_finished"]:
            if interaction.message.flags.ephemeral:
                await interaction.message.delete(
                    delay=self.config["paginator_delete_delay"]
                )

        await self.on_stop(interaction)
        super().stop()

    async def on_start(self, interaction: Interaction):
        pass

    async def on_stop(self, interaction: Interaction):
        pass

    async def acquire_page_count(self, interaction: Interaction) -> int:
        if self.static_data_page_count is None:
            return await self.get_page_count(interaction)

        return self.static_data_page_count

    async def get_page_count(self, interaction: Interaction) -> int:
        raise NotImplementedError("get_page_count must be implemented!")

    async def update_page_number(self, interaction: Interaction, page: int):
        count = await self.acquire_page_count(interaction)

        self.page = (page % count)

    async def update_page_content(self, interaction: Interaction):
        await interaction.response.defer()
        contents = await self.acquire_page_content(interaction)

        ephemeral = self.config["paginator_ephemeral"]
        if ephemeral is not None:
            contents["ephemeral"] = ephemeral

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
