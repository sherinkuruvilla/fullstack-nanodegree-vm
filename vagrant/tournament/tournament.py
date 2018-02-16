#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament user=postgres password=sherin")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players;")
    playercount = c.fetchall()[0][0]
    db.close()
    return playercount


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players values(%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or aplayer
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

    All players from table show their wins, losses and opponent score
    Player standing is decided by ordering by wins and then by opponent's
    average wins.
    This ensures that those with a tie will break tie when they have beaten a
    stronger opponent than the other on average
    """
    db = connect()
    c = db.cursor()
    c.execute("""
            select id, name, wins, matches from
            player_standings order by wins desc, opp_wins desc;""")
    player_standings = c.fetchall()
    db.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches values(%s, %s)", (winner, loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    """
    The base view is player_standings sorted by wins desc & tiebreaker scores
    The partner view is essentially the same as base view but offset by 1
    This is to ensure that if id1, id2, id3 and id4 are as per player_standing,
    the partner view will show id2, id3 and id4 with matching row number
    as first view.
    once joined on matching row numbers, and skipping alternate rows
    we will ensure we will get id1 and id2 paired etc.
    """
    db = connect()
    c = db.cursor()
    c.execute("""
            select id, name, partner_id, partner_name from
            swiss_ranking;""")
    swiss_ranking = c.fetchall()
    db.close()
    return swiss_ranking
