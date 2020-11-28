from flask import Flask, render_template, url_for
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')

@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/shows/<int:page>')
@app.route('/shows/most-rated')
def most_rated(page=False):
    ROWS_PER_PAGE = 15
    INITIAL_ROWS = 15
    offset = 0
    number_of_pages = int((queries.get_number_of_rows()[0]['count'] - INITIAL_ROWS) / ROWS_PER_PAGE)
    if page != False:
        offset = ROWS_PER_PAGE * page - INITIAL_ROWS

    shows_15_best = queries.get_15_best(offset)

    return render_template('most_rated.html', shows_15_best=shows_15_best, number_of_pages=number_of_pages, page=page)

@app.route('/show/<id>')
def shows_id(id):

    return render_template('shows_id.html', id=id)

def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
