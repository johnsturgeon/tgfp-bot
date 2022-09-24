""" Script will listen for messages and respond with smart things """
import os
from typing import List

import sentry_sdk
import hikari
import lightbulb
from tgfp_lib import TGFP, TGFPPlayer
from help import get_help

from get_standings import get_game_care_scores_for_player, formatted_care
tgfp: TGFP = TGFP()


sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN_TGFP_BOT'),
    traces_sample_rate=1.0
)
components = hikari.api.CacheComponents.ALL - hikari.api.CacheComponents.MESSAGES

bot: lightbulb.BotApp = lightbulb.BotApp(
    token=os.getenv('DISCORD_AUTH_TOKEN'),
    intents=hikari.Intents.ALL,
    banner=None,
    cache_settings=hikari.impl.CacheSettings(
        components=components
    )
)


@bot.command
@lightbulb.option(
    "expand",
    description="display results in expanded form, more detail",
    type=bool,
    default=False
)
@lightbulb.command("do_i_care", description="How much do you care about this week's games")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    player: TGFPPlayer = tgfp.find_players(discord_id=ctx.member.id)[0]
    if not player.this_weeks_picks():
        await ctx.respond("You must not care that much, you haven't even entered your picks yet!")
    else:
        scores = get_game_care_scores_for_player(player)
        await ctx.respond(formatted_care(scores))


@bot.command
@lightbulb.option(
    "help_topic",
    description="Get help for the various TGFP Bot commands",
    choices=['all', 'do_i_care']
)
@lightbulb.command("help", description="TGFP Bot Command Help")
@lightbulb.implements(lightbulb.SlashCommand)
async def give_help(ctx: lightbulb.Context) -> None:
    match ctx.options.help_topic:
        case 'do_i_care':
            await ctx.respond(get_help('do_i_care'))
        case 'all':
            await ctx.respond(get_help('all'))


def main():
    bot.run()


if __name__ == '__main__':
    main()
