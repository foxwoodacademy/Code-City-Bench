
import { useState, useEffect, useCallback } from 'react';
import { RiskMeshState, SecurityAgent, TacticalCampaign, PentestOutcome } from '../types';

const INITIAL_AGENTS: SecurityAgent[] = [
  { id: 'archer', name: 'Archer', status: 'Active', type: 'Scout', load: 12, health: 100, lastPing: Date.now(), persona: 'Recon Specialist' },
  { id: 'hollis', name: 'Hollis', status: 'Operational', type: 'Guardian', load: 30, health: 100, lastPing: Date.now(), persona: 'Encryption Sentinel' },
  { id: 'eden', name: 'Miss Eden', status: 'Active', type: 'Orchestrator', load: 45, health: 99, lastPing: Date.now(), persona: 'Twin Shard A' },
  { id: 'jude', name: 'Miss Jude', status: 'Active', type: 'Orchestrator', load: 45, health: 99, lastPing: Date.now(), persona: 'Twin Shard B' },
  { id: 'mod-1', name: 'Identity Shard Alpha', status: 'Active', type: 'Overseer', load: 15, health: 100, lastPing: Date.now() },
];

const INITIAL_PENTEST_HISTORY: PentestOutcome[] = [
  { id: 'pen-1', timestamp: Date.now() - 300000, stepLabel: 'Initial Probe', result: 'Success', details: 'Scanning AI Studio edge nodes. Latency detected at 45ms.', vulnerabilityIdentified: 'Open Debug Port' },
  { id: 'pen-2', timestamp: Date.now() - 150000, stepLabel: 'Buffer Overflow Simulation', result: 'Intercepted', details: 'WAF detected high-frequency payload at index 244. Blocked origin.', vulnerabilityIdentified: 'Classic Overflow' },
];

export const useSecurityMesh = () => {
  const [state, setState] = useState<RiskMeshState>({
    globalRisk: 22,
    activeTriggers: [],
    agents: INITIAL_AGENTS,
    networkHealth: 99.98,
    detectedIntent: 'Monitoring',
    auditLedger: [
      { id: 'initial-audit', timestamp: Date.now() - 3600000, type: 'Knowledge Transfer', concept: 'Root Authority Initialization', vector: 'Internal', depth: 'Conceptual', vetted: true }
    ],
    activeCampaigns: [],
    pentestHistory: INITIAL_PENTEST_HISTORY
  });

  const anchorKnowledge = useCallback((concept: string, vector: string, depth: any) => {
    const newAudit = {
      id: `audit-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      type: 'Knowledge Transfer',
      concept,
      vector,
      depth,
      vetted: true
    };
    setState(prev => ({
      ...prev,
      auditLedger: [newAudit, ...prev.auditLedger]
    }));
  }, []);

  const addCampaign = useCallback((name: string, objective: string, steps: any[]) => {
    const newCamp: TacticalCampaign = {
      id: `camp-${Math.random().toString(36).substr(2, 9)}`,
      name,
      objective,
      complexity: Math.floor(Math.random() * 30) + 70,
      steps: steps.map((s, i) => ({
        ...s,
        id: `step-${i}`,
        pos: { x: 10 + (i * 25), y: 30 + Math.random() * 40 }
      }))
    };
    setState(prev => ({
      ...prev,
      activeCampaigns: [newCamp, ...prev.activeCampaigns]
    }));
  }, []);

  const logPentest = useCallback((stepLabel: string, result: 'Success' | 'Intercepted' | 'Warning', details: string, vulnerability?: string) => {
    const outcome: PentestOutcome = {
      id: `pen-${Date.now()}`,
      timestamp: Date.now(),
      stepLabel,
      result,
      details,
      vulnerabilityIdentified: vulnerability
    };
    setState(prev => ({
      ...prev,
      pentestHistory: [outcome, ...prev.pentestHistory].slice(0, 50)
    }));
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setState(prev => ({
        ...prev,
        agents: prev.agents.map(a => ({
          ...a,
          load: Math.max(10, Math.min(90, a.load + (Math.random() * 4 - 2))),
          lastPing: Date.now()
        })),
        globalRisk: Math.max(15, prev.globalRisk - 0.05),
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return { ...state, anchorKnowledge, addCampaign, logPentest };
};
