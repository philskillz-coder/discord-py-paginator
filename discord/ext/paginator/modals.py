from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import User, Interaction, ui
from discord.utils import MISSING

if TYPE_CHECKING:
    from .paginator import Paginator


class QuickNav(ui.Modal, title="Quick Navigation"):
    def __init__(
            self,
            *,
            parent: Paginator,
            user: User,
            title: str = MISSING,
            timeout: Optional[float] = None,
            custom_id: str = MISSING
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.parent = parent
        self.user = user
        self.interaction_check = self.parent.interaction_check

    page = ui.TextInput(label='Page')

    async def on_submit(self, interaction: Interaction):
        if not str(self.page).isdigit() or not await self.parent.child_update_page_number(interaction, int(str(self.page)) - 1):
            await interaction.response.send_message(
                self.parent.quick_navigation_error_message % self.page.value,
                ephemeral=True
            )
            raise ValueError("Not a number")

        await self.parent.child_update_page_content(interaction)


class Search(ui.Modal, title="Search"):
    def __init__(
            self,
            *,
            parent: Paginator,
            user: User,
            title: str = MISSING,
            timeout: Optional[float] = None,
            custom_id: str = MISSING
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.parent = parent
        self.user = user
        self.interaction_check = self.parent.interaction_check

    query = ui.TextInput(label='Query')

    async def on_submit(self, interaction: Interaction):
        page_number = await self.parent.search_page(interaction, query=self.query.value)
        if page_number is None or not await self.parent.child_update_page_number(interaction, page_number):
            await interaction.response.send_message(
                self.parent.search_button_error_message % self.query.value,
                ephemeral=True
            )
            return

        await self.parent.child_update_page_content(interaction)
