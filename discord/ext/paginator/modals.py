from __future__ import annotations

from discord import ButtonStyle, User, Interaction, ui
from discord.ext.commands import Bot
from discord.utils import MISSING

from . import button, errors

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .paginator import Paginator


class QuickNav(ui.Modal, title='Quick Navigation'):
    def __init__(self, *, parent: Paginator, user: User, title: str = MISSING, timeout: Optional[float] = None, custom_id: str = MISSING) -> None:
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
            raise ValueError("lazy") # add better error message

        return True

    async def on_submit(self, interaction: Interaction):
        if not str(self.page).isdigit():
            await interaction.response.send_message("This is not a number!")
            raise ValueError("lazy") # add better error message

        await self.parent.set_page(int(str(self.page)))
        await interaction.response.edit_message(
            **await self.parent.get_page_content()
        )
