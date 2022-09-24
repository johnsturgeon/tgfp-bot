import hikari


def get_help(command) -> hikari.Embed:
    help_embed: hikari.Embed = hikari.Embed(
        title="TGFP Bot Command Help",
        description="You can type `/help [command]` to get specific help \
            for one command, or just `/help all` for all commands",
        color="#ffdc00"
    )
    match command:
        case 'do_i_care':
            add_do_i_care_command_to_embed(help_embed)
        case 'all':
            add_all_commands_to_embed(help_embed)
    return help_embed


def add_all_commands_to_embed(embed: hikari.Embed):
    add_do_i_care_command_to_embed(embed, True)


def add_do_i_care_command_to_embed(embed: hikari.Embed, add_description_to_field=False):
    title: str = "TGFP Bot Help for `/do_i_care`"
    description: str = "> _Gives each game a 'star' rating based on how \
           many people picked *differently* than you!_"
    field_description = ""
    if not add_description_to_field:
        embed.title = title
        embed.description = description
    else:
        field_description = f"{title}\n{description}\n"
    embed.add_field(
        name="`/do_i_care`",
        value=f"""{field_description}
    • No Star means everybody picked the SAME
    • :star: == 0-29 % of players picked against you
    • :star::star: == 30-49 %
    • :star::star::star: == 50-69 %
    • :star::star::star::star: == 70-89 %
    • :star::star::star::star::star: == > 90 %
    """
    )
