import atexit
from sqlite3 import connect, OperationalError
from flask import (
    abort,
    Flask,
    jsonify,
    request,
    render_template
)

from .queries import (
    ALL_LINKS,
    INSERT_LINK,
    DELETE_LINKS,
    ALL_EMPLOYEES,
    INSERT_EMPLOYEE,
    DELETE_EMPLOYEE
)

app = Flask(__name__)
db = 'chart.sqlite'
conn = connect(db)
cursor = conn.cursor()
atexit.register(conn.close)


try:
    cursor.execute('create table employees (employee)')
    cursor.execute('create table links (boss TEXT, employee TEXT)')
except OperationalError:
    print('Tables exists')


def employees_for_add(line, branch):
    line_set = set(line.split(','))
    branch_set = set(branch.split(','))
    diff = branch_set.difference(line_set)
    return ','.join(diff)


@app.route('/api/orgchart/new', methods=['POST'])
def make_new_chart():
    cursor.execute('drop table links')
    cursor.execute('drop table employees')
    cursor.execute('create table employees (employee)')
    cursor.execute('create table links (boss, employee)')
    return 'OK!'


@app.route('/api/orgchart/add', methods=['POST'])
def add_to_chart():
    try:
        boss_id = request.form['boss_id']
        employees = [(employee,) for employee in request.form['employees'].split(',')]
        links = [(boss_id, employee[0],) for employee in employees]
        employees.append((boss_id,))
        cursor.executemany(INSERT_LINK, links)
        cursor.executemany(INSERT_EMPLOYEE, employees)
        conn.commit()
        return 'OK!'
    except OperationalError:
        abort(500)


@app.route('/api/orgchart/<boss_id>')
def del_from_chart(boss_id):
    try:
        cursor.execute(DELETE_LINKS, (boss_id,))
        cursor.execute(DELETE_EMPLOYEE, (boss_id,))
        conn.commit()
        return 'OK!'
    except OperationalError:
        abort(500)


@app.route('/api/orgchart')
def get_chart():
    try:
        cursor.execute(ALL_LINKS)
        links = [{'from': row[0], 'to': row[1]} for row in cursor.fetchall()]
        cursor.execute(ALL_EMPLOYEES)
        employees = [{'key': row[0], 'color': '#CCC'} for row in set(cursor.fetchall())]

        return jsonify({
            'links': links,
            'employees': employees,
        })
    except OperationalError:
        abort(500)


@app.route('/test')
def test():
    cursor.execute(ALL_LINKS)
    links = cursor.fetchall()
    cursor.execute(ALL_EMPLOYEES)
    employees = cursor.fetchall()

    return jsonify({'links': links, 'employees': employees})


@app.route('/')
def display_chart():
    return render_template('index.html')
