import sys, os
# from cookiecutter.main import cookiecutter

try:
	input
except:
	input = raw_input

def check_path(python_interpreter):
	if python_interpreter == "python" or python_interpreter == "python3":
		pass
	elif os.path.isfile(python_interpreter):
		pass
	else:
		raise ValueError("Python interpreter not exist.")
		sys.exit(1)

def get_venv_interpreter(replace_keyword="current_venv", py_path=sys.executable):
	path = os.path.join(os.getcwd(), "Makefile")
	with open(path, 'r') as file:
		mkfile = file.read()
	
	if replace_keyword in mkfile:
		mkfile = mkfile.replace(replace_keyword, py_path)
	
		with open(path, 'w') as file:
			file.write(mkfile)

context = {{cookiecutter}}
context['user_name']=os.getlogin()
python_interpreter = context['python_interpreter']
if python_interpreter == "current_venv":
	get_venv_interpreter()
elif python_interpreter == "other_path":
	py_path = input("Please enter the path to the interpreter (e.g. /Anaconda/env/bm_learn/bin/python)\n>> ").lower()
	check_path(py_path)
	get_venv_interpreter(python_interpreter, py_path)
