from typing import Optional, Literal

import discord
from discord.ext import commands
from discord.ext.paginator import Paginator
from discord import ui

i = discord.Intents.default()
i.message_content = True
i.members = True

bot = commands.Bot(
    "!",
    intents=i
)


class MemberPaginator(Paginator):
    paginator_delete_when_finished = True
    paginator_delete_delay = 0  # 0 seconds
    paginator_not_allowed_message = "Sorry, its not for you!"

    page_number_button_label = "%s/%s"

    def __init__(self, client: commands.Bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client

    async def get_page_count(self, interaction: discord.Interaction) -> int:
        return interaction.guild.member_count

    async def page_update(self, interaction: discord.Interaction, current_page: int):
        member = interaction.guild.members[current_page]

        return await interaction.response.edit_message(
            content=f"Member {current_page + 1}/{await self.get_page_count(interaction)}",
            embed=(
                discord.Embed(
                    title=f"Member {member}"
                )
                .add_field(name="Created at", value=str(member.created_at), inline=False)
                .add_field(name="Joined at", value=str(member.joined_at), inline=False)
            ),
            view=self
        )

    search_button_error_message = "Nothing found for '%s'"

    async def search_page(self, interaction: discord.Interaction, query: str) -> Optional[int]:
        for i, member in enumerate(interaction.guild.members):
            if query in member.name:
                print(i, member.name)
                return i

        return None

    async def on_setup(self, *args, **kwargs):
        # This is called by Paginator.run (when the paginator is sent)
        # You could set up a database connection here, for example.
        # But I would rather do that in on_start because you're wasting resources if the paginator is not started.

        print("Setup")

    async def on_start(self, interaction: discord.Interaction):
        # This is called when the paginator is started
        # If you need a database connection, you should set it up here.
        self.kick_member.disabled = False
        print("Start")

    async def on_stop(self, interaction: discord.Interaction):
        # This is called when the paginator is stopped with the stop button NOT WHEN IT TIMES OUT
        # If you needed a database connection, you should close it here.

        print("Stop")

    @ui.button(
        label="Kick",
        disabled=True,
        style=discord.ButtonStyle.red,
        row=3
    )
    async def kick_member(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.members[self.page]
        await member.kick()
        await interaction.response.send_message(
            content="Kicked!",
            ephemeral=True
        )


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object],
               spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


@bot.command(
    name="members"
)
async def show_members(ctx: commands.Context):
    await ctx.send(
        content="The guild members",
        view=await MemberPaginator(
            ctx.bot,
            ctx.author
        ).run()
    )


@bot.tree.command(
    name="members"
)
async def show_members(interaction: discord.Interaction):
    await interaction.response.send_message(
        content="The guild members",
        view=await MemberPaginator(
            interaction.client,
            interaction.user
        ).run(),
        ephemeral=True
    )


with open("TOKEN", "r") as f:
    token = f.read()

bot.run(token)
