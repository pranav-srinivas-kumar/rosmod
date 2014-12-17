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
using Antlr4.Runtime;
using Antlr4.Runtime.Atn;
using Antlr4.Runtime.Dfa;
using Sharpen;

namespace Antlr4.Runtime
{
    /// <summary>How to emit recognition errors for parsers.</summary>
    /// <remarks>How to emit recognition errors for parsers.</remarks>
    public interface IParserErrorListener : IAntlrErrorListener<IToken>
    {
        /// <summary>
        /// This method is called by the parser when a full-context prediction
        /// results in an ambiguity.
        /// </summary>
        /// <remarks>
        /// This method is called by the parser when a full-context prediction
        /// results in an ambiguity.
        /// <p/>
        /// When
        /// <code>exact</code>
        /// is
        /// <code>true</code>
        /// , <em>all</em> of the alternatives in
        /// <code>ambigAlts</code>
        /// are viable, i.e. this is reporting an exact ambiguity.
        /// When
        /// <code>exact</code>
        /// is
        /// <code>false</code>
        /// , <em>at least two</em> of the
        /// alternatives in
        /// <code>ambigAlts</code>
        /// are viable for the current input, but
        /// the prediction algorithm terminated as soon as it determined that at
        /// least the <em>minimum</em> alternative in
        /// <code>ambigAlts</code>
        /// is viable.
        /// <p/>
        /// When the
        /// <see cref="Antlr4.Runtime.Atn.PredictionMode.LlExactAmbigDetection">Antlr4.Runtime.Atn.PredictionMode.LlExactAmbigDetection</see>
        /// prediction mode
        /// is used, the parser is required to identify exact ambiguities so
        /// <code>exact</code>
        /// will always be
        /// <code>true</code>
        /// .
        /// </remarks>
        /// <param name="recognizer">the parser instance</param>
        /// <param name="dfa">the DFA for the current decision</param>
        /// <param name="startIndex">the input index where the decision started</param>
        /// <param name="stopIndex">the input input where the ambiguity is reported</param>
        /// <param name="exact">
        /// 
        /// <code>true</code>
        /// if the ambiguity is exactly known, otherwise
        /// <code>false</code>
        /// . This is always
        /// <code>true</code>
        /// when
        /// <see cref="Antlr4.Runtime.Atn.PredictionMode.LlExactAmbigDetection">Antlr4.Runtime.Atn.PredictionMode.LlExactAmbigDetection</see>
        /// is used.
        /// </param>
        /// <param name="ambigAlts">the potentially ambiguous alternatives</param>
        /// <param name="configs">
        /// the ATN configuration set where the ambiguity was
        /// determined
        /// </param>
        void ReportAmbiguity(Parser recognizer, DFA dfa, int startIndex, int stopIndex, bool exact, BitSet ambigAlts, ATNConfigSet configs);

        /// <summary>
        /// This method is called when an SLL conflict occurs and the parser is about
        /// to use the full context information to make an LL decision.
        /// </summary>
        /// <remarks>
        /// This method is called when an SLL conflict occurs and the parser is about
        /// to use the full context information to make an LL decision.
        /// <p/>
        /// If one or more configurations in
        /// <code>configs</code>
        /// contains a semantic
        /// predicate, the predicates are evaluated before this method is called. The
        /// subset of alternatives which are still viable after predicates are
        /// evaluated is reported in
        /// <code>conflictingAlts</code>
        /// .
        /// </remarks>
        /// <param name="recognizer">the parser instance</param>
        /// <param name="dfa">the DFA for the current decision</param>
        /// <param name="startIndex">the input index where the decision started</param>
        /// <param name="stopIndex">the input index where the SLL conflict occurred</param>
        /// <param name="conflictingAlts">
        /// The specific conflicting alternatives. If this is
        /// <code>null</code>
        /// , the conflicting alternatives are all alternatives
        /// represented in
        /// <code>configs</code>
        /// .
        /// </param>
        /// <param name="conflictState">
        /// the simulator state when the SLL conflict was
        /// detected
        /// </param>
        void ReportAttemptingFullContext(Parser recognizer, DFA dfa, int startIndex, int stopIndex, BitSet conflictingAlts, SimulatorState conflictState);

        /// <summary>
        /// This method is called by the parser when a full-context prediction has a
        /// unique result.
        /// </summary>
        /// <remarks>
        /// This method is called by the parser when a full-context prediction has a
        /// unique result.
        /// <p/>
        /// For prediction implementations that only evaluate full-context
        /// predictions when an SLL conflict is found (including the default
        /// <see cref="Antlr4.Runtime.Atn.ParserATNSimulator">Antlr4.Runtime.Atn.ParserATNSimulator</see>
        /// implementation), this method reports cases
        /// where SLL conflicts were resolved to unique full-context predictions,
        /// i.e. the decision was context-sensitive. This report does not necessarily
        /// indicate a problem, and it may appear even in completely unambiguous
        /// grammars.
        /// <p/>
        /// <code>configs</code>
        /// may have more than one represented alternative if the
        /// full-context prediction algorithm does not evaluate predicates before
        /// beginning the full-context prediction. In all cases, the final prediction
        /// is passed as the
        /// <code>prediction</code>
        /// argument.
        /// </remarks>
        /// <param name="recognizer">the parser instance</param>
        /// <param name="dfa">the DFA for the current decision</param>
        /// <param name="startIndex">the input index where the decision started</param>
        /// <param name="stopIndex">
        /// the input index where the context sensitivity was
        /// finally determined
        /// </param>
        /// <param name="prediction">the unambiguous result of the full-context prediction</param>
        /// <param name="acceptState">
        /// the simulator state when the unambiguous prediction
        /// was determined
        /// </param>
        void ReportContextSensitivity(Parser recognizer, DFA dfa, int startIndex, int stopIndex, int prediction, SimulatorState acceptState);
    }
}
