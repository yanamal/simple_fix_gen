import json

from python_fix_explainer import test_all, generate_correction


# ~~~~~~ Problem/solution defintion ~~~~~~

output_name = 'helloWorld'

correct_solutions = [
    '''
def helloWorld():
    return "Hello World!"
    '''
]

unit_tests = [
    'helloWorld() == "Hello World!"'
]

student_solution = '''
def helloWorld():
    print("Hello World!") 
'''

prepend_code = '''
'''

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
