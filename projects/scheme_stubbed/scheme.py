"""A Scheme interpreter and its read-eval-print loop."""

import sys
import os

from scheme_builtins import *
from scheme_reader import *
from ucb import main, trace


##############
# Eval/Apply #
##############

SPECIAL_FORMS = {'define', 'quote', 'begin', 'lambda', 'if', 'cond', 'and', 'or', 'let', 'mu', 'define-macro'}

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in environment ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # PROBLEM 2
    if slef_evaluate(expr):             # base case 1
        return expr
    if isinstance(expr, str):       # base case 2
        return env.get_symbol(expr)
    if isinstance(expr, Pair):
        if isinstance(expr.first, str) and expr.first in SPECIAL_FORMS:     # if special form
            return scheme_spform(expr.first, expr.rest, env)
        operator = scheme_eval(expr.first, env)
        if isinstance(operator, MacroProcedure):
            return scheme_apply(operator, expr.rest, env)
        return scheme_apply(operator, expr.rest.map(lambda x: scheme_eval(x, env)), env)
    raise SchemeError(f'expr: {expr}, env: {env}')

def slef_evaluate(expr):
    """If the value of evaluating the expresion EXPR is itself."""
    return isinstance(expr, int) or isinstance(expr, float) or \
           isinstance(expr, bool) or expr is nil or expr is None


def scheme_spform(keyword, expr, env):
    """Deal with the special form in the scheme"""
    if keyword == 'define':
        if len(expr) < 2:
            raise SchemeError
        return scheme_define(expr, env)
    if keyword == 'quote':
        if len(expr) != 1:
            raise SyntaxError
        return expr.first
    if keyword == 'begin':
        if len(expr) == 0:
            raise SyntaxError
        return eval_all(expr, env)
    if keyword == 'lambda':
        if len(expr) > 1 and valid_formal(expr.first):
            return LambdaProcedure(expr.first, expr.rest, env)
        raise SchemeError
    if keyword == 'if':
        if not (len(expr) == 2 or len(expr) == 3):
            raise SchemeError
        return scheme_if(expr, env)
    if keyword == 'cond':
        if len(expr) == 0:
            raise SchemeError
        return scheme_cond(expr, env)
    if keyword == 'and':
        if len(expr) == 0:
            return True
        return scheme_andor(True, expr, env)
    if keyword == 'or':
        if len(expr) == 0:
            return False
        return scheme_andor(False, expr, env)
    if keyword == 'let':
        if len(expr) < 2:
            raise SchemeError
        return scheme_let(expr, env)
    if keyword == 'mu':
        if len(expr) > 1 and valid_formal(expr.first):
            return MuProcedure(expr.first, expr.rest)
        raise SchemeError
    if keyword == 'define-macro':
        first, body = expr.first, expr.rest
        if len(expr) >= 2 and type(first) == Pair and valid_formal(first):
            return env.define(first.first, MacroProcedure(first.rest, body, env))
        raise SchemeError
    raise SyntaxError(f'Forget keyword \'{keyword}\' about the special form in scheme!!!')


def scheme_define(expr, env):
    """Do the special form 'define' in the Scheme
    Assume the expr is the Scheme list"""
    first, body = expr.first, expr.rest
    if type(first) == str:                  # if first is a symbol
        return env.define(first, scheme_eval(body.first, env))
    if type(first) == Pair and type(first.first) == str and valid_formal(first.rest):
        return env.define(first.first, LambdaProcedure(first.rest, body, env))
    raise SchemeError

def eval_all(expr, env):
    """Evaluate all the scheme expression in EXPR with ENV, and return 
    the value of the last expression in EXPR. Assume the expr is not a 
    empty scheme list"""
    if expr.rest is nil:
        return scheme_eval(expr.first, env, True)       # Tail context
    scheme_eval(expr.first, env)
    return eval_all(expr.rest, env)

def scheme_if(expr, env):
    """Do the special form 'if' in the Scheme
    Assume the expr is the Scheme list"""
    predicate, consequent, alter = expr.first, expr.rest.first, expr.rest.rest
    if not is_scheme_false(scheme_eval(predicate, env)):
        return scheme_eval(consequent, env, True)       # Tail context
    elif alter is not nil:
        return scheme_eval(alter.first, env, True)      # Tail context
    return scheme_eval('undefined', env)


def scheme_let(expr, env):
    """Do the special form 'let' in the Scheme
    Assume the expr is the Scheme list."""
    bind = expr.first
    args = unzip_pair(bind)
    formal, arg = args.first, args.rest.first
    while bind is not nil:
        if len(bind.first) != 2:
            raise SchemeError
        bind = bind.rest
    if not valid_formal(formal):
        raise SchemeError
    subframe = env.create_subframe(formal, arg.map(lambda x: scheme_eval(x, env)))
    return scheme_spform('begin', expr.rest, subframe)


def is_instance(value, cls, ept):
    """Test if the value is the instance of the cls, if is, then test whether it's value is ept"""
    return type(value) == cls and value == ept


def scheme_cond(expr, env):
    """Do the special form 'cond' in the Scheme
    Assume the expr is the Scheme list
    
    >>> expr = read_line("(cond ((= 4 3)) ('hi))")
    >>> expr = expr.rest
    >>> scheme_cond(expr, create_global_frame())
    'hi'
    """
    if expr is nil:     # base case 1
        return scheme_eval('undefined', env)
    clause = expr.first
    if expr.rest is nil and is_instance(clause.first, str, 'else'):
        clause.first = True
    test = scheme_eval(clause.first, env)       # eval the value previously
    if not is_scheme_false(test):   # base case 2
        return test if clause.rest is nil else scheme_spform('begin', clause.rest, env)
    return scheme_cond(expr.rest, env)


def is_scheme_false(value):
    """Return whether a value in Scheme is #f. Assume expr is Scheme list.
    In the Scheme, Any expression may be evaluated in a boolean context, 
    but #f is the only value that is false. All other values are treated 
    as true in a boolean context.
    Note: This function only receive Scheme value"""
    return (type(value) == bool) and (value == False)


def scheme_andor(flag, expr, env):
    """Evaluate the value of special from 'and', 'or'
    if the keyword is and, then the flag is True
    if the keyword is or, then the flag is False"""
    if len(expr) == 1:
        return scheme_eval(expr.first, env, True)       # Tail context
    value = scheme_eval(expr.first, env)
    if (not is_scheme_false(value)) == flag:
        return scheme_andor(flag, expr.rest, env)
    return value


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    environment ENV."""
    # PROBLEM 2
    if isinstance(procedure, BuiltinProcedure):
        return procedure.apply(args, env)
    if isinstance(procedure, LambdaProcedure):
        return procedure.apply(args)
    if isinstance(procedure, MuProcedure):
        return procedure.apply(args, env)
    if isinstance(procedure, MacroProcedure):
        return procedure.apply(args, env)
    raise SchemeError(f'scheme_apply error: procedure: {procedure}, procedure_type: {type(procedure)}, \
         {args}, {env}')



################
# Environments #
################

class Frame:
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        "Your Code Here"
        self.parent = parent
        self.bindings = {}
        # Note: you should define instance variables self.parent and self.bindings

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        self.bindings[symbol] = value
        return symbol

    def get_symbol(self, symbol):
        """Return the value of the symbol in the enviroment, search it from 
        down to up
        
        >>> env = create_global_frame()
        >>> sub_env = Frame(env)
        >>> env.define('x', 20)
        'x'
        >>> env.define('y', 40)
        'y'
        >>> sub_env.define('x', 2)
        'x'
        >>> sub_env.get_symbol('x')
        2
        >>> sub_env.get_symbol('y')
        40
        """
        if self.parent is None and symbol not in self.bindings:
            raise SchemeError(f'Unknown identifer {symbol}')    # This Symbol is undefined
        if symbol in self.bindings:             # if this symbol defined in the current env
            return self.bindings[symbol]
        return self.parent.get_symbol(symbol)   # else search it in the parent env

    # BEGIN PROBLEM 2/3
    "*** YOUR CODE HERE ***"
    def create_subframe(self, formals, args):
        """Accroding the formals and args provided to create a subframe.
        Both formals and args are Scheme list"""
        subframe = Frame(self)
        while formals is not nil:
            subframe.define(formals.first, args.first)
            formals, args = formals.rest, args.rest
        return subframe
    # END PROBLEM 2/3

##############
# Procedures #
##############

class Procedure:
    """The supertype of all Scheme procedures."""

def scheme_procedurep(x):
    return isinstance(x, Procedure)

class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, fn, use_env=False, name='builtin'):
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

    def apply(self, args, env):
        """Apply SELF to ARGS in ENV, where ARGS is a Scheme list.

        >>> env = create_global_frame()
        >>> plus = env.bindings['+']
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
        """
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        argv = pair2list(args)
        if self.use_env:        
            argv.append(env)        # whether the function need pass argument env
        try:
            return self.fn(*argv)
        except TypeError:
            raise SchemeError
        # END PROBLEM 2


class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        self.formals = formals
        self.body = body
        self.env = env

    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    def apply(self, args):
        """Apply these args in the function, and return the value

        >>> formals = Pair('x', nil)
        >>> body = Pair(Pair('+', Pair('x', Pair(2, nil))), nil)
        >>> env = create_global_frame()
        >>> add2 = LambdaProcedure(formals, body, env)
        >>> add2.apply(Pair(3, nil))
        5
        >>> add2.apply(Pair(20, nil))
        22
        """
        if len(args) != len(self.formals):
            raise SchemeError
        env = self.env.create_subframe(self.formals, args)
        return scheme_spform('begin', self.body, env)

    # END PROBLEM 3
    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))



class MacroProcedure(Procedure):
    """A Procedure defined by a define-macro expression."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        self.formals = formals
        self.body = body
        self.env = env
    
    def apply(self, args, cur_env):
        """
        >>> define = "(define-macro (for formal iterable body) (list 'map (list 'lambda (list formal) body) iterable))"
        >>> eval =  "(for i '(1 2 3) (if (= i 1) 0 i))"
        >>> env = create_global_frame()
        >>> defines = read_line(define)
        >>> evals = read_line(eval)
        >>> scheme_eval(defines, env)
        for
        >>> scheme_eval(evals, env)
        (0 2 3)
        """
        if len(args) != len(self.formals):
            raise SchemeError(f'MacroProcedure args dismatch, {args}')
        subframe = self.env.create_subframe(self.formals, args)
        temp = scheme_eval(Pair('begin', self.body), subframe)
        return scheme_eval(temp, cur_env)

    def __str__(self):
        return str(Pair('define-macro', Pair(self.formals, self.body)))
    
    def __repr__(self):
        return f'MacroProcedure({repr(self.formals)}, {repr(self.body)}, {repr(self.env)})'

def add_builtins(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as built-in procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, BuiltinProcedure(fn, name=proc_name))

#################
# Special Forms #
#################

"""
How you implement special forms is up to you. We recommend you encapsulate the
logic for each special form separately somehow, which you can do here.
"""

# BEGIN PROBLEM 2/3
"*** YOUR CODE HERE ***"
def valid_formal(formal):
    """Check if the formal is valid, the formal is a Scheme list
    1. The arguments in the formal must be a valid symbol
    2. The arguments in the formal cannot repeat with each other"""
    args = set()
    while formal is not nil:
        if type(formal.first) != str or formal.first in args:
            return False
        args.add(formal.first)
        formal = formal.rest
    return True

def pair2list(pair):
    """Change a pair class instance to a list"""
    lst = []
    while pair is not nil:
        lst.append(pair.first)
        pair = pair.rest
    return lst

def unzip_pair(pair):
    """unzip a pair onject
    
    >>> expr = read_line('((x 2) (y 3) (z 4))')
    >>> str(unzip_pair(expr))
    '((x y z) (2 3 4))'
    >>> expr = read_line('()')
    >>> str(unzip_pair(expr))
    '(() ())'
    """
    if pair is nil:
        return Pair(nil, Pair(nil, nil))
    value, elem = unzip_pair(pair.rest), pair.first
    return Pair(Pair(elem.first, value.first), Pair(Pair(elem.rest.first, value.rest.first), nil))
# END PROBLEM 2/3

# Utility methods for checking the structure of Scheme programs

def validate_form(expr, min, max=float('inf')):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.

    >>> validate_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + repl_str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif length > max:
        raise SchemeError('too many operands in form')

def validate_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of
    formals is not a list of symbols or if any symbol is repeated.

    >>> validate_formals(read_line('(a b c)'))
    """
    symbols = set()
    def validate_and_add(symbol, is_last):
        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        validate_and_add(formals.first, formals.rest is nil)
        formals = formals.rest

    # here for compatibility with DOTS_ARE_CONS
    if formals != nil:
        validate_and_add(formals, True)

def validate_procedure(procedure):
    """Check that PROCEDURE is a valid Scheme procedure."""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), repl_str(procedure)))

#################
# Dynamic Scope #
#################

class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """
    # BEGIN NO PROMPT
    "*** YOUR CODE HERE ***"
    # END NO PROMPT

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    # BEGIN PROBLEM EC
    "*** YOUR CODE HERE ***"
    def apply(self, args, env):
        """Apply these args in the function, and the parent of the environment of the 
        function is current environment

        >>> env = create_global_frame()
        >>> line = read_line("(mu (x) (+ x y))")
        >>> func = scheme_eval(line, env)
        >>> args = read_line("(2)")
        >>> subenv = env.create_subframe(Pair('y', nil), Pair(5, nil))
        >>> func.apply(args, subenv)
        7
        """
        if len(self.formals) != len(args):
            raise SchemeError(f'mu function args error')
        subframe = env.create_subframe(self.formals, args)
        return scheme_spform('begin', self.body, subframe)
    # END PROBLEM EC

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))
# BEGIN PROBLEM EC
"*** YOUR CODE HERE ***"
# END PROBLEM EC


##################
# Tail Recursion #
##################


# Make classes/functions for creating tail recursive programs here?
class Unevaluated:
    """An unevaluated expression with it's environment"""
    def __init__(self, expr, env):
        self.expr = expr
        self.env = env

    def __repr__(self):
        return f'Object Unevaluated: expr: {self.expr}\nenv: {self.env}'


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the optional questions."""
    val = scheme_apply(procedure, args, env)
    # Add stuff here?
    if isinstance(val, Unevaluated):
        val = scheme_eval(val.expr, val.env)
    return val

# BEGIN PROBLEM 8
"*** YOUR CODE HERE ***"
def optimize_tail_calls(original_scheme_eval):
    """"""
    def optimized_eval(expr, env, tail=False):
        if tail and not slef_evaluate(expr) and not isinstance(expr, str):
            return Unevaluated(expr, env)
        
        result = Unevaluated(expr, env)
        while isinstance(result, Unevaluated):
            expr, env = result.expr, result.env
            result = original_scheme_eval(expr, env)
        return result
    return optimized_eval
# END PROBLEM 8
orgin_scheme_eval = scheme_eval
scheme_eval = optimize_tail_calls(scheme_eval)

####################
# Extra Procedures #
####################

def scheme_map(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'map')
    validate_type(s, scheme_listp, 1, 'map')
    return s.map(lambda x: complete_apply(fn, Pair(x, nil), env))

def scheme_filter(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'filter')
    validate_type(s, scheme_listp, 1, 'filter')
    head, current = nil, nil
    while s is not nil:
        item, s = s.first, s.rest
        if complete_apply(fn, Pair(item, nil), env):
            if head is nil:
                head = Pair(item, nil)
                current = head
            else:
                current.rest = Pair(item, nil)
                current = current.rest
    return head

def scheme_reduce(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'reduce')
    validate_type(s, lambda x: x is not nil, 1, 'reduce')
    validate_type(s, scheme_listp, 1, 'reduce')
    value, s = s.first, s.rest
    while s is not nil:
        value = complete_apply(fn, scheme_list(value, s.first), env)
        s = s.rest
    return value

################
# Input/Output #
################

def read_eval_print_loop(next_line, env, interactive=False, quiet=False,
                         startup=False, load_files=()):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
                    print(repl_str(result))
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if (isinstance(err, RuntimeError) and
                'maximum recursion depth exceeded' not in getattr(err, 'args')[0]):
                raise
            elif isinstance(err, RuntimeError):
                print('Error: maximum recursion depth exceeded')
            else:
                print('Error:', err)
        except KeyboardInterrupt:  # <Control>-C
            if not startup:
                raise
            print()
            print('KeyboardInterrupt')
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return

def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or
    (SYM, QUIET, ENV). The file named SYM is loaded into environment ENV,
    with verbosity determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError('"load" given incorrect number of arguments: '
                          '{0}'.format(len(expressions)))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    validate_type(sym, scheme_symbolp, 0, 'load')
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)
    def next_line():
        return buffer_lines(*args)

    read_eval_print_loop(next_line, env, quiet=quiet)

def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))

def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    env.define('eval',
               BuiltinProcedure(scheme_eval, True, 'eval'))
    env.define('apply',
               BuiltinProcedure(complete_apply, True, 'apply'))
    env.define('load',
               BuiltinProcedure(scheme_load, True, 'load'))
    env.define('procedure?',
               BuiltinProcedure(scheme_procedurep, False, 'procedure?'))
    env.define('map',
               BuiltinProcedure(scheme_map, True, 'map'))
    env.define('filter',
               BuiltinProcedure(scheme_filter, True, 'filter'))
    env.define('reduce',
               BuiltinProcedure(scheme_reduce, True, 'reduce'))
    env.define('undefined', None)
    add_builtins(env, BUILTINS)
    return env

@main
def run(*argv):
    import argparse
    parser = argparse.ArgumentParser(description='CS 61A Scheme Interpreter')
    parser.add_argument('--pillow-turtle', action='store_true',
                        help='run with pillow-based turtle. This is much faster for rendering but there is no GUI')
    parser.add_argument('--turtle-save-path', default=None,
                        help='save the image to this location when done')
    parser.add_argument('-load', '-i', action='store_true',
                       help='run file interactively')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help='Scheme file to run')
    args = parser.parse_args()

    import scheme
    scheme.TK_TURTLE = not args.pillow_turtle
    scheme.TURTLE_SAVE_PATH = args.turtle_save_path
    sys.path.insert(0, '')
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(scheme.__file__))))

    next_line = buffer_input
    interactive = True
    load_files = []

    if args.file is not None:
        if args.load:
            load_files.append(getattr(args.file, 'name'))
        else:
            lines = args.file.readlines()
            def next_line():
                return buffer_lines(lines)
            interactive = False

    read_eval_print_loop(next_line, create_global_frame(), startup=True,
                         interactive=interactive, load_files=load_files)
    tscheme_exitonclick()