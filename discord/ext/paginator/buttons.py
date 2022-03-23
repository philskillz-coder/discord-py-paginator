from __future__ import annotations

from discord import ButtonStyle, User, Interaction
from discord.ext.commands import Bot

from . import button, errors

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
            style=ButtonStyle.blurple,
            emoji="\U000023ee",
            label="First",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not keine ahnung")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.set_page(1)
        await interaction.response.edit_message(
            **await self.parent.get_page_content()
        )


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
            emoji="\U000025c0",
            label="Previous",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not keine ahnung")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.set_page(self.parent.page-1)
        await interaction.response.edit_message(
            **await self.parent.get_page_content()
        )



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
            emoji="\U000027a1",
            label="Next",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not keine ahnung")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.set_page(self.parent.page + 1)
        await interaction.response.edit_message(
            **await self.parent.get_page_content()
        )



class LastElement(button.BetterButton):
    def __init__(
            self,
            client: Bot,
            parent: Paginator,
            user: User,
            disabled: bool = True
    ):
        super().__init__(
            style=ButtonStyle.blurple,
            emoji="\U000023ed",
            label="Last",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not keine ahnung")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.set_page(await self.parent.get_page_count())
        await interaction.response.edit_message(
            **await self.parent.get_page_content()
        )

class Stop(button.BetterButton):
    def __init__(
            self,
            client: Bot,
            parent: Paginator,
            user: User,
            disabled: bool = True
    ):
        super().__init__(
            style=ButtonStyle.blurple,
            emoji="\U0001f7e5",
            label="Stop",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not keine ahnung")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        self.parent.stop()
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
            style=ButtonStyle.blurple,
            emoji="\U0001f7e9",
            label="Start",
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not keine ahnung")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent.start()
        await self.parent.set_page(1)
        values = await self.parent.get_page_content()
        values.update({"view": self.parent})

        await interaction.response.edit_message(
            **values
        )