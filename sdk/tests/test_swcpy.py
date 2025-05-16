import pytest
from swcpy import SWCClient
from swcpy import SWCConfig
from swcpy.schemas import League, Team, Player, Performance
from io import BytesIO
import pyarrow.parquet as pq
import pandas as pd
from typing import List 

def test_health_check():
    """Tests health check from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    response = client.get_health_check()
    assert(response.status_code == 200)
    assert("API health check successful" in response.json()["message"])

def test_list_leagues():
    """Tests get leagues from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    leagues_response = client.list_leagues()
    # Assert the endpoint return a list object
    assert(isinstance(leagues_response, List))
    # Assert each item in the list is an instance of a Pydantic League object
    for league in leagues_response:
        assert(isinstance(league, League))
    # Assert that 5 League objects are returned
    assert(len(leagues_response) == 5)

def test_list_leagues_no_backoff():
    """Tests get leagues from SDK without backoff"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    leagues_response = client.list_leagues()
    # Assert the list is not empty
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of League
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 5    

def test_get_leagues_with_filter():
    """Tests get leagues from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    leagues_response = client.list_leagues(league_name='Pigskin Prodigal Fantasy League')

    # Assert the list is not empty
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of League
    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 1


def test_get_league_by_id():
    """Tests get leagues from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    league_response = client.get_league_by_id(5002)
        
    assert isinstance(league_response, League)
    assert len(league_response.teams) == 8        

def test_list_teams():
    """Tests list teams from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    teams_response = client.list_teams()

    # Assert the list is not empty
    assert isinstance(teams_response, list)
    # Assert each item in the list is an instance of League
    for team in teams_response:
        assert isinstance(team, Team)
    assert len(teams_response) == 20



#players
def test_list_players():
    """Tests get players from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    players_response = client.list_players(skip=0,limit=1500)

    # Assert the list is not empty
    assert isinstance(players_response, list)
    # Assert each item in the list is an instance of League
    for player in players_response:
        assert isinstance(player, Player)
    assert len(players_response) == 1018


def test_list_players_by_name():
    """Tests that the count of players in the database is what is expected"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    players_response = client.list_players(first_name="Bryce", last_name="Young")

    # Assert the list is not empty
    assert isinstance(players_response, list)
    # Assert each item in the list is an instance of League
    for player in players_response:
        assert isinstance(player, Player)
    assert len(players_response) == 1
    assert players_response[0].player_id == 2009


def test_get_player_by_id():
    """Tests get player by ID from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    player_response = client.get_player_by_id(2009)

    assert isinstance(player_response, Player)
    assert player_response.first_name == "Bryce"       

#scoring endpoints
def test_list_performances():
    """Tests get peformances from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    performances_response = client.list_performances(skip=0,limit=20000)


    # Assert the list is not empty
    assert isinstance(performances_response, list)
    # Assert each item in the list is an instance of League
    for performance in performances_response:
        assert isinstance(performance, Performance)
    assert len(performances_response) == 17306


#test /v0/performances/ with changed date
def test_list_performances_by_date():
    """Tests get peformances from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    performances_response = client.list_performances(skip=0,limit=3000,minimum_last_changed_date="2024-04-01")

    # Assert the list is not empty
    assert isinstance(performances_response, list)
    # Assert each item in the list is an instance of League
    for performance in performances_response:
        assert isinstance(performance, Performance)
    assert len(performances_response) == 2711

def test_bulk_player_file_parquet():
    """Tests bulk player download through SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False, bulk_file_format="parquet")
    client = SWCClient(config)
    player_file_parquet = client.get_bulk_player_file()
    # Assert the file has the correct number of records (including header)
    player_table = pq.read_table(BytesIO(player_file_parquet))
    player_df = player_table.to_pandas()
    assert(len(player_df) == 1018)