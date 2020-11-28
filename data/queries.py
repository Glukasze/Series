from data import data_manager
from psycopg2 import sql

def get_number_of_rows():
    return data_manager.execute_select('SELECT COUNT(*) FROM shows')

def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')

def get_15_best(offset):
    return data_manager.execute_select(sql.SQL("""SELECT shows.id, shows.title, shows.year, ROUND(rating,1), shows.runtime,
                                        CASE
                                        WHEN shows.homepage is NULL THEN 'No URL'
                                        ELSE shows.homepage
                                        END,
                                        CASE
                                        WHEN shows.trailer is NULL THEN 'No URL'
                                        ELSE shows.trailer
                                        END,
                                        STRING_AGG (genres.name, ', ' ORDER BY name) genres
                                        FROM show_genres
                                        JOIN shows
                                        ON show_id = shows.id
                                        JOIN genres
                                        ON genre_id = genres.id
                                        GROUP BY shows.id, shows.title, shows.rating, shows.homepage, shows.trailer, shows.runtime, shows.year
                                        ORDER BY rating DESC LIMIT 15 OFFSET {};""").format(sql.Literal(offset)))
