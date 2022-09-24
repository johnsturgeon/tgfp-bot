from dataclasses import dataclass
from typing import List

from tgfp_lib import TGFP, TGFPPlayer, TGFPPick, TGFPGame, TGFPTeam

tgfp = TGFP()
all_picks: List[TGFPPick] = tgfp.find_picks(week_no=tgfp.current_week())
all_games: List[TGFPGame] = tgfp.find_games(week_no=tgfp.current_week())


@dataclass
class GameCareScore:
    game: TGFPGame
    care_score: float
    player_count_against: int


def get_number_of_against(my_pick: TGFPPick, game: TGFPGame) -> int:
    number_of_against: int = 0
    pick: TGFPPick
    for pick in all_picks:
        if pick == my_pick:
            continue
        if pick.winner_for_game_id(game.id) != my_pick.winner_for_game_id(game.id):
            number_of_against += 1
    return number_of_against


def get_game_care_scores_for_player(player: TGFPPlayer) -> List[GameCareScore]:
    care_scores: List[GameCareScore] = []
    game: TGFPGame
    for game in all_games:
        number_against: int = get_number_of_against(player.this_weeks_picks(), game)
        number_of_picks: int = len(all_picks) - 1  # me
        score: float = round((number_against / number_of_picks), 2)
        care_scores.append(GameCareScore(game, score, number_against))
    return care_scores


def formatted_care(care_scores: List[GameCareScore]) -> str:
    output: str = ""
    for care in care_scores:
        if 0 < care.care_score < 0.1:
            stars = 1
        else:
            stars = round(care.care_score / .2)
        star_string: str = ""
        for n in range(stars):
            star_string += ':star:'
        road_team: TGFPTeam = tgfp.find_teams(care.game.road_team_id)[0]
        home_team: TGFPTeam = tgfp.find_teams(care.game.home_team_id)[0]
        road_team_emoji: str = road_team.discord_emoji
        home_team_emoji: str = home_team.discord_emoji
        # local_time = arrow.get(care.game.start_time).to('US/Pacific')
        # formatted_time = local_time.format("ddd @ h:mma ZZZ")
        output += f"{road_team_emoji} @ {home_team_emoji} {star_string}\n"

    output += "\n> Type `/help` for more information"
    return output


def length_of_city() -> int:
    max_length: int = 0
    for team in tgfp.teams():
        max_length = max(len(team.city), max_length)
    return max_length


def length_of_short_name() -> int:
    max_length: int = 0
    for team in tgfp.teams():
        max_length = max(len(team.short_name), max_length)
    return max_length


if __name__ == '__main__':
    me: TGFPPlayer = tgfp.find_players(player_full_name="John Sturgeon")[0]
    scores = get_game_care_scores_for_player(me)
    print(formatted_care(scores))
