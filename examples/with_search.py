from typing import Optional

import discord
from discord.ext.paginator import Paginator


class MemberPaginator(Paginator):
    search_button_error_message = "Nothing found for '%s'"

    async def search_page(self, interaction: discord.Interaction, query: str) -> Optional[int]:
        for i, member in enumerate(interaction.guild.members):
            if query in member.name:
                print(i, member.name)
                return i

        return None
