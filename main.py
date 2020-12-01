from flask import Flask, render_template, url_for
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')

ROWS_PER_PAGE = 15
PAGES_SHOWN = 5

def get_order(page, old_order, order, direction):
    string = f'/shows/{page}/{order}/'

    if direction == 'ASC' and order == old_order:
        return string + 'DESC'
    elif direction == 'DESC' and order == old_order:
        return string + 'ASC'
    else:
        return string + direction

def print_arrow():
    return '&darr'

@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')

# @app.route('/shows')
# @app.route('/shows/<order>')
# @app.route('/shows/<order>/<direction>')
# @app.route('/shows/<int:page>')
# @app.route('/shows/<int:page>/<order>')
@app.route('/shows/<int:page>/<order>/<direction>')
@app.route('/shows/most-rated')
# @app.route('/shows/most-rated/<order>')
# @app.route('/shows/most-rated/<order>/<direction>')
def most_rated(page=1, order='rating', direction='DESC'):

    number_of_pages = int((queries.get_number_of_shows()['count']) / ROWS_PER_PAGE) + 1
    offset = ROWS_PER_PAGE * page - ROWS_PER_PAGE

    shows_sorted = queries.get_sorted(order, direction, ROWS_PER_PAGE, offset)

    pages_shown_start = int(page - ((PAGES_SHOWN - 1) / 2))
    pages_shown_end = int(page + ((PAGES_SHOWN - 1) / 2))

    if pages_shown_start < 1:
        pages_shown_start = 1
        pages_shown_end = PAGES_SHOWN
    elif pages_shown_end > number_of_pages:
        pages_shown_start = number_of_pages - PAGES_SHOWN + 1
        pages_shown_end = number_of_pages

    return render_template('most_rated.html',
                           shows_sorted=shows_sorted,
                           pages_shown_start=pages_shown_start,
                           pages_shown_end=pages_shown_end,
                           page=page,
                           number_of_pages=number_of_pages,
                           direction=direction,
                           order=order,
                           get_order=get_order,
                           print_arrow=print_arrow)

@app.route('/show/<int:id>')
def shows_id(id):

# TODO get ready int from queries
    show_detailed = queries.get_detailed(id)
    runtime_formatted = divmod(show_detailed[0]['runtime'], 60)
    if runtime_formatted[0] < 1:
        runtime_formatted = f"{runtime_formatted[1]}min"
    elif runtime_formatted[1] < 1:
        runtime_formatted = f"{runtime_formatted[0]}h"
    else:
        runtime_formatted = f"{runtime_formatted[0]}h {runtime_formatted[1]}min"

    actors_raw = queries.get_actors(id)
    actors = []
    for actor in actors_raw:
        if len(actors) < 2:
            actors.append(actor['name'] + ', ')
        else:
            actors.append(actor['name'])

    seasons = queries.get_seasons(id)
    for season in seasons:
        print(season)


    return render_template('shows_id.html', show_detailed=show_detailed,
                           runtime_formatted=runtime_formatted,
                           actors=actors,
                           seasons=seasons)

def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
