from discord import ui, User, Interaction, Webhook, Client, ButtonStyle
from discord.ext.commands import Bot

from . import view_buttons

from typing import Dict, Any, List, Union, Optional, Callable, Coroutine

GCP_TYPE = Callable[[Interaction, int], Coroutine[Any, Any, Dict[str, Any]]]


class ClassConfig:
    paginator_view_timeout: int = 180
    paginator_delete_when_finished: bool = True  # only works when paginator is not ephemeral
    paginator_delete_delay = 10

    start_button_style: ButtonStyle = ButtonStyle.success
    start_button_label: str = "Start"
    start_button_emoji: str = None

    stop_button_style: ButtonStyle = ButtonStyle.danger
    stop_button_label: str = "Quit"
    stop_button_emoji: str = None

    quick_navigation_button_enabled: bool = True
    quick_navigation_button_style: ButtonStyle = ButtonStyle.blurple
    quick_navigation_button_label: str = "Nav"
    quick_navigation_button_emoji: str = None
    quick_navigation_error_message: str = "%s is not a number!"  # None means no message

    first_element_button_enabled: bool = True
    first_element_button_style: ButtonStyle = ButtonStyle.secondary
    first_element_button_label: str = "\U000025c0 \U000025c0"  # None means no label
    first_element_button_emoji: str = None

    prev_element_button_enabled: bool = True
    prev_element_button_style: ButtonStyle = ButtonStyle.secondary
    prev_element_button_label: str = "\U000025c0"
    prev_element_button_emoji: str = None

    next_element_button_enabled: bool = True
    next_element_button_style: ButtonStyle = ButtonStyle.secondary
    next_element_button_label: str = "\U000025b6"
    next_element_button_emoji: str = None

    last_element_button_enabled: bool = True
    last_element_button_style: ButtonStyle = ButtonStyle.secondary
    last_element_button_label: str = "\U000025b6 \U000025b6"
    last_element_button_emoji: str = None

    placeholder_button_enabled: bool = True
    placeholder_button_style: ButtonStyle = ButtonStyle.secondary
    placeholder_button_label: str = "\U0001f6ab"
    placeholder_button_emoji: str = None


class Unset:
    pass


class InstanceConfig:
    paginator_view_timeout: int = Unset
    paginator_delete_when_finished: bool = Unset  # only works when paginator is not ephemeral
    paginator_delete_delay = Unset

    start_button_style: ButtonStyle = Unset
    start_button_label: str = Unset
    start_button_emoji: str = Unset

    stop_button_style: ButtonStyle = Unset
    stop_button_label: str = Unset
    stop_button_emoji: str = Unset

    quick_navigation_button_enabled: bool = Unset
    quick_navigation_button_style: ButtonStyle = Unset
    quick_navigation_button_label: str = Unset
    quick_navigation_button_emoji: str = Unset
    quick_navigation_error_message: str = Unset  # None means no message

    first_element_button_enabled: bool = Unset
    first_element_button_style: ButtonStyle = Unset
    first_element_button_label: str = Unset  # None means no label
    first_element_button_emoji: str = Unset

    prev_element_button_enabled: bool = Unset
    prev_element_button_style: ButtonStyle = Unset
    prev_element_button_label: str = Unset
    prev_element_button_emoji: str = Unset

    next_element_button_enabled: bool = Unset
    next_element_button_style: ButtonStyle = Unset
    next_element_button_label: str = Unset
    next_element_button_emoji: str = Unset

    last_element_button_enabled: bool = Unset
    last_element_button_style: ButtonStyle = Unset
    last_element_button_label: str = Unset
    last_element_button_emoji: str = Unset

    placeholder_button_enabled: bool = Unset
    placeholder_button_style: ButtonStyle = Unset
    placeholder_button_label: str = Unset
    placeholder_button_emoji: str = Unset


class Paginator(ui.View):
    CLASS_CONFIG = ClassConfig()

    @staticmethod
    def merge_config(instance_config: InstanceConfig) -> ClassConfig:
        if instance_config is None:
            return ClassConfig()

        for key, value in Paginator.CLASS_CONFIG.__class__.__dict__.items():
            if key.startswith("__"):
                continue

            if getattr(instance_config, key) is Unset:
                setattr(instance_config, key, value)

        return instance_config

    def __init__(
            self,
            client: Union[Bot, Client],
            user: User,
            config: Optional[InstanceConfig] = None,
    ):
        self.config = self.merge_config(config)
        super().__init__(timeout=config.paginator_view_timeout)

        self.client = client
        self.user = user
        self.page = 0

        self.first_elem_btn = view_buttons.FirstElement(
            config.first_element_button_style,
            config.first_element_button_label,
            config.first_element_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=config.first_element_button_enabled,
            disabled=True
        )

        self.prev_elem_btn = view_buttons.PreviousElement(
            config.prev_element_button_style,
            config.prev_element_button_label,
            config.prev_element_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=config.prev_element_button_enabled,
            disabled=True
        )

        self.next_elem_btn = view_buttons.NextElement(
            config.next_element_button_style,
            config.next_element_button_label,
            config.next_element_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=config.next_element_button_enabled,
            disabled=True
        )

        self.last_elem_btn = view_buttons.LastElement(
            config.last_element_button_style,
            config.last_element_button_label,
            config.last_element_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=config.last_element_button_enabled,
            disabled=True
        )

        self.start_btn = view_buttons.Start(
            config.start_button_style,
            config.start_button_label,
            config.start_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=True,
            disabled=False
        )

        self.stop_btn = view_buttons.Stop(
            config.stop_button_style,
            config.stop_button_label,
            config.stop_button_emoji,
            client=self.client,
            parent=self,
            user=user,
            using=True,
            disabled=False
        )

        self.quick_nav_btn = view_buttons.QuickNav(
            config.quick_navigation_button_style,
            config.quick_navigation_button_label,
            config.quick_navigation_button_emoji,
            client=self.client,
            parent=self,
            user=user,
            using=config.quick_navigation_button_enabled,
            disabled=True
        )

    async def run(self, *args, **kwargs):
        await self.add_buttons()
        await self.on_setup(*args, **kwargs)

        return self

    async def on_setup(self, *args, **kwargs):  # for users
        pass

    async def on_start(self, interaction: Interaction):  # for users
        pass

    async def on_stop(self, interaction: Interaction):  # for users
        pass

    # noinspection PyArgumentList
    async def add_buttons(self):
        placeholder_config = (
            self.config.placeholder_button_style,
            self.config.placeholder_button_label,
            self.config.placeholder_button_emoji
        )

        # first element, previous element
        if self.config.first_element_button_enabled:
            self.add_item(self.first_elem_btn)
        if self.config.prev_element_button_enabled:
            self.add_item(self.prev_elem_btn)

        self.add_item(self.start_btn)

        # next element, last element
        if self.config.next_element_button_enabled:
            self.add_item(self.next_elem_btn)
        if self.config.last_element_button_enabled:
            self.add_item(self.last_elem_btn)

        # placeholders
        if self.config.placeholder_button_enabled:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))

        self.add_item(self.stop_btn)

        # placeholders
        if self.config.placeholder_button_enabled:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))

    # noinspection PyArgumentList
    async def child_paginator_start(self, interaction: Interaction):
        self.clear_items()

        self.first_elem_btn.disabled = False
        self.prev_elem_btn.disabled = False
        self.next_elem_btn.disabled = False
        self.last_elem_btn.disabled = False
        self.quick_nav_btn.disabled = False

        placeholder_config = (
            self.config.placeholder_button_style,
            self.config.placeholder_button_label,
            self.config.placeholder_button_emoji
        )

        # first element, previous element
        if self.config.first_element_button_enabled:
            self.add_item(self.first_elem_btn)
        if self.config.prev_element_button_enabled:
            self.add_item(self.prev_elem_btn)

        # quick nav
        if self.config.quick_navigation_button_enabled:
            self.add_item(self.quick_nav_btn)

        # next element, last element
        if self.config.next_element_button_enabled:
            self.add_item(self.next_elem_btn)
        if self.config.last_element_button_enabled:
            self.add_item(self.last_elem_btn)

        # placeholders
        if self.config.placeholder_button_enabled:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))

        self.add_item(self.stop_btn)

        # placeholders
        if self.config.placeholder_button_enabled:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))

        await self.on_start(interaction)

    async def child_paginator_stop(self, interaction: Interaction):
        if (
                self.config.paginator_delete_when_finished
                and not interaction.message.flags.ephemeral
        ):
            await interaction.message.delete(
                delay=self.config.paginator_delete_delay
            )

        await self.on_stop(interaction)
        super().stop()

    async def child_update_page_number(self, interaction: Interaction, page: int):
        _page_count = await self.get_page_count(interaction)
        self.page = (page % _page_count)

    async def child_update_page_content(self, interaction: Interaction):
        await self.page_update(interaction, self.page)

    async def get_page_count(self, interaction: Interaction) -> int:
        raise NotImplementedError("get_page_count must be implemented or static_page_count set!")

    async def page_update(self, interaction: Interaction, current_page: int):
        raise NotImplementedError("update_page must be implemented!")
