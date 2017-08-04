import sqlite3
from bottle import route, run, debug, template, request, static_file, error

@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()
    return template('make_table', rows=result)

@route('/new')
def form_new_item():
    return template('new_task.tpl')

@route('/new', method='POST')
def new_item():
    new = request.POST.task.strip()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
    new_id = c.lastrowid
    conn.commit()
    c.close()
    return """<p>The new task was inserted into the database, the ID is {}</p>
            <a href="/todo">back to list</a>""".format(str(new_id))

@route('/edit/<no:int>')
def form_edit_item(no):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
    cur_data = c.fetchone()
    c.close()
    return template('edit_task', old=cur_data, no=no)

@route('/edit/<no:int>', method='POST')
def edit_item(no):
    edit = request.POST.task.strip()
    status = request.POST.status.strip()
    if status == 'open':
        status = 1
    else:
        status = 0
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, str(no)))
    conn.commit()
    c.close()
    return """<p>The item number {} was successfully updated</p>
            <a href="/todo">back to list</a>""".format(str(no))

@route('/item<item:re:[0-9]+>')
def show_item(item):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(item)))
    result = c.fetchone()
    c.close()
    if not result:
        return """<p>This item number does not exist!</p>
                <a href="/todo">back to list</a>"""
    else:
        return """<p>Task: {}</p>
                <a href="/todo">back to list</a>""".format(str(result))

@route('/help')
def help():
    return static_file('help.html', root='./static')

@route('/json<json:re:[0-9]+>')
def show_json(json):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(json)))
    result = c.fetchone()
    c.close()
    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result}

@error(404)
def mistake(code):
    return 'Nothing to show!'

run(host='localhost', port=8080, debug=True, reloader=True)
