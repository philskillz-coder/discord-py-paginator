from typing import Optional, Literal

import discord
from discord.ext import commands
from discord.ext.paginator import paginator

i = discord.Intents.default()
i.message_content = True
i.members = True

bot = commands.Bot(
    "!",
    intents=i
)


class GuildPaginator(paginator.Paginator):
    async def get_page_count(self, interaction: discord.Interaction) -> int:
        return len(self.client.guilds)

    async def page_update(self, interaction: discord.Interaction, current_page: int):
        guild = self.client.guilds[current_page]

        return await interaction.response.edit_message(
            content=f"Guild {current_page + 1}/{await self.get_page_count(interaction)}",
            embed=(
                discord.Embed(
                    title=f"Guild {guild.name}"
                )
                .add_field(name="ID", value=str(guild.id))
                .add_field(name="Created at", value=str(guild.created_at), inline=False)
            ),
            view=self
        )


class MemberPaginator(paginator.Paginator):
    placeholder_button_enabled = False

    async def get_page_count(self, interaction: discord.Interaction) -> int:
        return interaction.guild.member_count

    async def page_update(self, interaction: discord.Interaction, current_page: int):
        member = interaction.guild.members[current_page]

        return await interaction.response.edit_message(
            content=f"Member {current_page + 1}/{await self.get_page_count(interaction)}",
            embed=(
                discord.Embed(
                    title=str(member),
                    colour=discord.Color.green()
                )
                .add_field(name="ID", value=str(member.id))
                .add_field(name="Created at", value=str(member.created_at), inline=False)
                .add_field(name="Joined at", value=str(member.joined_at), inline=False)
                .add_field(name="Roles", value=", ".join([role.name for role in member.roles]))
            ),
            view=self
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


@bot.command()
async def show_guilds(ctx: commands.Context):
    await ctx.send(
        content="The bot guilds",
        view=await GuildPaginator(
            ctx.bot,
            ctx.author
        ).run()
    )


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
    name="guilds",
    description="Show all the guilds"
)
async def show_guilds(interaction: discord.Interaction):
    await interaction.response.send_message(
        content="The bot guilds",
        view=await GuildPaginator(
            interaction.client,
            interaction.user
        ).run(interaction),
        ephemeral=True
    )


@bot.tree.command(
    name="members",
    description="Show the guild members"
)
async def show_guilds(interaction: discord.Interaction):
    await interaction.response.send_message(
        content="The guild members",
        view=await MemberPaginator(
            interaction.client,
            interaction.user
        ).run(interaction),
        ephemeral=True
    )


with open("TOKEN", "r") as f:
    token = f.read()

bot.run(token)
