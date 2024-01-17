"""
    pygments.lexers.morloc
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Morloc language.

    :copyright: Copyright 2016-2024 by Zebulun Arendsee, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import *
from pygments import unistring as uni

__all__ = ['MorlocLexer']

#  Text        | Token.Text            | for any type of text data
#  Whitespace  | Token.Text.Whitespace | for whitespace
#  Error       | Token.Error           | represents lexer errors
#  Other       | Token.Other           | special token for data not matched by a parser (e.g. HTML markup in PHP code)
#  Keyword     | Token.Keyword         | any kind of keywords
#  Name        | Token.Name            | variable/function names
#  Literal     | Token.Literal         | Any literals
#  String      | Token.Literal.String  | string literals
#  Number      | Token.Literal.Number  | number literals
#  Operator    | Token.Operator        | operators (+, not…)
#  Punctuation | Token.Punctuation     | punctuation ([, (…)
#  Comment     | Token.Comment         | any kind of comments
#  Generic     | Token.Generic         | generic tokens (have a look at the explanation below)


class MorlocLexer(RegexLexer):
    """
    Morloc language syntax highlighter
    """
    name = "Morloc"
    aliases = ["morloc"]
    filenames = ["*.loc"]
    mimetypes = ['text/x-morloc']

    reserved = (
        "module",
        "source",
        "export",
        "import",
        "object",
        "table",
        "record",
        "type",
        "where",
        "from",
    )

    tokens = {
        "root": [
            ("where", Keyword.Reserved),
            (r"\s+", Whitespace),
            (r"--.*$", Comment.Single),
            (r"\{-", Comment.Multiline, "comment"),
            (r"\bmodule\b", Keyword.Reserved, "module"),
            (
                r'(source)(\s+)([A-Za-z]+)(\s*)(\()',
                bygroups(
                    Keyword.Reserved, Whitespace, Name, Whitespace, Text
                ),
                "#push",
                "sourcelist",
            ),
            (
                r'(source)(\s+)([A-Za-z]+)(\s+)(from)(\s+)("[^"]+")(\s*)(\()',
                bygroups(
                    Keyword.Reserved, Whitespace, Name, Whitespace,
                    Keyword.Reserved, Whitespace, String, Whitespace, Text
                ),
                "#push",
                "sourcelist",
            ),
            (
                r"(type)(\s+)([A-Z][A-Za-z]*)",
                bygroups(
                    Keyword.Reserved,
                    Whitespace,
                    Name
                ),
            ),
            #
            (r"^(export)(\s+)([\w+])", bygroups(Keyword.Reserved, Whitespace, Name)),
            (
                r"(\bimport\b)(\s+)([a-zA-Z.][\w]+)",
                bygroups(Keyword.Reserved, Whitespace, Name),
            ),
            (
                r"(\bimport\b)(\()",
                bygroups(Keyword.Reserved, Punctuation),
                "importList",
            ),
            # general constructors
            (r"(object|table|record)(\s+)([A-Z]\w+)(\s*)(=)",
             bygroups(Keyword.Reserved, Whitespace, Name, Whitespace,
                      Operator.Word)),

            #  (r"\bobject\b", Keyword.Reserved, "general_object"),
            #  (r"\btable\b", Keyword.Reserved, "general_table"),
            #  (r"\brecord\b", Keyword.Reserved, "general_record"),
            #  # concrete constructors
            #  (r"\bobject\b", Keyword.Reserved, "concrete_object"),
            #  (r"\btable\b", Keyword.Reserved, "concrete_table"),
            #  (r"\brecord\b", Keyword.Reserved, "concrete_record"),

            #  Identifiers
            (r"[" + uni.Ll + r"][\w']*", Name),
            (r"[" + uni.Lu + r"][\w']*", Name),
            (
                r"(')\[[^\]]*\]",
                Keyword.Type,
            ),  # tuples and lists get special treatment in GHC
            (r"(')\([^)]*\)", Keyword.Type),  # ..
            (r"(')[:!#$%&*+.\\/<=>?@^|~-]+", Keyword.Type),  # promoted type operators
            #  Operators
            (r"(<-|::|->|=>|=|\.|\\|@)", Operator.Word),  # specials
            #  Numbers
            (r"0[xX]_*[\da-fA-F](_*[\da-fA-F])*_*[pP][+-]?\d(_*\d)*", Number.Float),
            (
                r"0[xX]_*[\da-fA-F](_*[\da-fA-F])*\.[\da-fA-F](_*[\da-fA-F])*"
                r"(_*[pP][+-]?\d(_*\d)*)?",
                Number.Float,
            ),
            (r"\d(_*\d)*_*[eE][+-]?\d(_*\d)*", Number.Float),
            (r"\d(_*\d)*\.\d(_*\d)*(_*[eE][+-]?\d(_*\d)*)?", Number.Float),
            (r"0[bB]_*[01](_*[01])*", Number.Bin),
            (r"0[oO]_*[0-7](_*[0-7])*", Number.Oct),
            (r"0[xX]_*[\da-fA-F](_*[\da-fA-F])*", Number.Hex),
            (r"\d(_*\d)*", Number.Integer),
            #  Character/String Literals
            (r'"', String, "string"),
            #  Special
            (r"\[\]", Keyword.Type),
            (r"\(\)", Name.Builtin),
            (r"[][(),;`{}]", Punctuation),
        ],
        "comment": [
            (r"[^-{}]", Comment.Multiline),
            (r"\{-", Comment.Multiline, "#push"),
            (r"-\}", Comment.Multiline, "#pop"),
            (r"[-{}]", Comment.Multiline),
        ],
        "module": [
            (r"\s+", Whitespace),
            (r"[" + uni.Ll + r"][\w.]*", Name, "#pop"),
        ],
        "string": [
            (r'[^\\"]+', String),
            (r"\\", String.Escape, "escape"),
            ('"', String, "#pop"),
        ],
        "escape": [
            (r'[abfnrtv"\'&\\]', String.Escape, "#pop"),
            (r"\^[][" + uni.Lu + r"@^_]", String.Escape, "#pop"),
            (r"o[0-7]+", String.Escape, "#pop"),
            (r"x[\da-fA-F]+", String.Escape, "#pop"),
            (r"\d+", String.Escape, "#pop"),
            (r"(\s+)(\\)", bygroups(Whitespace, String.Escape), "#pop"),
        ],
        "sourcelist": [
            (r"\s+", Whitespace),
            (r"\(", Text, "#push"),
            (r"\)", Text, "#pop"),
            (r"\"[^\"]+\"", String),
            (r",", Punctuation),
            (
                r'("[^"]+")(\s+)(as)(\s+)([\w]+)',
                bygroups(String, Whitespace, Keyword, Whitespace, Name),
            ),
        ],
        "importList": [
            (r"\s+", Whitespace),
            (r"\(", Text, "#push"),
            (r"\)", Text, "#pop"),
            (r"[A-Za-z][\w]*", Name),
            (r",", Punctuation),
        ],

        #  "general_object": [],
        #  "general_table": [],
        #  "general_record": [],
        #  "concrete_object": [],
        #  "concrete_table": [],
        #  "concrete_record": [],
    }
