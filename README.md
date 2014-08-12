Super-Preprocessor
==================


ABOUT:
-----
Helps with literate programming (at least I __think__ it's called "literate")
by unravelling definitions. For example, we might DEFINE:
    *** declare some integers ***
        int a, b, c;
    !!!
and later USE it as so:
    <<< declare some integers >>>

For include-type stuff, start with:
    ***! only do this once***


EXAMPLE:
-------
See Bootstrap folder for literate rendition of the Super Preprocessor (in Python).


SPECIFICATIONS:
--------------
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
