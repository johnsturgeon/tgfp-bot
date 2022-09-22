""" Script will listen for messages and respond with smart things """
import os
import sentry_sdk
import hikari
from tgfp_lib import TGFP, TGFPPlayer

from get_standings import get_game_care_scores_for_player, formatted_care
tgfp: TGFP = TGFP()

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN_TGFP_BOT'),
    traces_sample_rate=1.0
)

bot: hikari.GatewayBot = hikari.GatewayBot(
    token=os.getenv('DISCORD_AUTH_TOKEN'),
    intents=hikari.Intents.ALL
)
help_string: str = """
```
!TGFP commands:
========================
 - !TGFP Do I Care
    Description:
     Gives each game a 'star' rating based on how many people picked *differently* than you!
     No Star means everybody picked the SAME
     ⭐  == 0-29 % of players picked against you
     ⭐️⭐️  == 30-49 %
     ⭐️⭐️⭐  == 50-69 %
     ⭐️⭐️⭐️⭐️  == 70-89 %
     ⭐️⭐️⭐️⭐️⭐️  == > 90 % of players picked against you
```
"""


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    if event.content == "!TGFP Scores":
        await event.message.respond("No scores yet!!")
    elif event.content.startswith('!TGFP Do I Care'):
        player: TGFPPlayer = tgfp.find_players(discord_id=event.member.id)[0]
        if not player.this_weeks_picks():
            await event.message.respond("You must not care that much, you haven't even entered your picks yet!")
        else:
            scores = get_game_care_scores_for_player(player)
            i_care_str: str = formatted_care(scores)
            i_care_str += "\n`!TGFP Help for description`"
            await event.message.respond(i_care_str)
    elif event.content.startswith('!TGFP'):
        await event.message.respond(help_string)


def main():
    bot.run()


if __name__ == '__main__':
    main()
