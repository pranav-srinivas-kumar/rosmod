from Tkinter import *
import tkFont
import string
import pygments


class PygmentsText(Text):
    
    """Class that uses the pygments syntax-based highlighter to color-code text
    displayed in a Tk Text widget. Note that this isn't the same as a code
    pretty-printer. It just color-codes. It is also heuristic. It's not easy, in
    general, to determine how much of a text has to be reformatted given a
    change in it. We make a guess (1-2 lines) that should be good for a wide
    variety of highlighted langauges and use cases. """


    def __init__(self, root, lexer, formatter):
        Text.__init__(self, root)

        self.lexer     = lexer      # from pygments.lexers
        self.formatter = formatter  # a TkFormatter

        self.config_tags()
        self.bind('<KeyRelease>', self.key_press)
        self.bind('<Control-l>',  lambda *args: self.reformatEverything() )

    
    def insertFormatted(self, location, text):
        """Similar to self.insert(), but instead of plain text, uses pygments to
        provide a set of formmating tags. The formatter should return stream of
        tagged lines of the format tagName:payload_string\n, which this class then
        inserts in tagged way. Note that if the given text is smaller than a
        "complete syntactic unit" of the language being syntax-highlighted, insertFormatted()
        probably won't result in correct syntax highlighting. Use self.reformatRange()
        or self.reformatEverything() to reformat a larger enclosing range if
        you're making micro-inserts."""
        
        textTagged = pygments.highlight(text, self.lexer, self.formatter)

        insertList = []
        for chunk in textTagged.splitlines():
            # split tagged lines into component parts
            tagEnd = string.index(chunk, ':')
            tagName, stringPart = chunk[:tagEnd], chunk[tagEnd+1:]
            
            # clean up / unquote / reformat data as necessary
            stringPart = string.replace(stringPart, r'\n', "\n")
            
            # add to the insert list
            insertList.append(stringPart)
            insertList.append(tagName)

        # pygments.highlight() can send back extra linefeed markers at the end.
        # So if we didn't mean to end with a return, check for these, and if
        # they're just linefeeds, truncate them
        if not text.endswith("\n"):
            penultimate = insertList[-2]
            if (penultimate.endswith("\n")):
                if penultimate == "\n":
                    insertList = insertList[:-2]
                else:
                    insertList[-2] = insertList[-2][:-1]
        
        # if something to insert, do it (actual typed returns are the missing
        # else case here; net-net they don't get formatted through pygments)
        if insertList:
            self.insert(location, *insertList)


    def config_tags(self):
        """Get style defintions from the friendly local pygments formatter, and
        instantiate them as Tk.Text tag definitions."""
        
        # Discover what 'basefont' currently in use
        curFontName = self.cget('font')
        curFont = tkFont.nametofont(curFontName)
        curFontSpecs = curFont.actual()
        basefont = ' '.join([ str(curFontSpecs[k]) for k in 'family size'.split() ])
        
        # Get tag definitions from our pygments formatter
        styledict = self.formatter.get_style_defs()
        
        # Define our tags accordingly
        for tagName, attTupleList in styledict.iteritems():
            # print "tagconfig:", tagName, tkatts
            for attTuple in attTupleList:
                (attName, attValue) = attTuple
                if attName == 'font':
                    #self.tag_configure(tagName, font = basefont + ' ' + attValue)
                    self.tag_configure(tagName, font = "sans 12")
                else:
                    attSetter = dict([attTuple])
                    self.tag_configure(tagName, **attSetter)


    def key_press(self, key):
        """On key press (key release, acctually, so the character has already
        been inserted), reformat the effected area. The laziest, lowest-performance, and
        yet most correct approach would be to reformat
        the entire text contents. But that might be a bit slow / brute force. So we
        localize the reformatting, usually to a single line, with a fall back to
        several lines. If this doesn't catch it, the user can always type a key
        (default Control-L) bound to self.reformatEverything()."""
            
        savePosn = self.index(INSERT)
        linenum = int(savePosn.split('.')[0])
        startline = linenum
        
        if key.char in {"\n", "\r"}:
            # breaking a line, so reformat this line and the one before
            startline = linenum - 1 if linenum > 1 else 1
            
        self.reformatRange("%d.0"%(startline), "%d.end"%(linenum))
            
        self.see(savePosn)
        self.mark_set(INSERT, savePosn)
    
    
    def reformatRange(self, start, end):
        """Reformat the given range of text. """
        
        buffer = str(self.get(start, end))
        self.delete(start, end)
        self.insertFormatted(start, buffer)
        
    
    def reformatEverything(self):
        """Reformat the works!"""
        
        self.reformatRange("1.0", "end")
