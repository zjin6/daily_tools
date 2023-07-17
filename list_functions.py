import inspect
import importlib


module_name = input('module name: ')

def get_functions(module_name):
    # Import the module dynamically
    module = importlib.import_module(module_name)

    # Get all the members of the module
    members = inspect.getmembers(module)

    # Filter only the functions defined in the module
    functions = []
    for member_name, member in members:
        if inspect.isfunction(member) and member_name[0] != '_':
            # Check if the function is decorated
            is_decorated = False
            for obj in inspect.getmembers(module):
                if obj[0] == member_name:
                    if hasattr(obj[1], '__wrapped__'):
                        is_decorated = True
                        break
            if is_decorated:
                functions.append(member.__name__)
            else:
                functions.append(member_name)

    # Return the list of functions
    return functions




functions = get_functions(module_name)
for fun_name in functions:
    print(fun_name)
    

