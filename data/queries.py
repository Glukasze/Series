from data import data_manager
from psycopg2 import sql

def get_number_of_shows():
    return data_manager.execute_select('SELECT COUNT(*) FROM shows')[0]

def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')

def get_sorted(order, direction, limit, offset):
    return data_manager.execute_select(sql.SQL("""
    SELECT shows.id, shows.title, shows.year,
    ROUND(rating,1), shows.runtime,
                                        CASE
                                        WHEN shows.homepage is NULL THEN 'No URL'
                                        ELSE shows.homepage
                                        END,
                                        CASE
                                        WHEN shows.trailer is NULL THEN 'No URL'
                                        ELSE shows.trailer
                                        END,
                                        STRING_AGG (genres.name, ', ' ORDER BY name) genres
                                        FROM shows
                                        LEFT JOIN show_genres
                                        ON show_id = shows.id
                                        LEFT JOIN genres
                                        ON genre_id = genres.id
                                        GROUP BY shows.id, shows.title, shows.rating, shows.homepage,
                                        shows.trailer,shows.runtime, shows.year
                                        ORDER BY 
                                        CASE WHEN %(direction)s = 'ASC' THEN {order} END ASC,
                                        CASE WHEN %(direction)s = 'DESC' THEN {order} END DESC
                                        LIMIT {limit} OFFSET {offset};"""
                                               ).format(order = sql.Identifier(order),
                                                        limit = sql.Literal(limit),
                                                        offset = sql.Literal(offset)), {'direction':direction})

def get_detailed(id):
    return data_manager.execute_select(sql.SQL("""
    SELECT shows.title, shows.runtime, ROUND(shows.rating, 1),
    STRING_AGG(genres.name, ', ' ORDER BY name) genres, shows.overview, shows.trailer
    FROM shows
    LEFT JOIN show_genres
    ON shows.id = show_genres.show_id
    LEFT JOIN genres
    ON genres.id = show_genres.genre_id
    WHERE shows.id = {id}
    GROUP BY shows.title, shows.runtime, shows.rating, shows.overview, shows.trailer;""").format(id = sql.Literal(id)))

def get_actors(id):
    return data_manager.execute_select(sql.SQL("""
    SELECT actors.name FROM actors
    LEFT JOIN show_characters
    ON actors.id = show_characters.actor_id
    LEFT JOIN shows
    ON show_characters.show_id = shows.id
    WHERE shows.id = {id}
    LIMIT 3;""").format(id = sql.Literal(id)))

def get_seasons(id):
    return data_manager.execute_select(sql.SQL("""
    SELECT seasons.season_number, seasons.title, seasons.overview
    FROM seasons
    LEFT JOIN shows
    ON seasons.show_id = shows.id
    WHERE shows.id = {id};""").format(id = sql.Literal(id)))