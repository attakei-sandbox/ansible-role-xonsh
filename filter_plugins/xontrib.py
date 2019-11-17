import re
from typing import Dict, List
from ansible import errors  # noqa


ansi_escape_8bit = re.compile(br'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')


class Xontrib(object):
    def __init__(self, name: str, installed: bool, loaded: bool):
        self.name = name
        self.installed = installed
        self.loaded = loaded

    def __repr__(self):
        msg = f'Xontrib: {self.name}'
        if self.loaded:
            msg += ' (loaded)'
        elif self.installed:
            msg += ' (installed)'
        else:
            msg += ' (not installed)'
        return msg

    @classmethod
    def parse_from_shell(cls, line: str):
        parts = [
            ansi_escape_8bit.sub(b'', p.encode()).decode()
            for p in line.split()
        ]
        print(parts)
        return cls(parts[0], parts[1] == 'installed', parts[2] == 'loaded')


def parse_xontribs(lines: List[str]) -> Dict[str, Xontrib]:
    xontribs = {}
    for l in lines:
        xontrib = Xontrib.parse_from_shell(l)
        xontribs.setdefault(xontrib.name, xontrib)
    return xontribs


class FilterModule(object):
    def filters(self):
        return {
            'parse_xontribs': parse_xontribs,
        }
