import inspect

from lampost.server.handlers import MethodHandler
from lampost.di.resource import Injected, module_inject

perm = Injected('perm')
module_inject(__name__)

admin_ops = {}


def admin_op(func):
    a_spec = inspect.getargspec(func)

    if a_spec.defaults:
        params = [''] * (len(a_spec.args) - len(a_spec.defaults)) + list(a_spec.defaults)
    else:
        params = [''] * len(a_spec.args)

    admin_ops[func.__name__] = {'func': func, 'dto': {'name': func.__name__, 'args': a_spec.args, 'params': params}}
    return func


class AdminHandler(MethodHandler):

    def operations(self):
        perm.check_perm(self.player, 'supreme')
        return [op['dto'] for op in admin_ops.values()]

    def execute(self):
        exec_op = self.raw
        op = admin_ops[exec_op['name']]
        return op['func'](*exec_op['params'])

