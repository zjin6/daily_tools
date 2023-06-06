### import the module, then invoke this function

from inspect import getmembers, isfunction, signature, getargspec, getmodule

def whatfun(module):
    fun_list = getmembers(module, isfunction)
    print(str(len(fun_list)) + ' functions' + '-' * 40)
    for fun_name, func in fun_list:
        print(fun_name + str(signature(func)))



# for example:
# import fileoperA0
# whatfun(fileoperA0)