from __future__ import absolute_import, division, print_function

print('main.py: Running...')


import sys

import libfoolang


ctx = libfoolang.AnalysisContext()
u = ctx.get_from_buffer('foo', 'example')

if u.diagnostics:
    for d in u.diagnostics:
        print('{}'.format(d))
    sys.exit(1)

print('Evaluating .p_do_solving...')
try:
    print(u.root.p_do_solving)
except libfoolang.PropertyError as exc:
    print('Got an exception: {}'.format(exc))

print('main.py: Done.')
