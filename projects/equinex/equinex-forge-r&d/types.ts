
export interface UserProfile {
  id: string;
  name: string;
  email: string;
  avatar: string;
  trustScore: number;
  lastLogin: string;
  status: 'Active' | 'Locked' | 'Review';
}

export interface AuthSession {
  id: string;
  device: string;
  location: string;
  timestamp: string;
  method: 'Biometric' | 'Passkey' | 'OAuth' | 'Hardware';
  risk: 'Low' | 'Medium' | 'High';
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  intent?: string;
  audio?: string; // base64 pcm
  toolCall?: {
    name: string;
    args: any;
  };
}

export interface TacticalStep {
  id: string;
  label: string;
  description: string;
  pos: { x: number; y: number };
  type: 'Entry' | 'Pivot' | 'Objective';
  successRate: number;
  detectionRisk: number;
  targetSubsystem?: string;
}

export interface TacticalCampaign {
  id: string;
  name: string;
  objective: string;
  steps: TacticalStep[];
  complexity: number;
}

export interface SecurityAgent {
  id: string;
  name: string;
  status: 'Active' | 'Standby' | 'Operational' | 'Alert';
  type: 'Overseer' | 'Guardian' | 'Scout' | 'Orchestrator';
  load: number;
  health: number;
  lastPing: number;
  persona?: string;
}

export interface PentestOutcome {
  id: string;
  timestamp: number;
  stepLabel: string;
  result: 'Success' | 'Intercepted' | 'Warning';
  details: string;
  vulnerabilityIdentified?: string;
}

export interface RiskMeshState {
  globalRisk: number;
  activeTriggers: any[];
  agents: SecurityAgent[];
  networkHealth: number;
  detectedIntent?: string;
  auditLedger: any[];
  activeCampaigns: TacticalCampaign[];
  pentestHistory: PentestOutcome[];
}

export type ThinkingHatColor = 'White' | 'Red' | 'Black' | 'Yellow' | 'Green' | 'Blue';

export interface ThinkingHat {
  type: ThinkingHatColor;
  label: string;
  focus: string;
  description: string;
  active: boolean;
}

// FIX: Added missing exported members to resolve module build errors in external components
export interface RemoteLink {
  id: string;
  name: string;
  role: string;
  accessLevel: number;
  status: 'Linked' | 'Pending';
}

export interface AfireflyPreset {
  name: 'combat' | 'ghost';
  label?: string;
}

export interface WearableShard {
  id: string;
  type: 'Watch' | 'Vape';
  label: string;
  battery: number;
  metric: string;
  value: number | string;
  lastSync: number;
}
