"""
    pygments.lexers.morloc
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Morloc language.

    Based on the morloc compiler grammar (Parser.y and Lexer.hs).

    :copyright: Copyright 2016-2026 by Zebulun Arendsee, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, words
from pygments.token import (
    Comment, Keyword, Name, Number, Operator, Punctuation,
    String, Whitespace,
)

__all__ = ['MorlocLexer']


class MorlocLexer(RegexLexer):
    """
    Morloc language syntax highlighter.

    Supports indentation-sensitive layout, string interpolation,
    triple-quoted multiline strings, typeclasses, do-notation,
    guard expressions, and more.
    """
    name = "Morloc"
    aliases = ["morloc"]
    filenames = ["*.loc"]
    mimetypes = ['text/x-morloc']

    tokens = {
        'root': [
            # Whitespace
            (r'\s+', Whitespace),

            # Group annotation comments: --* ...
            (r'--\*[^\n]*', Comment.Special),

            # Docstring comments: --' ...
            (r"--'[^\n]*", Comment.Special),

            # Line comments: -- ...
            (r'--[^\n]*', Comment.Single),

            # Nestable block comments: {- ... -}
            (r'\{-', Comment.Multiline, 'comment'),

            # Triple-quoted strings (must precede regular strings)
            (r"'''", String, 'triple_single_string'),
            (r'"""', String, 'triple_double_string'),

            # Double-quoted strings with interpolation
            (r'"', String, 'string'),

            # Pragmas: %inline (dim, like comments)
            (r'%inline\b', Comment.Preproc),

            # Intrinsics: @name
            (r"@[a-z][a-zA-Z0-9_']*", Name.Builtin),

            # Keywords
            (words((
                'module', 'import', 'export', 'source', 'from', 'where',
                'as', 'type', 'record', 'object', 'table',
                'class', 'instance',
                'infixl', 'infixr', 'infix',
                'let', 'in', 'do',
            ), prefix=r'\b', suffix=r'\b'), Keyword.Reserved),

            # Built-in constants
            (r'\b(True|False|Null)\b', Keyword.Constant),

            # Numbers: hex, octal, binary, float, integer
            (r'0[xX][0-9a-fA-F]+', Number.Hex),
            (r'0[oO][0-7]+', Number.Oct),
            (r'0[bB][01]+', Number.Bin),
            (r'[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?', Number.Float),
            (r'[0-9]+[eE][+-]?[0-9]+', Number.Float),
            (r'[0-9]+', Number.Integer),

            # Delimiters / punctuation
            (r'[(){}\[\],;]', Punctuation),

            # Lambda
            (r'\\', Operator),

            # Underscore hole (standalone only, not part of identifier)
            (r"_(?![a-zA-Z0-9_'])", Name.Builtin.Pseudo),

            # Operators (sequences of operator characters from Lexer.hs)
            # Covers ::, ->, =>, <-, =, :, ?, !, *, ., <, >, and user-defined
            (r'[:!$%&*+./<=>?@^|~#-]+', Operator),

            # Upper-case identifiers (types, constructors, class names)
            (r"[A-Z][a-zA-Z0-9_']*", Name.Class),

            # Lower-case identifiers (variables, functions)
            (r"[a-z_][a-zA-Z0-9_']*", Name),
        ],

        # Nestable block comments {- ... -}
        'comment': [
            (r'[^{}-]+', Comment.Multiline),
            (r'\{-', Comment.Multiline, '#push'),
            (r'-\}', Comment.Multiline, '#pop'),
            (r'[{}-]', Comment.Multiline),
        ],

        # Double-quoted string with interpolation
        'string': [
            (r'[^"\\#]+', String),
            (r'#\{', String.Interpol, 'interp'),
            (r'\\.', String.Escape),
            (r'#', String),
            (r'"', String, '#pop'),
        ],

        # String interpolation #{...}
        'interp': [
            (r'\}', String.Interpol, '#pop'),
            include('root'),
        ],

        # Triple single-quoted multiline string '''...'''
        'triple_single_string': [
            (r"'''", String, '#pop'),
            (r'#\{', String.Interpol, 'interp'),
            (r"[^'\\#]+", String),
            (r'\\.', String.Escape),
            (r'#', String),
            (r"'", String),
        ],

        # Triple double-quoted multiline string """..."""
        'triple_double_string': [
            (r'"""', String, '#pop'),
            (r'#\{', String.Interpol, 'interp'),
            (r'[^"\\#]+', String),
            (r'\\.', String.Escape),
            (r'#', String),
            (r'"', String),
        ],
    }
