from __future__ import annotations

from discord import ButtonStyle, User, Interaction
from discord.ext.commands import Bot

from . import button, errors, modals

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .paginator import Paginator

class FirstElement(button.BetterButton):
    def __init__(
            self,
            client: Bot,
            parent: Paginator,
            user: User,
            disabled: bool = True
    ):
        super().__init__(
            style=ButtonStyle.secondary,
            label="\U000025c0 \U000025c0",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.set_page(interaction, 1)
        await self.parent.update_contents(interaction)

class PreviousElement(button.BetterButton):
    def __init__(
            self,
            client: Bot,
            parent: Paginator,
            user: User,
            disabled: bool = True
    ):
        super().__init__(
            style=ButtonStyle.blurple,
            label="\U000025c0",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.set_page(interaction, self.parent.page-1)
        await self.parent.update_contents(interaction)


class NextElement(button.BetterButton):
    def __init__(
            self,
            client: Bot,
            parent: Paginator,
            user: User,
            disabled: bool = True
    ):
        super().__init__(
            style=ButtonStyle.blurple,
            label="\U000025b6",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.set_page(interaction, self.parent.page + 1)
        await self.parent.update_contents(interaction)

class LastElement(button.BetterButton):
    def __init__(
            self,
            client: Bot,
            parent: Paginator,
            user: User,
            disabled: bool = True
    ):
        super().__init__(
            style=ButtonStyle.secondary,
            label="\U000025b6 \U000025b6",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.set_page(interaction, await self.parent.get_page_count(interaction))
        await self.parent.update_contents(interaction)


class Stop(button.BetterButton):
    def __init__(
            self,
            client: Bot,
            parent: Paginator,
            user: User,
            disabled: bool = True
    ):
        super().__init__(
            style=ButtonStyle.danger,
            label="Quit",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.stop(interaction)
        await interaction.response.send_message(
            content="Stopped",
            ephemeral=True
        )

class Start(button.BetterButton):
    def __init__(
            self,
            client: Bot,
            parent: Paginator,
            user: User,
            disabled: bool = True
    ):
        super().__init__(
            style=ButtonStyle.success,
            label="Start",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.start(interaction)
        await interaction.response.defer()
        values = await self.parent._get_update_contents(interaction)
        values.update({"view": self.parent})

        ws = interaction.followup
        await ws.edit_message(
            (await interaction.original_message()).id,
            **values
        )


class QuickNav(button.BetterButton):
    def __init__(
            self,
            client: Bot,
            parent: Paginator,
            user: User,
            disabled: bool = True
    ):
        super().__init__(
            style=ButtonStyle.blurple,
            label="Nav",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await interaction.response.send_modal(modals.QuickNav(parent=self.parent, user=self.user))

class Placeholder(button.BetterButton):
    def __init__(
            self
    ):
        super().__init__(
            style=ButtonStyle.secondary,
            label="\U0001f6ab",
            disabled=True
        )
