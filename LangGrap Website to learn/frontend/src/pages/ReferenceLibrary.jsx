import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  HelpCircle,
  Search,
  ExternalLink,
  BookOpen,
  Terminal,
  Code2,
  Cpu,
  Layers,
  ShieldCheck,
  Check
} from 'lucide-react';
import { api } from '../services/api';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const ReferenceLibrary = () => {
  const [searchParams] = useSearchParams();
  const [glossary, setGlossary] = useState([]);
  const [comparison, setComparison] = useState([]);
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '');
  const [activeTab, setActiveTab] = useState('glossary'); // 'glossary' | 'comparison' | 'docs'
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.getGlossary(), api.getFrameworkComparison()])
      .then(([gloss, comp]) => {
        setGlossary(gloss || []);
        setComparison(comp || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const filteredGlossary = glossary.filter(item =>
    item.term.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.definition.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const officialDocsLinks = [
    { title: "LangGraph Overview & Concepts", url: "https://docs.langchain.com/oss/python/langgraph/overview", desc: "Core architecture, mental models, and Pregel super-steps." },
    { title: "Graph API Reference", url: "https://docs.langchain.com/oss/python/langgraph/graph-api", desc: "StateGraph, START, END, add_node, add_conditional_edges, Command." },
    { title: "Persistence & Checkpointing", url: "https://docs.langchain.com/oss/python/langgraph/persistence", desc: "MemorySaver, SqliteSaver, thread_id, state history, and time-travel." },
    { title: "Dynamic Interrupts (HITL)", url: "https://docs.langchain.com/oss/python/langgraph/interrupts", desc: "interrupt(), Command(resume=...), approval gates, and state editing." },
    { title: "Streaming Architecture", url: "https://docs.langchain.com/oss/python/langgraph/streaming", desc: "stream_mode='values', 'updates', 'messages', SSE, and token streaming." },
    { title: "Subgraphs & Hierarchies", url: "https://docs.langchain.com/oss/python/langgraph/subgraphs", desc: "Parent/child state isolation, supervisor agent patterns, and handoffs." },
    { title: "Testing LangGraph Workflows", url: "https://docs.langchain.com/oss/python/langgraph/test", desc: "pytest fixtures, deterministic mock models, and CI assertions." }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-dark-800 pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <HelpCircle className="w-5 h-5 text-blue-400" />
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Reference Library & Architectural Docs
            </h1>
          </div>
          <p className="text-xs text-slate-400">
            Authoritative glossary, framework comparisons, and official LangGraph documentation.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center bg-dark-850 p-1 rounded-lg border border-dark-750">
          <button
            onClick={() => setActiveTab('glossary')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors ${
              activeTab === 'glossary'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Glossary ({glossary.length})
          </button>
          <button
            onClick={() => setActiveTab('comparison')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors ${
              activeTab === 'comparison'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Framework Matrix
          </button>
          <button
            onClick={() => setActiveTab('docs')}
            className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors ${
              activeTab === 'docs'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Official Docs
          </button>
        </div>
      </div>

      {/* TAB 1: GLOSSARY */}
      {activeTab === 'glossary' && (
        <div className="space-y-6">
          
          {/* Search Input */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
            <input
              type="text"
              placeholder="Filter glossary terms (e.g. Reducer, Super-step, Command, Checkpointer)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-dark-850 border border-dark-700 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          {/* Glossary Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredGlossary.map((item, idx) => (
              <Card key={idx} className="space-y-3 border-dark-750 flex flex-col justify-between">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-bold text-cyan-300 font-mono">
                      {item.term}
                    </span>
                    <Badge variant="beginner" size="xs">{item.category}</Badge>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed">
                    {item.definition}
                  </p>

                  {item.code_snippet && (
                    <pre className="p-2.5 rounded-lg bg-dark-950 border border-dark-800 text-[11px] font-mono text-slate-300 overflow-x-auto leading-tight">
                      {item.code_snippet}
                    </pre>
                  )}
                </div>

                {item.docs_url && (
                  <div className="pt-2 border-t border-dark-800/80">
                    <a
                      href={item.docs_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-[11px] text-blue-400 hover:text-blue-300 flex items-center gap-1 font-semibold"
                    >
                      <span>Official Reference</span>
                      <ExternalLink className="w-2.5 h-2.5" />
                    </a>
                  </div>
                )}
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* TAB 2: FRAMEWORK MATRIX */}
      {activeTab === 'comparison' && (
        <div className="space-y-6">
          <div className="rounded-2xl border border-dark-750 bg-dark-850/80 overflow-hidden shadow-xl">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-dark-900 border-b border-dark-750 text-slate-400 uppercase text-[10px] font-bold tracking-wider">
                  <tr>
                    <th className="p-4">Framework</th>
                    <th className="p-4">Execution Paradigm</th>
                    <th className="p-4">Best For</th>
                    <th className="p-4">Strengths</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dark-750/60 font-sans">
                  {comparison.map((f, i) => (
                    <tr key={i} className="hover:bg-dark-800/40 transition-colors">
                      <td className="p-4 font-bold text-white font-mono text-xs">
                        {f.framework}
                      </td>
                      <td className="p-4 text-cyan-300 font-medium">
                        {f.paradigm}
                      </td>
                      <td className="p-4 text-slate-300">
                        {f.best_for}
                      </td>
                      <td className="p-4 text-emerald-400">
                        {f.strengths}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: OFFICIAL DOCS DIRECTORY */}
      {activeTab === 'docs' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {officialDocsLinks.map((doc, idx) => (
            <Card key={idx} hover className="p-4 border-dark-750 flex flex-col justify-between space-y-3">
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-100 text-sm">
                    {doc.title}
                  </span>
                  <ExternalLink className="w-4 h-4 text-slate-400" />
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  {doc.desc}
                </p>
              </div>
              <a
                href={doc.url}
                target="_blank"
                rel="noreferrer"
                className="text-xs font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1"
              >
                <span>Read Documentation</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
