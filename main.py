from flask import Flask, render_template, url_for, request, redirect, jsonify
from data import queries
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')

ROWS_PER_PAGE = 15
PAGES_SHOWN = 5

# setting correct order for sorting to avoid logical expressions in HTML
def get_order(page, old_order, order, direction):
    string = f'/shows/{page}/{order}/'

    if direction == 'ASC' and order == old_order:
        return string + 'DESC'
    elif direction == 'DESC' and order == old_order:
        return string + 'ASC'
    else:
        return string + direction

# welcome page
@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)

# dummy page with the default layout
@app.route('/design')
def design():
    return render_template('design.html')

# def find_movies(shows_all, selected_rating):
#     result = []
#     for item in shows_all:
#         if str(item['round']) == selected_rating:
#             result.append(item)
#     return result

#JSON routes

@app.route('/by_actor/<show>')
def by_actor(show):

    show = "%" + show + "%"
    selected = queries.get_actors_by_show(show)
    return jsonify(selected)

@app.route('/by_rating/<rating>')
def by_rating(rating):
    selected = queries.get_names_by_rating(rating)
    return jsonify(selected)

@app.route('/data/testing/<show>')
def data_testing(show):
    show = '%' + show + '%'
    selected = queries.get_actors_by_show(show)
    return jsonify(selected)



# main page with sorting

# @app.route('/shows')
# @app.route('/shows/<order>')
# @app.route('/shows/<order>/<direction>')
# @app.route('/shows/<int:page>')
# @app.route('/shows/<int:page>/<order>')
@app.route('/shows/<int:page>/<order>/<direction>')
@app.route('/shows/most-rated', methods=['POST', 'GET'])
# @app.route('/shows/most-rated/<order>')
# @app.route('/shows/most-rated/<order>/<direction>')
def most_rated(page=1, order='rating', direction='DESC'):


    number_of_pages = int((queries.get_number_of_shows()['count']) / ROWS_PER_PAGE) + 1
    offset = ROWS_PER_PAGE * page - ROWS_PER_PAGE

    # ready sql data
    shows_sorted = queries.get_sorted(order, direction, ROWS_PER_PAGE, offset)

    # pagination
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
                           get_order=get_order)

# page with detailed view on a given show
@app.route('/show/<int:show_id>')
def shows_id(show_id):

    # ready sql data
    show_detailed = queries.get_detailed(show_id)
    print(show_detailed)

    # formatting runtime to show hours and minutes if >60 and only minutes if <60
    runtime_formatted = divmod(show_detailed[0]['runtime'], 60)
    if runtime_formatted[0] < 1:
        runtime_formatted = f"{runtime_formatted[1]}min"
    elif runtime_formatted[1] < 1:
        runtime_formatted = f"{runtime_formatted[0]}h"
    else:
        runtime_formatted = f"{runtime_formatted[0]}h {runtime_formatted[1]}min"

    # preparing 3 top actors
    actors_raw = queries.get_actors_by_show_id(show_id)
    actors = []
    for actor in actors_raw:
        if len(actors) < 2:
            actors.append(actor['name'] + ', ')
        else:
            actors.append(actor['name'])

    seasons = queries.get_seasons(show_id)
    for season in seasons:
        print(season)


    return render_template('shows_id.html', show_detailed=show_detailed,
                           runtime_formatted=runtime_formatted,
                           actors=actors,
                           seasons=seasons)

# page for testing
@app.route('/testing')
def testing():

    episode = queries.get_game()

    return render_template('testing.html', episode=episode)


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
