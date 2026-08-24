export type ProviderId = "openai" | "anthropic" | "openai-compatible";

export interface ModelRequest {
  model: string;
  system?: string;
  input: unknown;
  tools?: ToolDefinition[];
  signal?: AbortSignal;
}

export interface ModelEvent {
  type: "text-delta" | "tool-call" | "reasoning" | "done" | "error";
  text?: string;
  toolCall?: ToolCall;
  error?: Error;
}

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
  execute(input: unknown): Promise<ToolResult>;
}

export interface ToolCall {
  id: string;
  name: string;
  input: unknown;
}

export interface ToolResult {
  output: unknown;
  isError?: boolean;
}

export interface Skill {
  name: string;
  description: string;
  path: string;
  instructions: string;
}

export interface AgentConfig {
  provider: ProviderId;
  model: string;
  maxIterations: number;
  permissionMode: "ask" | "auto" | "deny";
}
