from discord.ext import commands
from discord import Interaction, Intents, Embed, Color
from discord.ext.paginator import paginator

intents = Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


class GuildPaginator(paginator.Paginator):
    async def get_page_count(self, interaction: Interaction) -> int:
        return len(self.client.guilds)

    async def page_update(self, interaction: Interaction, current_page: int):
        guild = self.client.guilds[current_page]

        return await interaction.response.edit_message(
            content=f"Guild {current_page + 1}/{await self.get_page_count(interaction)}",
            embed=(
                Embed(
                    title="Guild",
                    colour=Color.green()
                )
                .add_field(name="Name", value=guild.name)
                .add_field(name="ID", value=str(guild.id))
                .add_field(name="Member count", value=str(guild.member_count), inline=False)
            ),
            view=self
        )

class MemberPaginator(paginator.Paginator):
    async def get_page_count(self, interaction: Interaction) -> int:
        return interaction.guild.member_count

    async def page_update(self, interaction: Interaction, current_page: int):
        member = interaction.guild.members[current_page]

        return await interaction.response.edit_message(
            content=f"Member {current_page + 1}/{await self.get_page_count(interaction)}",
            embed=(
                Embed(
                    title=f"Member {member}",
                    colour=Color.green()
                )
                .add_field(name="Display Name", value=member.display_name)
                .add_field(name="ID", value=str(member.id))
                .add_field(name="Created at", value=str(member.created_at), inline=False)
                .add_field(name="Is bot", value=str(member.bot), inline=False)
            ),
            view=self
        )


@bot.command(
    name="guilds",
    description="Show all the guilds"
)
async def show_guilds(ctx: commands.Context):
    await ctx.send(
        content="The bot guilds",
        view=await GuildPaginator(
            ctx.bot,
            ctx.author
        ).run()
    )

@bot.command(
    name="members",
    description="Show all the guild members"
)
async def show_guilds(ctx: commands.Context):
    await ctx.send(
        content="The guild members",
        view=await MemberPaginator(
            ctx.bot,
            ctx.author
        ).run()
    )

with open("token", "r") as f:
    token = f.read()

bot.run(
    token
)