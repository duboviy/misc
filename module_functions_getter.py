import operator
import inspect


def get_module_functions(module, function_prefix=''):
    
    def filter_function(inspected_function):
        function_name, function = inspected_function
        if (function_name.startswith(function_prefix) and
            inspect.getmodule(function) == module):
            return True

    funcs = map(operator.itemgetter(1),
                        filter(filter_function,
                               inspect.getmembers(module, inspect.isfunction)))
    return funcs
