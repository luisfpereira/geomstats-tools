
import argparse

RELEASE_TYPE_TO_LEVEL = {
    'major': 0,
    'minor': 1,
    'patch': 2,
}


def _update_version(filename, level):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith('__version__'):
            version_line = i
            break

    version = line.split('=')[1].strip()[1:-1]
    version_elems = [int(val) for val in version.split('.')]

    version_elems[level] += 1
    i = level + 1
    while i < 3:
        version_elems[i] = 0
        i += 1

    new_version = '.'.join([str(val) for val in version_elems])
    lines[version_line] = f'__version__ = "{new_version}"\n'

    with open(filename, 'w') as file:
        file.writelines(lines)

    return new_version


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('release_type', type=str)

    release_type = parser.parse_args().release_type

    filename = 'geomstats/__init__.py'
    level = RELEASE_TYPE_TO_LEVEL[release_type]

    new_version = _update_version(filename, level=level)
    print(new_version)
