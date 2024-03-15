import dataclasses
import functools
import http

from tabulate import tabulate

from .types import LeagueType
from .utils import DefaultHTTPSession, slugify


@dataclasses.dataclass(frozen=True)
class League:
    type_: LeagueType
    title: str  # e.g. "Ancestor"
    slug: str  # e.g. "ancestor"
    is_hardcore: bool
    previous_title: str | None = None  # league before self.title, e.g. "Crucible"
    previous_slug: str | None = None  # league before self.title, e.g. "crucible"


@functools.cache
def get_leagues() -> dict[LeagueType, League]:
    session = DefaultHTTPSession()

    url = 'https://poe.ninja/api/data/getindexstate'
    res = session.get(url)
    assert res.status_code == http.HTTPStatus.OK, f'{res.status_code} {url}'

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

    # current challenge league usually is the first
    challenge_league_name = res_parsed['economyLeagues'][0]['name']
    assert challenge_league_name != 'Standard', challenge_league_name
    assert 'Hardcore' not in challenge_league_name, challenge_league_name
    assert 'Ruthless' not in challenge_league_name, challenge_league_name
    assert 'HC' not in challenge_league_name, challenge_league_name

    # find previous challenge league
    previous_challenge_league_name = res_parsed['oldEconomyLeagues'][0]['name']
    assert previous_challenge_league_name != challenge_league_name
    assert previous_challenge_league_name != 'Standard', challenge_league_name
    assert 'Hardcore' not in previous_challenge_league_name, previous_challenge_league_name
    assert 'Ruthless' not in previous_challenge_league_name, previous_challenge_league_name
    assert 'HC' not in previous_challenge_league_name, previous_challenge_league_name

    leagues[LeagueType.CHALLENGE] = League(
        type_=LeagueType.CHALLENGE,
        title=challenge_league_name,
        previous_title=previous_challenge_league_name,
        slug=slugify(challenge_league_name),
        previous_slug=slugify(previous_challenge_league_name),
        is_hardcore=False,
    )
    leagues[LeagueType.CHALLENGE_HARDCORE] = League(
        type_=LeagueType.CHALLENGE_HARDCORE,
        title=f'Hardcore {challenge_league_name}',
        previous_title=f'Hardcore {previous_challenge_league_name}',
        slug=f'{leagues[LeagueType.CHALLENGE].slug}hc',
        previous_slug=f'{leagues[LeagueType.CHALLENGE].previous_slug}hc',
        is_hardcore=True,
    )

    print(
        tabulate(
            [
                [
                    league_type,
                    league.title,
                    league.slug,
                    league.previous_title,
                    league.previous_slug,
                    league.is_hardcore,
                ]
                for league_type, league in leagues.items()
            ],
            headers=('league type', 'current human', 'current slug', 'previous human', 'previous slug', 'is hardcore'),
            tablefmt='outline',
        ),
    )

    return leagues
