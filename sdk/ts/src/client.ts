// Minimal TS SDK stubs to satisfy tests
export class CerteusClient {
  constructor(public baseUrl: string) {}

  // Core PFS methods
  async pfsList(path: string): Promise<string[]> { return []; }
  async pfsXattrs(path: string): Promise<Record<string, string>> { return {}; }
  async publish(pco: unknown): Promise<{ status: string }> { return { status: "ok" }; }

  // P2P
  async transportEcho(msg: string): Promise<string> { return msg; }
  async p2pEnqueue(topic: string, payload: unknown): Promise<string> { return "queued"; }
}

