from typing import Dict, Any, Union, Callable, Coroutine

from discord import ui, User, Interaction, Client, ButtonStyle
from discord.ext.commands import Bot

from . import view_buttons

GCP_TYPE = Callable[[Interaction, int], Coroutine[Any, Any, Dict[str, Any]]]


class Paginator(ui.View):
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

    def __init__(
            self,
            client: Union[Bot, Client],
            user: User
    ):
        super().__init__(timeout=self.paginator_view_timeout)

        self.client = client
        self.user = user
        self.page = 0

        self.first_elem_btn = view_buttons.FirstElement(
            self.first_element_button_style,
            self.first_element_button_label,
            self.first_element_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=self.first_element_button_enabled,
            disabled=True
        )

        self.prev_elem_btn = view_buttons.PreviousElement(
            self.prev_element_button_style,
            self.prev_element_button_label,
            self.prev_element_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=self.prev_element_button_enabled,
            disabled=True
        )

        self.next_elem_btn = view_buttons.NextElement(
            self.next_element_button_style,
            self.next_element_button_label,
            self.next_element_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=self.next_element_button_enabled,
            disabled=True
        )

        self.last_elem_btn = view_buttons.LastElement(
            self.last_element_button_style,
            self.last_element_button_label,
            self.last_element_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=self.last_element_button_enabled,
            disabled=True
        )

        self.start_btn = view_buttons.Start(
            self.start_button_style,
            self.start_button_label,
            self.start_button_emoji,
            client=client,
            parent=self,
            user=user,
            using=True,
            disabled=False
        )

        self.stop_btn = view_buttons.Stop(
            self.stop_button_style,
            self.stop_button_label,
            self.stop_button_emoji,
            client=self.client,
            parent=self,
            user=user,
            using=True,
            disabled=False
        )

        self.quick_nav_btn = view_buttons.QuickNav(
            self.quick_navigation_button_style,
            self.quick_navigation_button_label,
            self.quick_navigation_button_emoji,
            client=self.client,
            parent=self,
            user=user,
            using=self.quick_navigation_button_enabled,
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
            self.placeholder_button_style,
            self.placeholder_button_label,
            self.placeholder_button_emoji
        )

        # first element, previous element
        if self.first_element_button_enabled:
            self.add_item(self.first_elem_btn)
        if self.prev_element_button_enabled:
            self.add_item(self.prev_elem_btn)

        self.add_item(self.start_btn)

        # next element, last element
        if self.next_element_button_enabled:
            self.add_item(self.next_elem_btn)
        if self.last_element_button_enabled:
            self.add_item(self.last_elem_btn)

        # placeholders
        if self.placeholder_button_enabled:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))

        self.add_item(self.stop_btn)

        # placeholders
        if self.placeholder_button_enabled:
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
            self.placeholder_button_style,
            self.placeholder_button_label,
            self.placeholder_button_emoji
        )

        # first element, previous element
        if self.first_element_button_enabled:
            self.add_item(self.first_elem_btn)
        if self.prev_element_button_enabled:
            self.add_item(self.prev_elem_btn)

        # quick nav
        if self.quick_navigation_button_enabled:
            self.add_item(self.quick_nav_btn)

        # next element, last element
        if self.next_element_button_enabled:
            self.add_item(self.next_elem_btn)
        if self.last_element_button_enabled:
            self.add_item(self.last_elem_btn)

        # placeholders
        if self.placeholder_button_enabled:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))

        self.add_item(self.stop_btn)

        # placeholders
        if self.placeholder_button_enabled:
            self.add_item(view_buttons.Placeholder(*placeholder_config))
            self.add_item(view_buttons.Placeholder(*placeholder_config))

        await self.on_start(interaction)

    async def child_paginator_stop(self, interaction: Interaction):
        if (
                self.paginator_delete_when_finished
                and not interaction.message.flags.ephemeral
        ):
            await interaction.message.delete(
                delay=self.paginator_delete_delay
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
