# morloclexer

A [Pygments](https://pygments.org/) lexer for the [Morloc](https://morloc.io) language.

## Installation

```
pip install morloclexer
```

## Usage

Once installed, Pygments will automatically detect `.loc` files:

```bash
pygmentize -l morloc example.loc
```

Or use it in Python:

```python
from pygments import highlight
from pygments.formatters import HtmlFormatter
from morloclexer.lexer import MorlocLexer

code = 'module main (*)\nimport math (sqrt)\n'
html = highlight(code, MorlocLexer(), HtmlFormatter())
```
