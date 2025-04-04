import json

from python_fix_explainer import test_all, generate_correction

import logging
logging.basicConfig(level=logging.INFO)


# ~~~~~~ Problem/solution defintion ~~~~~~

output_name = 'ant_elif_1move'

correct_solutions = [
    '''
for i in range(10):
    if is_yellow():
        paint_blue()
        turn_left()
    elif is_blue():
        erase()
        turn_right()
    else:
        paint_yellow()
        turn_right()
    move_forward()
''',
'''
for i in range(10):
    if is_yellow():
        paint_blue()
        turn_left()
        move_forward()
    elif is_blue():
        erase()
        turn_right()
        move_forward()
    else:
        paint_yellow()
        turn_right()
        move_forward()
'''
]

unit_tests = [
    'field_as_str() == expected_field'
]

student_solution = '''
for i in range(10):
    if is_yellow():
        paint_blue()
        turn_left()
    if is_blue():
        erase()
        turn_right()
    else:
        paint_yellow()
        turn_right()
    move_forward()
'''

prepend_code = """
directional_moves = [
    (0, -1),  # 0 = Up
    (1, 0),   # 1 = Right
    (0, 1),   # 2 = Down
    (-1, 0)   # 3 = Left
]


# 20x20 field
field = [['.']*20 for _ in range(20)]


def field_as_str():
    rows = []
    for y in range(len(field[0])):
        row = ''.join([field[x][y] for x in range(len(field))])
        rows.append(row)
    return '\\n'.join(rows)


ant_x = 10
ant_y = 10
ant_direction = 1  # Right


def erase():
    field[ant_x][ant_y] = '.'
    return {'painted': '.'}


def paint_blue():
    field[ant_x][ant_y] = 'b'
    return {'painted': 'b'}


def paint_yellow():
    field[ant_x][ant_y] = 'y'
    return {'painted': 'y'}


def is_clear():
    return field[ant_x][ant_y] == '.'


def is_blue():
    return field[ant_x][ant_y] == 'b'


def is_yellow():
    return field[ant_x][ant_y] == 'y'


def move_forward():
    global ant_x, ant_y
    move_x, move_y = directional_moves[ant_direction]
    ant_x = (ant_x + move_x) % 20
    ant_y = (ant_y + move_y) % 20
    return {
        'x': ant_x,
        'y': ant_y,
        'dir': ant_direction
    }


def turn_right():
    global ant_direction
    ant_direction = (ant_direction + 1) % 4
    return {
        'x': ant_x,
        'y': ant_y,
        'dir': ant_direction
    }


def turn_left():
    global ant_direction
    ant_direction = (ant_direction + 3) % 4  # under modulo 4, +3 is same as -1, but ensures it's positive.
    return {
        'x': ant_x,
        'y': ant_y,
        'dir': ant_direction
    }

expected_field = '''
....................
....................
....................
....................
....................
....................
....................
....................
....................
..........by........
.........y.y........
.........yy.........
....................
....................
....................
....................
....................
....................
....................
....................
'''.strip()

"""

append_code = '''
'''

# ~~~~~~ bits of HTML to use in the output ~~~~~~

html_header = '''
<head>
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.13.2/themes/base/jquery-ui.css">
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://code.jquery.com/ui/1.13.2/jquery-ui.js"></script>
    <script type="text/javascript" src="fixes.js"></script>
    <link rel="stylesheet" type="text/css" href="fixes.css">
</head>
<body>
'''

html_footer = '''
</body>
'''

# ~~~~~~ test solutions and generate output if everything is in order ~~~~~~

solution_test_results = test_all(correct_solutions, unit_tests, prepend_code=prepend_code, append_code=append_code)

if not all([all(st) for st in solution_test_results]):
    print('Not all solutions pass unit tests!')
else:
    # wrap student solution in a list since test_all takes a list of solutions
    student_test_result = test_all([student_solution], unit_tests,
                                   prepend_code=prepend_code, append_code=append_code)[0]
    if all(student_test_result):
        print(student_test_result)
        print('Student solution passes unit tests!')
    else:
        correction_data = generate_correction(incorrect_code=student_solution,
                                              problem_unit_tests=unit_tests,
                                              correct_versions=correct_solutions,
                                              prepend_code=prepend_code,
                                              append_code=append_code)

        with open(f'json/{output_name}.json', 'w') as out_json:
            json.dump(correction_data, out_json, indent=2)

        with open(f'html/{output_name}.html', 'w') as html_out:
            html_out.write(html_header)
            html_out.write('<div class="code-block side-by-side before" id="before_block"><pre>' +
                           correction_data['source'] + '</pre></div>')
            html_out.write('<div class="code-block side-by-side after" id="after_block"><pre>' +
                           correction_data['dest'] + '</pre></div>')
            rest_of_output = {k: v for (k, v) in correction_data.items() if k not in ['source', 'dest']}
            html_out.write(f'''
    <script>
      correction_data={json.dumps(rest_of_output, indent=2)}
    </script>
                    ''')
            html_out.write(html_footer)
