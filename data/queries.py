from data import data_manager
from psycopg2 import sql

def get_number_of_rows():
    return data_manager.execute_select('SELECT COUNT(*) FROM shows')

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
