from __future__ import print_function

import inspect
import StringIO
from IPython.display import Image


class Img(Image):
    def __repr__(self):
        return '<Img: {}>'.format(self.filename)

fail = Img('fail.png')
ok = Img('ok.png')

print_orig = print
stdout_buffer = StringIO.StringIO()


def check(ex_id):
    import solutions
    reload(solutions)

    if ex_id not in solutions.local_vars or ex_id not in solutions.prints:
        return fail

    frames = inspect.getouterframes(inspect.currentframe())
    frame = frames[1][0].f_locals
    for key, val in solutions.local_vars[ex_id].items():
        if key not in frame or frame[key] != val:
            return fail

    output = stdout_buffer.getvalue()
    stdout_buffer.seek(0)
    stdout_buffer.truncate()
    for msg in solutions.prints[ex_id]:
        if msg not in output:
            return fail

    return ok


def print(*args, **kwargs):
    if 'file' not in kwargs:
        print(*args, file=stdout_buffer, **kwargs)
    print_orig(*args, **kwargs)
