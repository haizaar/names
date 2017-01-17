from __future__ import unicode_literals
from os.path import abspath, join, dirname
import random
import bisect


__title__ = 'names'
__version__ = '0.3.0.post1'
__author__ = 'Trey Hunner'
__license__ = 'MIT'


full_path = lambda filename: abspath(join(dirname(__file__), filename))


FILES = {
    'first:male': full_path('dist.male.first'),
    'first:female': full_path('dist.female.first'),
    'last': full_path('dist.all.last'),
}

CACHE = {}

def get_name(filename):
    selected = random.random() * 90
    if filename in CACHE:
        return get_name_from_cache(filename, selected)
    else:
        return get_name_from_file(filename, selected)


def get_name_from_cache(filename, selected):
    cache = CACHE[filename]
    i = bisect.bisect_right(cache, selected)
    if i != len(cache):
        return cache[i].name
    return ""


def get_name_from_file(filename, selected):
    with open(filename) as name_file:
        for line in name_file:
            name, _, cummulative, _ = line.split()
            if float(cummulative) > selected:
                return name
    return ""  # Return empty string if file is empty


def get_first_name(gender=None):
    if gender is None:
        gender = random.choice(('male', 'female'))
    if gender not in ('male', 'female'):
        raise ValueError("Only 'male' and 'female' are supported as gender")
    return get_name(FILES['first:%s' % gender]).capitalize()


def get_last_name():
    return get_name(FILES['last']).capitalize()


def get_full_name(gender=None):
    return "{0} {1}".format(get_first_name(gender), get_last_name())


def init_cache():
    for full_path in FILES.values():
        CACHE[full_path] = _build_cache(full_path)


def _build_cache(filename):
    cache = list()
    for line in  open(filename):
        name, _, cummulative, _ = line.split()
        cummulative = float(cummulative)
        item = Name(cummulative)
        item.name = name
        cache.append(item)
    return cache


class Name(float):
    "Extending float (rank) to hold its name"
    pass
