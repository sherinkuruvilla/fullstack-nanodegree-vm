-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop database tournament;

create database tournament;

\c tournament;

drop table if exists players cascade;

create table players(
  name text,
  id serial PRIMARY KEY
);

drop table if exists matches cascade;

create table matches (
  winner_id integer REFERENCES players(id),
  loser_id integer REFERENCES players(id),
   PRIMARY KEY (winner_id, loser_id)
);


-- INITIAL BASE VIEW created to keep track of player, number of wins and losses.
create or replace view score
as
  select
  id,
  name,
  coalesce(wins,0) wins,
  coalesce(losses,0) losses
from
  players
  left join (select winner_id, count(*) wins from matches group by winner_id) win
    on players.id = win.winner_id
  left join  (select loser_id, count(*) losses from matches group by loser_id) loss
    on players.id = loss.loser_id;


-- VIEW built on top of score VIEW.
-- Using score, calculate opponent score to break a tie.
create or replace view opp_score
as
  select
  winner_id as id,
  round(avg(wins),2) opp_wins
from
  matches
  left join score
    on matches.loser_id=score.id
group by
  winner_id;

-- VIEW to provide player_standings
-- All players from table show their wins, losses and opponent score
-- Player standing is decided by ordering by wins and then by opponent's average wins.
-- This ensures that those with a tie will break tie when they have beaten a
-- stronger opponent than the other on average
create or replace view player_standings
as
  select
  players.id,
  players.name,
  wins+losses as matches,
  wins,
  opp_wins
from
  players
  left join score
    on players.id = score.id
  left join opp_score
    on players.id = opp_score.id
order by
  wins desc, opp_wins desc;

--VIEW to determine pairing based on top scores
--The base view is player_standings sorted by wins desc and tie breaker scores
--The partner view is essentially the same as base view but offset by 1
--This is to ensure that if id1, id2, id3 and id4 are as per player_standing,
--the partner view will show id2, id3 and id4 with matching row number as first view.
--once joined on matching row numbers, and skipping alternate rows
-- we will ensure we will get id1 and id2 paired etc.
create view swiss_ranking
as
  select
  id,
  name,
  partner_id,
  partner_name
from
  (select id, name, row_number() over (order by wins desc, opp_wins desc) rank
    from player_standings) player
  left join (select id  partner_id, name partner_name, row_number() over (order by wins desc, opp_wins desc)-1 rank
              from player_standings  offset 1) partner
                on player.rank=partner.rank
where player.rank % 2=1;










