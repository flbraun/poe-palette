import dataclasses
import functools
import http

from tabulate import tabulate

from .types import LeagueType
from .utils import LoggedRequestsSession, slugify


@dataclasses.dataclass(frozen=True)
class League:
    type_: LeagueType
    title: str  # e.g. "Ancestor"
    slug: str  # e.g. "ancestor"
    is_hardcore: bool


@functools.cache
def get_leagues() -> dict[LeagueType, League]:
    session = LoggedRequestsSession()

    res = session.get('https://poe.ninja/api/data/getindexstate')
    assert res.status_code == http.HTTPStatus.OK

    res_parsed = res.json()

    leagues = {
        LeagueType.STANDARD: League(
            type_=LeagueType.STANDARD,
            title='Standard',
            slug='standard',
            is_hardcore=False,
        ),
        LeagueType.HARDCORE: League(
            type_=LeagueType.HARDCORE,
            title='Hardcore',
            slug='hardcore',
            is_hardcore=True,
        ),
    }

    # challenge league usually is the first
    challenge_league_name = res_parsed['economyLeagues'][0]['name']
    assert challenge_league_name != 'Standard', challenge_league_name
    assert 'Hardcore' not in challenge_league_name, challenge_league_name
    assert 'Ruthless' not in challenge_league_name, challenge_league_name
    assert 'HC' not in challenge_league_name, challenge_league_name

    leagues[LeagueType.CHALLENGE] = League(
        type_=LeagueType.CHALLENGE,
        title=challenge_league_name,
        slug=slugify(challenge_league_name),
        is_hardcore=False,
    )
    leagues[LeagueType.CHALLENGE_HARDCORE] = League(
        type_=LeagueType.CHALLENGE_HARDCORE,
        title=f'Hardcore {challenge_league_name}',
        slug=f'{leagues[LeagueType.CHALLENGE].slug}hc',
        is_hardcore=True,
    )

    print(
        tabulate(
            [[league_type, league.title, league.slug, league.is_hardcore] for league_type, league in leagues.items()],
            headers=('league type', 'human', 'slug', 'is hardcore'),
            tablefmt='outline',
        ),
    )

    return leagues
