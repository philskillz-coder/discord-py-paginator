from typing import Dict, Any, Union, Callable, Coroutine, Optional

from discord import ui, User, Interaction, ButtonStyle, Emoji, PartialEmoji

from . import modals

GCP_TYPE = Callable[[Interaction, int], Coroutine[Any, Any, Dict[str, Any]]]


class PaginatorButton(ui.Button):
    def __init__(
            self,
            parent: "Paginator",
            /,
            *,
            style: ButtonStyle = ButtonStyle.secondary,
            label: Optional[str] = None,
            disabled: bool = False,
            url: Optional[str] = None,
            emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            url=url,
            emoji=emoji,
        )
        self.parent = parent


class FirstElementButton(PaginatorButton):
    async def callback(self, interaction: Interaction) -> Any:
        await self.parent.child_update_page_number(interaction, 0)
        await self.parent.child_update_page_content(interaction)


class PreviousElementButton(PaginatorButton):
    async def callback(self, interaction: Interaction) -> Any:
        await self.parent.child_update_page_number(interaction, self.parent.page - 1)
        await self.parent.child_update_page_content(interaction)


class NextElementButton(PaginatorButton):
    async def callback(self, interaction: Interaction) -> Any:
        await self.parent.child_update_page_number(interaction, self.parent.page + 1)
        await self.parent.child_update_page_content(interaction)


class LastElementButton(PaginatorButton):
    async def callback(self, interaction: Interaction) -> Any:
        await self.parent.child_update_page_number(
            interaction,
            (await self.parent.get_page_count(interaction) or self.parent.page + 1) - 1
        )
        await self.parent.child_update_page_content(interaction)


class StopButton(PaginatorButton):
    async def callback(self, interaction: Interaction) -> Any:
        await self.parent.child_paginator_stop(interaction)
        await interaction.response.send_message(
            content="Stopped",
            ephemeral=True
        )


class StartButton(PaginatorButton):
    async def callback(self, interaction: Interaction) -> Any:
        await self.parent.child_paginator_start(interaction)
        await self.parent.child_update_page_number(interaction, 0)
        await self.parent.child_update_page_content(interaction)


class QuickNavigationButton(PaginatorButton):
    async def callback(self, interaction: Interaction) -> Any:
        await interaction.response.send_modal(modals.QuickNav(parent=self.parent, user=self.parent.user))


class PlaceholderButton(PaginatorButton):

    async def callback(self, interaction: Interaction) -> Any:
        pass


class PageNumberButton(PaginatorButton):
    async def callback(self, interaction: Interaction) -> Any:
        pass


class SearchButton(PaginatorButton):
    async def callback(self, interaction: Interaction) -> Any:
        await interaction.response.send_modal(modals.Search(parent=self.parent, user=self.parent.user))


class Paginator(ui.View):
    paginator_view_timeout: int = 180
    paginator_delete_when_finished: bool = True  # only works when paginator is not ephemeral
    paginator_delete_delay: int = 10
    paginator_not_allowed_message: str = "You are not allowed to do this!"

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
    quick_navigation_error_message: str = "%s is not a number!"

    page_number_button_enabled: bool = True
    page_number_button_style: ButtonStyle = ButtonStyle.secondary
    page_number_button_label: str = "%s/%s"
    page_number_button_emoji: str = None

    search_button_enabled: bool = True
    search_button_style: ButtonStyle = ButtonStyle.secondary
    search_button_label: str = "\U0001f50d"
    search_button_emoji: str = None
    search_button_error_message: str = "No results found for '%s!'"

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
            user: User
    ):
        super().__init__(timeout=self.paginator_view_timeout)

        self.user = user
        self.page = 0

        self.first_elem_btn = FirstElementButton(
            self,
            style=self.first_element_button_style,
            label=self.first_element_button_label,
            emoji=self.first_element_button_emoji,
            disabled=True
        )

        self.prev_elem_btn = PreviousElementButton(
            self,
            style=self.prev_element_button_style,
            label=self.prev_element_button_label,
            emoji=self.prev_element_button_emoji,
            disabled=True
        )

        self.next_elem_btn = NextElementButton(
            self,
            style=self.next_element_button_style,
            label=self.next_element_button_label,
            emoji=self.next_element_button_emoji,
            disabled=True
        )

        self.last_elem_btn = LastElementButton(
            self,
            style=self.last_element_button_style,
            label=self.last_element_button_label,
            emoji=self.last_element_button_emoji,
            disabled=True
        )

        self.start_btn = StartButton(
            self,
            style=self.start_button_style,
            label=self.start_button_label,
            emoji=self.start_button_emoji,
            disabled=False
        )

        self.stop_btn = StopButton(
            self,
            style=self.stop_button_style,
            label=self.stop_button_label,
            emoji=self.stop_button_emoji,
            disabled=False
        )

        self.quick_nav_btn = QuickNavigationButton(
            self,
            style=self.quick_navigation_button_style,
            label=self.quick_navigation_button_label,
            emoji=self.quick_navigation_button_emoji,
            disabled=True
        )

        self.page_number_btn = PageNumberButton(
            self,
            style=self.page_number_button_style,
            label=self.page_number_button_label % ("-", "-"),
            emoji=self.page_number_button_emoji,
            disabled=True
        )

        self.search_btn = SearchButton(
            self,
            style=self.search_button_style,
            label=self.search_button_label,
            emoji=self.search_button_emoji,
            disabled=True
        )

    async def run(self, *args, **kwargs):
        """
        Runs the paginator.
        args and kwargs get passed to :func:`on_setup <discord.ext.paginator.paginator.Paginator.on_setup>`"""
        await self.on_setup(*args, **kwargs)

        await self.add_buttons()

        return self

    async def on_setup(self, *args, **kwargs):  # for users
        pass

    async def on_start(self, interaction: Interaction):  # for users
        pass

    async def on_stop(self, interaction: Interaction):  # for users
        pass

    async def interaction_check(self, interaction: Interaction, /) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(self.paginator_not_allowed_message, ephemeral=True)
            return False

        return True

    # noinspection PyArgumentList
    async def add_buttons(self):
        placeholder_config = dict(
            style=self.placeholder_button_style,
            label=self.placeholder_button_label,
            emoji=self.placeholder_button_emoji,
            disabled=True
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
            self.add_item(PlaceholderButton(self, **placeholder_config))

        # quick navigation
        if self.quick_navigation_button_enabled:
            self.add_item(self.quick_nav_btn)

        self.add_item(self.stop_btn)

        # search button
        if self.search_button_enabled:
            self.add_item(self.search_btn)

        # placeholders
        if self.placeholder_button_enabled:
            self.add_item(PlaceholderButton(self, **placeholder_config))

    # noinspection PyArgumentList
    async def child_paginator_start(self, interaction: Interaction):
        for item in self.children:
            if isinstance(item, PaginatorButton):
                self.remove_item(item)

        self.first_elem_btn.disabled = False
        self.prev_elem_btn.disabled = False
        self.next_elem_btn.disabled = False
        self.last_elem_btn.disabled = False
        self.quick_nav_btn.disabled = False
        self.search_btn.disabled = False

        placeholder_config = dict(
            style=self.placeholder_button_style,
            label=self.placeholder_button_label,
            emoji=self.placeholder_button_emoji,
            disabled=True
        )

        # first element, previous element
        if self.first_element_button_enabled:
            self.add_item(self.first_elem_btn)
        if self.prev_element_button_enabled:
            self.add_item(self.prev_elem_btn)

        # page number
        if self.page_number_button_enabled:
            self.add_item(self.page_number_btn)

        # next element, last element
        if self.next_element_button_enabled:
            self.add_item(self.next_elem_btn)
        if self.last_element_button_enabled:
            self.add_item(self.last_elem_btn)

        # placeholders
        if self.placeholder_button_enabled:
            self.add_item(PlaceholderButton(self, **placeholder_config))

        # quick navigation
        if self.quick_navigation_button_enabled:
            self.add_item(self.quick_nav_btn)

        self.add_item(self.stop_btn)

        # search button
        if self.search_button_enabled:
            self.add_item(self.search_btn)

        # placeholders
        if self.placeholder_button_enabled:
            self.add_item(PlaceholderButton(self, **placeholder_config))

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
        self.page_number_btn.label = self.page_number_button_label % (str(self.page + 1), str(await self.get_page_count(interaction)))
        await self.page_update(interaction, self.page)

    async def get_page_count(self, interaction: Interaction) -> int:
        raise NotImplementedError("get_page_count must be implemented!")

    async def page_update(self, interaction: Interaction, current_page: int):
        raise NotImplementedError("page_update must be implemented!")

    async def search_page(self, interaction: Interaction, query: str) -> Optional[int]:
        return None
