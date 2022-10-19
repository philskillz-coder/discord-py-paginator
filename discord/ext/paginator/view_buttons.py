from __future__ import annotations

from abc import ABC

from discord import ButtonStyle, User, Interaction
from discord.ext.commands import Bot

from . import button, errors, modals

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .paginator import Paginator


class FirstElement(button.BetterButton):
    def __init__(
            self,
            style: ButtonStyle,
            label: str,
            emoji: str,
            /,
            client: Bot,
            parent: Paginator,
            user: User,
            using: bool,
            disabled: bool = True
    ):
        super().__init__(
            style=style,
            label=label,
            emoji=emoji,
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user
        self.using = using

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this!")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent._child_update_page_number(interaction, 0)
        await self.parent._child_update_page_content(interaction)


class PreviousElement(button.BetterButton):
    def __init__(
            self,
            style: ButtonStyle,
            label: str,
            emoji: str,
            /,
            client: Bot,
            parent: Paginator,
            user: User,
            using: bool,
            disabled: bool = True
    ):
        super().__init__(
            style=style,
            label=label,
            emoji=emoji,
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user
        self.using = using

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this!")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent._child_update_page_number(interaction, self.parent.page - 1)
        await self.parent._child_update_page_content(interaction)


class NextElement(button.BetterButton):
    def __init__(
            self,
            style: ButtonStyle,
            label: str,
            emoji: str,
            /,
            client: Bot,
            parent: Paginator,
            user: User,
            using: bool,
            disabled: bool = True
    ):
        super().__init__(
            style=style,
            label=label,
            emoji=emoji,
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user
        self.using = using

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this!")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent._child_update_page_number(interaction, self.parent.page + 1)
        await self.parent._child_update_page_content(interaction)


class LastElement(button.BetterButton):
    def __init__(
            self,
            style: ButtonStyle,
            label: str,
            emoji: str,
            /,
            client: Bot,
            parent: Paginator,
            user: User,
            using: bool,
            disabled: bool = True
    ):
        super().__init__(
            style=style,
            label=label,
            emoji=emoji,
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user
        self.using = using

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this!")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent._child_update_page_number(
            interaction,
            (await self.parent.get_page_count(interaction) or self.parent.page+1)-1
        )
        await self.parent._child_update_page_content(interaction)


class Stop(button.BetterButton):
    def __init__(
            self,
            style: ButtonStyle,
            label: str,
            emoji: str,
            /,
            client: Bot,
            parent: Paginator,
            user: User,
            using: bool,
            disabled: bool = True
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user
        self.using = using

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this!")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent._child_paginator_stop(interaction)
        await interaction.response.send_message(
            content="Stopped",
            ephemeral=True
        )


class Start(button.BetterButton):
    def __init__(
            self,
            style: ButtonStyle,
            label: str,
            emoji: str,
            /,
            client: Bot,
            parent: Paginator,
            user: User,
            using: bool,
            disabled: bool = True
    ):
        super().__init__(
            style=style,
            label=label,
            emoji=emoji,
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user
        self.using = using

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this!")

        return True

    async def on_error(self, interaction: Interaction, error: errors.ButtonException):
        await interaction.response.send_message(
            content=error.message,
            ephemeral=True
        )

    async def on_click(self, interaction: Interaction):
        await self.parent._child_paginator_start(interaction)


class QuickNav(button.BetterButton):
    def __init__(
            self,
            style: ButtonStyle,
            label: str,
            emoji: str,
            /,
            client: Bot,
            parent: Paginator,
            user: User,
            using: bool,
            disabled: bool = True
    ):
        super().__init__(
            style=style,
            label=label,
            emoji=emoji,
            disabled=disabled
        )
        self.client = client
        self.parent = parent
        self.user = user
        self.using = using

    @button.button_check(1)
    async def check_author(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            raise errors.NotAuthor("You are not allowed to do this!")

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
            self,
            style: ButtonStyle,
            label: str,
            emoji: str,
            /
    ):
        super().__init__(
            style=style,
            label=label,
            emoji=emoji,
            disabled=True
        )
