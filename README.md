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


SPECS:
-----
###Nesting###
Definitions may not nest, but their bodies may contain Uses:

    // OK:
    <<< A >>>
    *** A ***
        <<< B >>>
        C
    !!!
    *** B ***
        D
    !!!
    
However, recursion breaks the Super Preprocessor:

    // Bad:
    <<<A>>>
    *** A ***
        <<< B >>>
    !!!
    *** B ***
        <<< A >>>
    !!!

Redefinitions are not allowed:

    // Bad:
    *** A ***
        B
    !!!
    *** A ***
        C
    !!!

###Whitespace###
Whitespace matters, since we parse line-by-line:
* "!!!" lines must have nothing else.
* "<<<" lines must have nothing before them.
where "nothing" means "only tabs and spaces"

So the following in-line symbols are correctly interpreted as non-preprocessor text:

    ## OK excerpts from Bootstrap\sl.ppp, \rt.ppp:
    *** define definition detectors ***
        def is_def_begin(line):
            line = line.strip()
            return (len(line) > 3) and (line[:3] == "***")
        def is_def_end(line):
            return line.strip() == "!!!"
    !!!
    *** parse identifier ***
        identifier = line.replace("<<<", "").replace(">>>", "").strip()
    !!!

But it doesn't matter too much at identifiers' edges:

    // four different def.s/uses of those def.s,
    // all OK:
    *** empty        ***
    !!!
    ***! unique empty ***
    !!!
    *** !empty ***
    !!!
    *** ! empty ***
    !!!
    <<<    empty >>>
    <<<unique empty>>>
    <<<!empty>>>
    <<<! empty>>>

###Parsing after Delimiters###
Program assumes identifier-closing symbols have no trailing text:

    *** after ident. in def., *** rest of line is overlooked
        <<< but after use, >>>rest of code is pasted in
    !!!

is equivalent to:

    *** after ident. in def., ***
        <<< but after use, rest of code is pasted in >>>
    !!!

Because of ungaurded parsing, closing symbols techically unnecessary:

    *** missing end-asterisks
        <<< missing end-angles
        more code
    *** new definition before end-exclamations
        ETC.

is equivalent to:

    *** missing end-asterisks ***
        <<< missing end-angles >>>
        code
    !!!
    *** new definition before end-exclamations ***
        ETC.
