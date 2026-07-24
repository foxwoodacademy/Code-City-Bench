/**
 * Strongly-typed interfaces for the core conversation_context and related types.
 * This is a focused subset tailored for the Guided Repair Assistant.
 * Expand these as needed to fully type your large JSON bootstrap.
 */

export type ParticipantRole = 'human' | 'ai' | 'system';

export interface DeviceSpec {
  vendor?: string;
  model?: string;
  codename?: string;
  soc?: string;
  storage?: 'eMMC' | 'UFS' | 'UNKNOWN';
  bootloader?: 'locked' | 'unlocked' | 'unknown';
  usb_debugging?: boolean | 'unknown';
  power_state?: 'battery' | 'charging' | 'unknown';
}

export interface RecoveryAction {
  id: string;
  title: string;
  description: string;
  risk: 'low' | 'medium' | 'high';
  prerequisites?: string[];
  tools?: string[];
  vendor_constraints?: string[];
}

export interface HardwareRecovery {
  emmc_extraction?: {
    tools: string[];
    temperature_range_c: { min: number; max: number };
    airflow_cfm?: number;
    nozzle_distance_mm?: { min: number; max: number };
    timing_seconds?: { min: number; max: number };
    notes?: string;
  };
  ram_preservation?: {
    maintain_power: boolean;
    window_seconds?: number;
    notes?: string;
  };
}

export interface ConversationContext {
  bootstrap_metadata?: {
    version?: string;
    timestamp?: string;
    protocol_name?: string;
    purpose?: string;
  };
  conversation_context?: {
    core_project?: string;
    project_status?: string;
    current_phase?: string;
    human?: {
      name?: string;
      approach?: string;
      philosophy?: string;
      projects?: string[];
    };
    technical_elements?: {
      hardware_recovery?: HardwareRecovery;
      software_exploits?: {
        bootloader_modes?: string[];
        tools?: string[];
      };
      context_preservation?: {
        json_bootstrap_handshake?: string;
        proto_schema_buffer?: string;
      };
    };
    key_insights?: {
      problem_identification?: { real_issue?: string; actual_truth?: string };
      next_steps?: { immediate?: string[]; technical?: string[] };
    };
  };
  // allow arbitrary extension while keeping core typed
  [k: string]: any;
}
