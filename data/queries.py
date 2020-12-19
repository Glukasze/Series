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

def get_detailed(show_id):
    return data_manager.execute_select(sql.SQL("""
    SELECT shows.title, shows.runtime, ROUND(shows.rating, 1),
    STRING_AGG(genres.name, ', ' ORDER BY name) genres, shows.overview, shows.trailer
    FROM shows
    LEFT JOIN show_genres
    ON shows.id = show_genres.show_id
    LEFT JOIN genres
    ON genres.id = show_genres.genre_id
    WHERE shows.id = {show_id}
    GROUP BY shows.title, shows.runtime, shows.rating, shows.overview, shows.trailer;""").format(show_id = sql.Literal(show_id)))

def get_actors_by_show_id(show_id):
    return data_manager.execute_select(sql.SQL("""
    SELECT actors.name FROM actors
    LEFT JOIN show_characters
    ON actors.id = show_characters.actor_id
    LEFT JOIN shows
    ON show_characters.show_id = shows.id
    WHERE shows.id = {show_id}
    LIMIT 3;""").format(show_id = sql.Literal(show_id)))

def get_seasons(id):
    return data_manager.execute_select(sql.SQL("""
    SELECT seasons.season_number, seasons.title, seasons.overview
    FROM seasons
    LEFT JOIN shows
    ON seasons.show_id = shows.id
    WHERE shows.id = {id};""").format(id = sql.Literal(id)))

def get_names_by_rating(rating):
    return data_manager.execute_select(sql.SQL("""
    SELECT title
    FROM shows
    WHERE ROUND(rating, 1) = {rating}""").format(rating = sql.Literal(rating)))

def get_characters_by_actor(actor):
    return data_manager.execute_select(sql.SQL("""
    SELECT actors.name, show_characters.character_name, shows.title, TO_CHAR(shows.year, 'YYYY')
    FROM actors
    LEFT JOIN show_characters
    ON actors.id = show_characters.actor_id
    LEFT JOIN shows
    ON show_characters.show_id = shows.id
    WHERE LOWER(actors.name) LIKE LOWER({actor})
    ORDER BY actors.name""").format(actor = sql.Literal(actor)))

def get_genres_and_actors():
    return data_manager.execute_select(sql.SQL("""
    SELECT actors.id, actors.name, STRING_AGG(DISTINCT genres.name, ', ' ORDER BY genres.name) genres
    FROM actors
    LEFT JOIN show_characters ON actors.id = show_characters.actor_id
    LEFT JOIN shows ON show_characters.show_id = shows.id
    LEFT JOIN show_genres ON shows.id = show_genres.show_id
    LEFT JOIN genres ON show_genres.genre_id = genres.id
    GROUP BY actors.id"""))

def get_genres_by_actors(actor):
    return data_manager.execute_select(sql.SQL("""
    SELECT actors.id, actors.name, STRING_AGG(DISTINCT genres.name, ', ' ORDER BY genres.name) genres
    FROM actors
    LEFT JOIN show_characters ON actors.id = show_characters.actor_id
    LEFT JOIN shows ON show_characters.show_id = shows.id
    LEFT JOIN show_genres ON shows.id = show_genres.show_id
    LEFT JOIN genres ON show_genres.genre_id = genres.id
    WHERE LOWER(actors.name) LIKE LOWER({actor})
    GROUP BY actors.id""").format(actor=sql.Literal(actor)))

def get_actors_by_show(show):
    return data_manager.execute_select(sql.SQL("""
    SELECT actors.name, show_characters.character_name, shows.title
    FROM actors
    LEFT JOIN show_characters ON actors.id = show_characters.actor_id
    LEFT JOIN shows ON show_characters.show_id = shows.id
    WHERE LOWER(shows.title) LIKE LOWER({show})
    GROUP BY actors.name, show_characters.character_name, shows.title""").format(show=sql.Literal(show)))

def get_game():
    return data_manager.execute_select(sql.SQL("""
    SELECT episodes.episode_number, episodes.title
    FROM episodes
    WHERE episodes.id = 73630"""))