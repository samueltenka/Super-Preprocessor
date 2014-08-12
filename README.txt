Super-Preprocessor
==================


ABOUT:
Literate programming, I think:
    ***declare some integers***
        int a, b, c;
    !!!
To use:
    <<< declare stuff >>>
For include-type stuff, start with:
    ***! only do this once***


FICKLENESS:
Definitions may not nest,
but their bodies may contain Uses.

Redefinitions would overwrite, but error checking in "define(ident, code)".
Technically, closing "***" unnecessary;
code afterward will be overlooked.
New definitions before "!!!" are OK.

Whitespace matters: we parse line-by-line.
"!!!" lines must have only "!!!" and whitespace
But identifiers are stripped, so <<<a>>> is like <<< a >>>.
must be "***!", not "*** !"

Recursion breaks program:
    <<<A>>>
    *** A ***
        <<< B >>>
    !!!
    *** B ***
        <<< A >>>
    !!!
