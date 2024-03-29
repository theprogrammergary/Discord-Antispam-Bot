"""
Entry for Discord Bot that acts as a controller for bot events and commands.
"""

# imports
import sys

import discord
from discord import app_commands
from discord.ext import commands

import config
import services.imposter.functions as imposter
import services.shared.functions as shared
import services.spam.functions as spam
import services.trading_plans.functions as trading_plans
import services.verify.commands as verify_commands
import services.verify.functions as verify
from config import logger

bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())


@bot.event
async def on_ready() -> None:
    """
    Controller for on_ready event.
    """

    await shared.log_in(bot=bot, discord=discord)


@bot.event
async def on_raw_reaction_add(payload) -> None:
    """
    Controller for on_reaction event.
    """

    guild: discord.Guild | None = bot.get_guild(payload.guild_id)
    channel: discord.GuildChannel | None = guild.get_channel(payload.channel_id)  # type: ignore

    if channel.name == config.VERIFY_CHANNEL:  # type: ignore
        await verify.check_verification(bot=bot, discord=discord, payload=payload)


@bot.event
async def on_member_join(member) -> None:
    """
    Controller for on_member_join event.
    """
    await imposter.member_joined(bot=bot, discord=discord, member=member)


@bot.event
async def on_member_update(before, after) -> None:
    """
    Controller for on_member_update event.
    """
    await imposter.member_updated(bot=bot, discord=discord, before=before, after=after)


@bot.event
async def on_user_update(before, after) -> None:
    """
    Controller for on_user_update event.
    """
    await imposter.user_updated(bot=bot, discord=discord, before=before, after=after)


@bot.event
async def on_message(message) -> None:
    """
    Controller for on_message event.
    """
    await spam.check_msg_for_spam(bot=bot, discord=discord, message=message)
    await trading_plans.check_trading_plan(bot=bot, message=message)


@bot.event
async def on_command_error() -> None:
    """
    Controller for on_command_error event.
    """
    return


@bot.tree.command(name="verify")
@app_commands.describe(
    url="Enter the URL:",
    question="Enter the question",
    answer="Enter the answer:",
    a="A",
    b="B",
    c="C",
    d="D",
)
async def verify_command(
    interaction: discord.Interaction,
    url: str,
    question: str,
    answer: str,
    a: str,
    b: str,
    c: str,
    d: str,
) -> None:
    """
    Controller for /verify command.
    """

    await verify_commands.command_new_verification(
        discord=discord,
        bot=bot,
        interaction=interaction,
        url=url,
        question=question,
        answer=answer,
        a=a,
        b=b,
        c=c,
        d=d,
    )


if __name__ == "__main__":
    if config.BOT_TOKEN is None:
        logger.critical("BOT_TOKEN is not configured.")
        sys.exit(1)

    bot.run(token=config.BOT_TOKEN)
