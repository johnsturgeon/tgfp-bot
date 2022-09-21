""" Script will listen for messages and respond with smart things """
import os
import sentry_sdk
import hikari

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN_TGFP_BOT'),
    traces_sample_rate=1.0
)

bot: hikari.GatewayBot = hikari.GatewayBot(
    token=os.getenv('DISCORD_AUTH_TOKEN'),
    intents=hikari.Intents.ALL
)


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    if event.content == "!TGFP Scores":
        await event.message.respond("No scores yet!!")


def main():
    bot.run()


if __name__ == '__main__':
    main()
