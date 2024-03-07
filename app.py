from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def query_database(query, parameters=()):
    conn = sqlite3.connect('ip_port_database.db')
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchall()
    conn.close()
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leasesets')
def leasesets(max_limit = 100):
    # Получаем данные для списка лизсетов
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    if limit > max_limit: limit = max_limit

    # Вычисляем общее количество лизсетов
    total_lease_sets = query_database("SELECT COUNT(*) FROM lease_sets")[0][0]

    # Ограничиваем offset, чтобы не превышать общее количество
    offset = min(offset, total_lease_sets - limit)

    lease_sets = query_database("SELECT * FROM lease_sets LIMIT ? OFFSET ?", (limit, offset))

    return render_template('leasesets.html', lease_sets=lease_sets, offset=offset, limit=limit, total_lease_sets=total_lease_sets)
@app.route('/search', methods=['GET', 'POST'])
def search(max_limit=100):
    offset = int(request.form.get('offset', request.args.get('offset', 0)))
    limit = int(request.args.get('limit', 10))
    if request.method == 'POST':
        search_term = request.form.get('search_term', request.form.get('prev_search_term'))
        offset = int(request.form.get('offset', 0))

        if limit > max_limit:
            limit = max_limit

        # Получаем общее количество результатов поиска
        total_search_results = query_database("SELECT COUNT(*) FROM ip_port_data WHERE city LIKE ? OR country LIKE ? OR ip LIKE ?", ('%' + search_term + '%', '%' + search_term + '%', '%' + ''.join(filter(str.isdigit, search_term)) + '%'))[0][0]

        # Выполняем поиск в базе данных
        search_result = query_database("SELECT * FROM ip_port_data WHERE city LIKE ? OR country LIKE ? OR ip LIKE ? LIMIT ? OFFSET ?", ('%' + search_term + '%', '%' + search_term + '%', '%' + ''.join(filter(str.isdigit, search_term)) + '%', limit, offset))

        return render_template('search_results.html', search_result=search_result, offset=offset, limit=limit, total_search_results=total_search_results, search_term=search_term)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)

