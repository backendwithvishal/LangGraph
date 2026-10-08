import React from 'react';
import { GitBranch, ExternalLink, Heart, Shield, BookOpen, Code2 } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="w-full border-t border-dark-800 bg-dark-900/90 text-slate-400 text-xs py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          {/* Col 1 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-blue-600 flex items-center justify-center text-white">
                <GitBranch className="w-3.5 h-3.5" />
              </div>
              <span className="font-bold text-slate-100 text-sm">GraphLab</span>
            </div>
            <p className="text-slate-400 leading-relaxed text-[11px]">
              The complete interactive LangGraph 0.2+ educational platform. Master cyclical graphs, persistence, interrupts, and multi-agent systems.
            </p>
          </div>

          {/* Col 2 */}
          <div className="space-y-2">
            <span className="font-semibold text-slate-200 block text-xs uppercase tracking-wider">
              Official Documentation
            </span>
            <ul className="space-y-1.5 text-[11px]">
              <li>
                <a
                  href="https://docs.langchain.com/oss/python/langgraph/overview"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-blue-400 flex items-center gap-1 transition-colors"
                >
                  LangGraph Overview <ExternalLink className="w-2.5 h-2.5" />
                </a>
              </li>
              <li>
                <a
                  href="https://docs.langchain.com/oss/python/langgraph/persistence"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-blue-400 flex items-center gap-1 transition-colors"
                >
                  Persistence & Memory <ExternalLink className="w-2.5 h-2.5" />
                </a>
              </li>
              <li>
                <a
                  href="https://docs.langchain.com/oss/python/langgraph/interrupts"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-blue-400 flex items-center gap-1 transition-colors"
                >
                  Dynamic Interrupts <ExternalLink className="w-2.5 h-2.5" />
                </a>
              </li>
              <li>
                <a
                  href="https://docs.langchain.com/oss/python/langgraph/streaming"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-blue-400 flex items-center gap-1 transition-colors"
                >
                  Streaming Architecture <ExternalLink className="w-2.5 h-2.5" />
                </a>
              </li>
            </ul>
          </div>

          {/* Col 3 */}
          <div className="space-y-2">
            <span className="font-semibold text-slate-200 block text-xs uppercase tracking-wider">
              Curriculum Tracks
            </span>
            <ul className="space-y-1.5 text-[11px]">
              <li><span className="text-emerald-400">●</span> Foundations & StateGraph (Day 1)</li>
              <li><span className="text-cyan-400">●</span> Routing, Reducers & Tools (Day 2)</li>
              <li><span className="text-violet-400">●</span> Persistence, HITL & Streams (Day 3)</li>
              <li><span className="text-indigo-400">●</span> Subgraphs & Functional API (Day 4)</li>
              <li><span className="text-amber-400">●</span> Production RAG & Testing (Day 5)</li>
            </ul>
          </div>

          {/* Col 4 */}
          <div className="space-y-2">
            <span className="font-semibold text-slate-200 block text-xs uppercase tracking-wider">
              Execution Guarantee
            </span>
            <p className="text-[11px] leading-relaxed text-slate-400">
              Deterministic examples and real LangGraph Python graph execution with genuine step-by-step state inspection and SSE event streaming.
            </p>
            <div className="pt-1">
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono">
                <Shield className="w-3 h-3" /> Zero Deprecated APIs
              </span>
            </div>
          </div>
        </div>

        <div className="pt-6 border-t border-dark-800 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-400">
          <span>GraphLab — Interactive Developer Education Platform</span>
          <span className="flex items-center gap-1">
            Built for production AI engineers mastering LangGraph 0.2+
          </span>
        </div>
      </div>
    </footer>
  );
};
