import re
from typing import Dict, List
from ansible import errors  # noqa


ansi_escape_8bit = re.compile(br'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')


def parse_from_shell(line: str):
    parts = [
        ansi_escape_8bit.sub(b'', p.encode()).decode()
        for p in line.split()
    ]
    return {
        'name': parts[0],
        'installed': parts[1] == 'installed',
        'loaded': parts[2] == 'loaded',
    }


def parse_xontribs(lines: List[str]) -> Dict[str, Dict]:
    xontribs = {}
    for l in lines:
        xontrib = parse_from_shell(l)
        xontribs.setdefault(xontrib['name'], xontrib)
    return xontribs


def xontrib_not_installed(xontribs: List[Dict]) -> List[str]:
    return [
        xontrib['name']
        for xontrib in xontribs.values()
        if not xontrib['installed']
    ]


class FilterModule(object):
    def filters(self):
        return {
            'parse_xontribs': parse_xontribs,
            'xontrib_not_installed': xontrib_not_installed,
        }
