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

    page = ui.TextInput(label='Page')

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(
                content="You are not allowed to do this",
                ephemeral=True
            )
            raise ValueError("You are not allowed to do this!")  # add better error message

        return True

    async def on_submit(self, interaction: Interaction):
        if not str(self.page).isdigit():
            await interaction.response.send_message(f"`{self.page}` is not a number!")
            raise ValueError("Not a number")  # add better error message

        await self.parent.__child_update_page_number(interaction, int(str(self.page)) - 1)
        await self.parent._child_update_page_content(interaction)
