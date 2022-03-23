from __future__ import annotations
from discord.ui import Button
from discord import ButtonStyle, Emoji, PartialEmoji, Interaction

from typing import Any, Dict, Callable, List, Coroutine, Type, Optional, Union

from .errors import ButtonException, ButtonFailed

EH = Callable[[Any, Interaction, ButtonException], Coroutine[Any, Any, Any]]
CH = Callable[[Any, Interaction], Coroutine[Any, Any, bool]]


class ButtonErrorHandler:
    def __init__(self, callback: EH, exception_type: Type[ButtonException]):
        self.callback = callback
        self.exception_type: Type[ButtonException] = exception_type

    async def invoke(self, instance, interaction: Interaction, error: ButtonException):
        return await self.callback(instance, interaction, error)


class ButtonCheck:
    def __init__(self, callback: CH, priority: int):
        self.callback = callback
        self.priority = priority

    async def invoke(self, instance, interaction: Interaction):
        return await self.callback(instance, interaction)


class ButtonMeta(type):
    __error_handlers__: Dict[Type[ButtonException], ButtonErrorHandler] = {}
    __checks__: Dict[int, ButtonCheck] = {}

    def __new__(mcs, *args: Any, **kwargs: Any):
        name, bases, attrs = args
        error_handlers = {}
        checks = {}

        new_cls = super().__new__(mcs, *args, **kwargs)
        for base in reversed(new_cls.__mro__):
            for elem, value in base.__dict__.items():
                if isinstance(value, ButtonErrorHandler):
                    error_handlers[value.exception_type] = value

                if isinstance(value, ButtonCheck):
                    checks[value.priority] = value

        new_cls.__error_handlers__ = error_handlers
        new_cls.__checks__ = checks

        return new_cls

    def __init__(cls, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args)


def button_on_error(exception_type: Type[ButtonException]):
    def deco(method: EH) -> ButtonErrorHandler:
        return ButtonErrorHandler(method, exception_type)

    return deco


def button_check(priority: int):
    def deco(method: CH) -> ButtonCheck:
        return ButtonCheck(method, priority)

    return deco


class BetterButton(Button, metaclass=ButtonMeta):
    def __init__(
            self,
            style: ButtonStyle = ButtonStyle.secondary,
            label: Optional[str] = None,
            disabled: bool = False,
            custom_id: Optional[str] = None,
            url: Optional[str] = None,
            emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
            row: Optional[int] = None
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row
        )

    async def on_error(self, interaction: Interaction, error: ButtonException):
        raise error

    async def interaction_check(self, interaction: Interaction) -> bool:
        return True

    async def on_click(self, interaction: Interaction):
        raise NotImplementedError("On click method not implemented!")

    async def callback(self, interaction: Interaction) -> Optional[Any]:
        try:
            value = await self.interaction_check(interaction)
            if value is not True:
                raise ButtonFailed(f"Interaction check {self.interaction_check.__name__!r} with priority 0 failed!")

            _checks: List[ButtonCheck] = sorted(self.__checks__.values(), key=lambda c: c.priority)

            for check in _checks:
                value = await check.invoke(self, interaction)

                if value is not True:
                    raise ButtonFailed("Button check failed!")

        except ButtonException as button_exception:
            for exception_type, callback in self.__error_handlers__.items():
                if isinstance(button_exception, exception_type):
                    await callback.invoke(self, interaction, button_exception)
                    return None

            await self.on_error(interaction, button_exception)
            return None

        return await self.on_click(interaction)

    def __init__button__(self, parent):
        self.parent = parent