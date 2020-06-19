import numpy
np_clip = numpy.clip
mm_clip = lambda x, l, u: max(l, min(u, x))
s_clip = lambda x, l, u: sorted((x, l, u))[1]
py_clip = lambda x, l, u: l if x < l else u if x > u else x

import random
rrange = random.randrange
print(py_clip(rrange(100), -1, 1))