"""
    Testing decorators
        DumpArgs dumps all arguments to default display
"""
from __future__ import absolute_import, print_function


def DumpArgs(func):  # pylint: disable=invalid-name
    """Decorator to print function call details.
       parameters names and effective values.

       example:
         @DumpArgs
         def myfunct(a, b, c='arg')
    """
    def wrapper(*func_args, **func_kwargs):
        """Wrapper function for the decorator. """

        arg_names = func.func_code.co_varnames[:func.func_code.co_argcount]
        args = func_args[:len(arg_names)]
        defaults = func.func_defaults or ()
        args = args + defaults[len(defaults) - (func.func_code.co_argcount -
                                                len(args)):]
        params = zip(arg_names, args)
        args = func_args[len(arg_names):]
        if args:
            params.append(('args', args))
        if func_kwargs:
            params.append(('kwargs', func_kwargs))

        print('%s (%s )' % (func.func_name,
                            ', '.join('%s = %r' % p for p in params)))
        return func(*func_args, **func_kwargs)
    return wrapper
