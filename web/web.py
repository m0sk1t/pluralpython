import atexit
from sqlite3 import connect, OperationalError
from flask import Flask, jsonify, request, render_template
from .queries import ALL, EXISTS, DELETE_ROW, INSERT_EMPLOYEES, UPDATE_EMPLOYEES

app = Flask(__name__)
db = 'chart.sqlite'
conn = connect(db)
cursor = conn.cursor()
atexit.register(conn.close)


def employees_for_add(line, branch):
    line_set = set(line.split(','))
    branch_set = set(branch.split(','))
    diff = branch_set.difference(line_set)
    return ','.join(diff)


@app.route('/api/orgchart/new', methods=['POST'])
def make_new_chart():
    try:
        cursor.execute('drop table chart')
        cursor.execute('create table chart (boss, employees)')
    except OperationalError:
        cursor.execute('create table chart (boss, employees)')
    return 'OK!'


@app.route('/api/orgchart/add', methods=['POST'])
def add_to_chart():
    boss_id = request.form['boss_id']
    employees = request.form['employees']
    cursor.execute(EXISTS, (boss_id,))
    row = cursor.fetchone()
    if row:
        computed_employees = row[1] + ',' + employees_for_add(row[1], employees)
        cursor.execute(UPDATE_EMPLOYEES, (computed_employees, boss_id,))
    else:
        cursor.execute(INSERT_EMPLOYEES, (boss_id, employees,))
    conn.commit()
    return 'OK!'


@app.route('/api/orgchart/<boss_id>')
def del_from_chart(boss_id):
    cursor.execute(DELETE_ROW, (boss_id,))
    conn.commit()
    return 'OK!'


@app.route('/api/orgchart')
def get_chart():
    cursor.execute(ALL)
    links = []
    employees = []
    for row in cursor.fetchall():
        boss, employees_str = row
        employees.append(boss)

        for employee in employees_str.split(','):
            employees.append(employee)
            links.append({'from': boss, 'to': employee})
    employees = [{'key': employee, 'color': str('#' + (employee * 3)[:6])} for employee in set(employees)]

    return jsonify({
        'links': links,
        'employees': employees,
    })


@app.route('/test')
def test():
    cursor.execute(ALL)
    return jsonify({'test': cursor.fetchall()})


@app.route('/')
def display_chart():
    return render_template('index.html')
