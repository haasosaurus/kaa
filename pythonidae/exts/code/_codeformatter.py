# -*- coding: utf-8 -*-


# standard library modules
import copy
import enum
import pathlib
import subprocess

# third-party packages
import autopep8
import bs4
import cssbeautifier
import jsbeautifier


class CodeFormatter:

    class Mode(enum.Enum):
        C = enum.auto()
        CPP = enum.auto()
        CPP_CLI = enum.auto()
        OBJECTIVE_C = enum.auto()
        CSHARP = enum.auto()
        JAVA = enum.auto()


    # astyle configuration
    astyle_opts_default = {
        'kwargs': {
            'mode': 'c',
            'style': 'java',
            'indent': 'spaces=4',
            'lineend': 'linux',
        },
        'args': {
            'add-braces': True,
            'attach-inlines': True,
            'attach-classes': True,
            'attach-namespaces': True,
            'break-closing-braces': True,
            'break-one-line-headers': True,
            'convert-tabs': True,
            'indent-col1-comments': True,
            'indent-switches': True,
            'pad-oper': True,
        },
    }
    astyle_opts = {
        Mode.C: {
            'kwargs': {
                'mode': 'c',
            },
            'args': {},
        },
        Mode.CPP: {
            'kwargs': {
                'mode': 'c',
            },
            'args': {},
        },
        Mode.CPP_CLI: {
            'kwargs': {
                'mode': 'c',
            },
            'args': {},
        },
        Mode.OBJECTIVE_C: {
            'kwargs': {
                'mode': 'c',
            },
            'args': {},
        },
        Mode.CSHARP: {
            'kwargs': {
                'mode': 'cs',
            },
            'args': {},
        },
        Mode.JAVA: {
            'kwargs': {
                'mode': 'java',
            },
            'args': {},
        },
    }

    # python configuration
    autopep8_opts = {
        'max_line_length': 100,
        'aggressive': 3,
    }

    # javascript options
    jsbeautifier_opts = jsbeautifier.default_options()
    jsbeautifier_opts.end_with_newline = False
    jsbeautifier_opts.indent_size = 4

    # css options
    cssbeautifier_opts = cssbeautifier.default_options()
    cssbeautifier_opts.end_with_newline = False
    cssbeautifier_opts.indent_size = 2

    # xml options
    xml_features = 'lxml'  # or alternately 'html5lib'

    @classmethod
    def astyle(
            cls,
            unformatted: str,
            mode: Mode,
    ) -> str:
        command = ['astyle']

        # create options dict
        opts = copy.deepcopy(cls.astyle_opts_default)
        for key, val in cls.astyle_opts[mode].items():
            opts[key].update(val)

        # add kwargs to command
        for key, val in opts['kwargs'].items():
            kwarg = f'--{key}={val}'
            command.append(kwarg)

        # add args to command
        for key, val in opts['args'].items():
            if val:
                key = f'--{key}'
                command.append(key)

        # run the command
        ret = subprocess.run(
            command,
            input=unformatted,
            encoding='utf-8',
            capture_output=True
        )
        formatted = ret.stdout
        return formatted

    @classmethod
    def c(cls, unformatted: str) -> str:
        mode = CodeFormatter.Mode.C
        formatted = cls.astyle(
            unformatted=unformatted,
            mode=mode
        )
        return formatted

    @classmethod
    def cpp(cls, unformatted: str) -> str:
        mode = CodeFormatter.Mode.CPP
        formatted = cls.astyle(
            unformatted=unformatted,
            mode=mode
        )
        return formatted

    @classmethod
    def cpp_cli(cls, unformatted: str) -> str:
        mode = CodeFormatter.Mode.CPP_CLI
        formatted = cls.astyle(
            unformatted=unformatted,
            mode=mode
        )
        return formatted

    @classmethod
    def objective_c(cls, unformatted: str) -> str:
        mode = CodeFormatter.Mode.OBJECTIVE_C
        formatted = cls.astyle(
            unformatted=unformatted,
            mode=mode
        )
        return formatted

    @classmethod
    def cs(cls, unformatted: str) -> str:
        mode = CodeFormatter.Mode.CSHARP
        formatted = cls.astyle(
            unformatted=unformatted,
            mode=mode
        )
        return formatted

    @classmethod
    def java(cls, unformatted: str) -> str:
        mode = CodeFormatter.Mode.JAVA
        formatted = cls.astyle(
            unformatted=unformatted,
            mode=mode
        )
        return formatted

    @classmethod
    def xml(cls, unformatted: str) -> str:
        soup = bs4.BeautifulSoup(
            unformatted,
            features=cls.xml_features,
        )
        formatted = soup.prettify()
        return formatted

    @classmethod
    def python(cls, unformatted: str) -> str:
        formatted = autopep8.fix_code(
            unformatted,
            options=cls.autopep8_opts,
        )
        return formatted

    @classmethod
    def javascript(cls, unformatted: str) -> str:
        formatted = jsbeautifier.beautify(
            unformatted,
            opts=cls.jsbeautifier_opts,
        )
        return formatted

    @classmethod
    def css(cls, unformatted: str) -> str:
        formatted = cssbeautifier.beautify(
            unformatted,
            opts=cls.cssbeautifier_opts,
        )
        return formatted
