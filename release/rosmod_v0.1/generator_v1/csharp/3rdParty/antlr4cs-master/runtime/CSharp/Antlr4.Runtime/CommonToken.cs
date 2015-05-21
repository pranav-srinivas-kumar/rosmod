/*
 * [The "BSD license"]
 *  Copyright (c) 2013 Terence Parr
 *  Copyright (c) 2013 Sam Harwell
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 *  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 *  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 *  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 *  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
using System;
using Antlr4.Runtime;
using Antlr4.Runtime.Misc;
using Sharpen;

namespace Antlr4.Runtime
{
#if !PORTABLE
    [System.Serializable]
#endif
    public class CommonToken : IWritableToken
    {
        private const long serialVersionUID = -6708843461296520577L;

        /// <summary>
        /// An empty
        /// <see cref="Antlr4.Runtime.Misc.Tuple2{T1, T2}">Antlr4.Runtime.Misc.Tuple2&lt;T1, T2&gt;</see>
        /// which is used as the default value of
        /// <see cref="source">source</see>
        /// for tokens that do not have a source.
        /// </summary>
        protected internal static readonly Tuple<ITokenSource, ICharStream> EmptySource = Tuple.Create<ITokenSource, ICharStream>(null, null);

        /// <summary>
        /// This is the backing field for
        /// <see cref="Type()">Type()</see>
        /// and
        /// <see cref="Type(int)">Type(int)</see>
        /// .
        /// </summary>
        protected internal int type;

        /// <summary>
        /// This is the backing field for
        /// <see cref="Line()">Line()</see>
        /// and
        /// <see cref="Line(int)">Line(int)</see>
        /// .
        /// </summary>
        protected internal int line;

        /// <summary>
        /// This is the backing field for
        /// <see cref="Column()">Column()</see>
        /// and
        /// <see cref="Column(int)">Column(int)</see>
        /// .
        /// </summary>
        protected internal int charPositionInLine = -1;

        /// <summary>
        /// This is the backing field for
        /// <see cref="Channel()">Channel()</see>
        /// and
        /// <see cref="Channel(int)">Channel(int)</see>
        /// .
        /// </summary>
        protected internal int channel = TokenConstants.DefaultChannel;

        /// <summary>
        /// This is the backing field for
        /// <see cref="TokenSource()">TokenSource()</see>
        /// and
        /// <see cref="InputStream()">InputStream()</see>
        /// .
        /// <p>
        /// These properties share a field to reduce the memory footprint of
        /// <see cref="CommonToken">CommonToken</see>
        /// . Tokens created by a
        /// <see cref="CommonTokenFactory">CommonTokenFactory</see>
        /// from
        /// the same source and input stream share a reference to the same
        /// <see cref="Antlr4.Runtime.Misc.Tuple2{T1, T2}">Antlr4.Runtime.Misc.Tuple2&lt;T1, T2&gt;</see>
        /// containing these values.</p>
        /// </summary>
        [NotNull]
        protected internal Tuple<ITokenSource, ICharStream> source;

        /// <summary>
        /// This is the backing field for
        /// <see cref="Text()">Text()</see>
        /// when the token text is
        /// explicitly set in the constructor or via
        /// <see cref="Text(string)">Text(string)</see>
        /// .
        /// </summary>
        /// <seealso cref="Text()">Text()</seealso>
        protected internal string text;

        /// <summary>
        /// This is the backing field for
        /// <see cref="TokenIndex()">TokenIndex()</see>
        /// and
        /// <see cref="TokenIndex(int)">TokenIndex(int)</see>
        /// .
        /// </summary>
        protected internal int index = -1;

        /// <summary>
        /// This is the backing field for
        /// <see cref="StartIndex()">StartIndex()</see>
        /// and
        /// <see cref="SetStartIndex(int)">SetStartIndex(int)</see>
        /// .
        /// </summary>
        protected internal int start;

        /// <summary>
        /// This is the backing field for
        /// <see cref="StopIndex()">StopIndex()</see>
        /// and
        /// <see cref="SetStopIndex(int)">SetStopIndex(int)</see>
        /// .
        /// </summary>
        protected internal int stop;

        /// <summary>
        /// Constructs a new
        /// <see cref="CommonToken">CommonToken</see>
        /// with the specified token type.
        /// </summary>
        /// <param name="type">The token type.</param>
        public CommonToken(int type)
        {
            // set to invalid position
            this.type = type;
            this.source = EmptySource;
        }

        public CommonToken(Tuple<ITokenSource, ICharStream> source, int type, int channel, int start, int stop)
        {
            this.source = source;
            this.type = type;
            this.channel = channel;
            this.start = start;
            this.stop = stop;
            if (source.Item1 != null)
            {
                this.line = source.Item1.Line;
                this.charPositionInLine = source.Item1.Column;
            }
        }

        /// <summary>
        /// Constructs a new
        /// <see cref="CommonToken">CommonToken</see>
        /// with the specified token type and
        /// text.
        /// </summary>
        /// <param name="type">The token type.</param>
        /// <param name="text">The text of the token.</param>
        public CommonToken(int type, string text)
        {
            this.type = type;
            this.channel = TokenConstants.DefaultChannel;
            this.text = text;
            this.source = EmptySource;
        }

        /// <summary>
        /// Constructs a new
        /// <see cref="CommonToken">CommonToken</see>
        /// as a copy of another
        /// <see cref="IToken">IToken</see>
        /// .
        /// <p>
        /// If
        /// <code>oldToken</code>
        /// is also a
        /// <see cref="CommonToken">CommonToken</see>
        /// instance, the newly
        /// constructed token will share a reference to the
        /// <see cref="text">text</see>
        /// field and
        /// the
        /// <see cref="Antlr4.Runtime.Misc.Tuple2{T1, T2}">Antlr4.Runtime.Misc.Tuple2&lt;T1, T2&gt;</see>
        /// stored in
        /// <see cref="source">source</see>
        /// . Otherwise,
        /// <see cref="text">text</see>
        /// will
        /// be assigned the result of calling
        /// <see cref="Text()">Text()</see>
        /// , and
        /// <see cref="source">source</see>
        /// will be constructed from the result of
        /// <see cref="IToken.TokenSource()">IToken.TokenSource()</see>
        /// and
        /// <see cref="IToken.InputStream()">IToken.InputStream()</see>
        /// .</p>
        /// </summary>
        /// <param name="oldToken">The token to copy.</param>
        public CommonToken(IToken oldToken)
        {
            type = oldToken.Type;
            line = oldToken.Line;
            index = oldToken.TokenIndex;
            charPositionInLine = oldToken.Column;
            channel = oldToken.Channel;
            start = oldToken.StartIndex;
            stop = oldToken.StopIndex;
            if (oldToken is Antlr4.Runtime.CommonToken)
            {
                text = ((Antlr4.Runtime.CommonToken)oldToken).text;
                source = ((Antlr4.Runtime.CommonToken)oldToken).source;
            }
            else
            {
                text = oldToken.Text;
                source = Tuple.Create(oldToken.TokenSource, oldToken.InputStream);
            }
        }

        public virtual int Type
        {
            get
            {
                return type;
            }
            set
            {
                int type = value;
                this.type = type;
            }
        }

        public virtual int Line
        {
            get
            {
                return line;
            }
            set
            {
                int line = value;
                this.line = line;
            }
        }

        /// <summary>Explicitly set the text for this token.</summary>
        /// <remarks>
        /// Explicitly set the text for this token. If {code text} is not
        /// <code>null</code>
        /// , then
        /// <see cref="Text()">Text()</see>
        /// will return this value rather than
        /// extracting the text from the input.
        /// </remarks>
        /// <value>
        /// The explicit text of the token, or
        /// <code>null</code>
        /// if the text
        /// should be obtained from the input along with the start and stop indexes
        /// of the token.
        /// </value>
        public virtual string Text
        {
            get
            {
                if (text != null)
                {
                    return text;
                }
                ICharStream input = InputStream;
                if (input == null)
                {
                    return null;
                }
                int n = input.Size;
                if (start < n && stop < n)
                {
                    return input.GetText(Interval.Of(start, stop));
                }
                else
                {
                    return "<EOF>";
                }
            }
            set
            {
                string text = value;
                this.text = text;
            }
        }

        public virtual int Column
        {
            get
            {
                return charPositionInLine;
            }
            set
            {
                int charPositionInLine = value;
                this.charPositionInLine = charPositionInLine;
            }
        }

        public virtual int Channel
        {
            get
            {
                return channel;
            }
            set
            {
                int channel = value;
                this.channel = channel;
            }
        }

        public virtual int StartIndex
        {
            get
            {
                return start;
            }
        }

        public virtual void SetStartIndex(int start)
        {
            this.start = start;
        }

        public virtual int StopIndex
        {
            get
            {
                return stop;
            }
        }

        public virtual void SetStopIndex(int stop)
        {
            this.stop = stop;
        }

        public virtual int TokenIndex
        {
            get
            {
                return index;
            }
            set
            {
                int index = value;
                this.index = index;
            }
        }

        public virtual ITokenSource TokenSource
        {
            get
            {
                return source.Item1;
            }
        }

        public virtual ICharStream InputStream
        {
            get
            {
                return source.Item2;
            }
        }

        public override string ToString()
        {
            string channelStr = string.Empty;
            if (channel > 0)
            {
                channelStr = ",channel=" + channel;
            }
            string txt = Text;
            if (txt != null)
            {
                txt = txt.Replace("\n", "\\n");
                txt = txt.Replace("\r", "\\r");
                txt = txt.Replace("\t", "\\t");
            }
            else
            {
                txt = "<no text>";
            }
            return "[@" + TokenIndex + "," + start + ":" + stop + "='" + txt + "',<" + type + ">" + channelStr + "," + line + ":" + Column + "]";
        }
    }
}
