from discord import ui, User, Interaction, Webhook, Client, ButtonStyle
from discord.ext.commands import Bot

from . import view_buttons

from typing import Dict, Any, List, Union, Optional, Callable, Coroutine

GCP_TYPE = Callable[[Interaction, int], Coroutine[Any, Any, Dict[str, Any]]]


class Paginator(ui.View):
    __CONFIG__: Dict = {  # DO NOT CHANGE THIS! You can add custom config attrs in Paginator.CONFIG
        "paginator_view_timeout": 180,
        "paginator_ephemeral": None,  # this setting overwrites ephemeral= from get_page_content. if None,
        # not overwritten
        "paginator_delete_when_finished": True,  # only works when paginator is not ephemeral
        "paginator_delete_delay": 10,

        "start_button_enabled": True,  # option not changeable!
        "start_button_style": ButtonStyle.success,
        "start_button_label": "Start",
        "start_button_emoji": None,

        "stop_button_enabled": True,  # option not changeable!
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
    CONFIG = __CONFIG__.copy()  # will count for all instances of your paginator

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
            **kwargs
    ):
        config = self.parse_config(config)
        self.config = config
        super().__init__(timeout=config["paginator_view_timeout"])

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
            using=config["first_element_button_enabled"],
            disabled=True
        )

        self.prev_elem_btn = view_buttons.PreviousElement(
            config["prev_element_button_style"],
            config["prev_element_button_label"],
            config["prev_element_button_emoji"],
            client=client,
            parent=self,
            user=user,
            using=config["prev_element_button_enabled"],
            disabled=True
        )

        self.next_elem_btn = view_buttons.NextElement(
            config["next_element_button_style"],
            config["next_element_button_label"],
            config["next_element_button_emoji"],
            client=client,
            parent=self,
            user=user,
            using=config["next_element_button_enabled"],
            disabled=True
        )

        self.last_elem_btn = view_buttons.LastElement(
            config["last_element_button_style"],
            config["last_element_button_label"],
            config["last_element_button_emoji"],
            client=client,
            parent=self,
            user=user,
            using=config["last_element_button_enabled"],
            disabled=True
        )

        self.start_btn = view_buttons.Start(
            config["start_button_style"],
            config["start_button_label"],
            config["start_button_emoji"],
            client=client,
            parent=self,
            user=user,
            using=True,
            disabled=False
        )

        self.stop_btn = view_buttons.Stop(
            config["stop_button_style"],
            config["stop_button_label"],
            config["stop_button_emoji"],
            client=self.client,
            parent=self,
            user=user,
            using=True,
            disabled=False
        )

        self.quick_nav_btn = view_buttons.QuickNav(
            config["quick_navigation_button_style"],
            config["quick_navigation_button_label"],
            config["quick_navigation_button_emoji"],
            client=self.client,
            parent=self,
            user=user,
            using=config["quick_navigation_button_enabled"],
            disabled=True
        )

        self.static_data: Optional[List[Dict[str, Any]]] = kwargs.get("static_data")
        self.static_page_count = len(self.static_data or []) or kwargs.get("static_page_count") or None

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

    async def run(self, *args, **kwargs):
        await self._add_buttons()
        await self.on_setup(*args, **kwargs)

        return self

    async def on_setup(self, *args, **kwargs):  # for users
        pass

    async def on_start(self, interaction: Interaction):  # for users
        pass

    async def on_stop(self, interaction: Interaction):  # for users
        pass

    # noinspection PyArgumentList
    async def _add_buttons(self):
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

    # noinspection PyArgumentList
    async def _child_paginator_start(self, interaction: Interaction):
        self.clear_items()

        self.first_elem_btn.disabled = not self.config["first_element_button_enabled"]

        self.prev_elem_btn.disabled = not self.config["prev_element_button_enabled"]

        self.next_elem_btn.disabled = not self.config["next_element_button_enabled"]

        self.last_elem_btn.disabled = not self.config["last_element_button_enabled"]

        self.quick_nav_btn.disabled = not self.config["quick_navigation_button_enabled"]

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

        await self.on_start(interaction)
        await self.page_update(interaction, 0)

    async def _child_paginator_stop(self, interaction: Interaction):
        if self.config["paginator_delete_when_finished"]:
            if interaction.message.flags.ephemeral:
                await interaction.message.delete(
                    delay=self.config["paginator_delete_delay"]
                )

        await self.on_stop(interaction)
        super().stop()

    async def _child_update_page_number(self, interaction: Interaction, page: int):
        if self.static_page_count is not None:
            _page_count = self.static_page_count
        else:
            _page_count = await self.get_page_count(interaction)

        self.page = (page % _page_count)

    async def _child_update_page_content(self, interaction: Interaction):
        if self.static_data is None:
            await self.page_update(interaction, self.page)

        else:
            await interaction.response.edit_message(
                **self.static_data[self.page]
            )

    async def get_page_count(self, interaction: Interaction) -> int:
        raise NotImplementedError("get_page_count must be implemented or static_page_count set!")

    async def page_update(self, interaction: Interaction, current_page: int):
        raise NotImplementedError("update_page must be implemented!")
