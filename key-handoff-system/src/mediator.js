/**
 * Key-Handoff Mediator
 *
 * Thin JS bridge over the Python mediator so both stacks resolve handles the same way.
 */

const { spawnSync } = require('child_process');
const path = require('path');

class CredentialRetrievalError extends Error {}

class Mediator {
  constructor(options = {}) {
    this.vaultPath = options.vaultPath || '/data/data/com.termux/files/home/.openclaw/vault.enc';
    this.envPrefix = options.envPrefix || '';
  }

  _pythonSnippet(action, serviceName) {
    const mediatorDir = path.resolve(__dirname);
    const payload = JSON.stringify({
      action,
      serviceName,
      vaultPath: this.vaultPath,
      envPrefix: this.envPrefix,
    });

    return `
import json, os, sys
sys.path.insert(0, ${JSON.stringify(mediatorDir)})
from mediator import Mediator, CredentialRetrievalError
payload = json.loads(sys.argv[1])
m = Mediator(payload["vaultPath"], payload["envPrefix"])
try:
    if payload["action"] == "handle":
        result = m.get_handle(payload["serviceName"], include_meta=True)
    elif payload["action"] == "status":
        status = m.get_service_status(payload["serviceName"])
        result = status.__dict__
    elif payload["action"] == "handles":
        result = m.get_handles(payload["serviceName"], include_meta=True)
    else:
        raise ValueError("unknown action")
    print(json.dumps({"ok": True, "result": result}))
except Exception as exc:
    print(json.dumps({"ok": False, "error": str(exc)}))
`;
  }

  _call(action, serviceName) {
    const payload = JSON.stringify({
      action,
      serviceName,
      vaultPath: this.vaultPath,
      envPrefix: this.envPrefix,
    });
    const result = spawnSync('python3', ['-c', this._pythonSnippet(action, serviceName), payload], { encoding: 'utf8' });

    if (result.error) {
      throw result.error;
    }

    if (result.status !== 0 && !result.stdout) {
      throw new Error(result.stderr || `mediator bridge failed with code ${result.status}`);
    }

    const lines = String(result.stdout || '').trim().split(/\r?\n/).filter(Boolean);
    const last = lines[lines.length - 1] || '{}';
    const parsed = JSON.parse(last);
    if (!parsed.ok) {
      throw new CredentialRetrievalError(parsed.error);
    }
    return parsed.result;
  }

  async getHandle(serviceName, options = {}) {
    const record = this._call('handle', serviceName);
    return options.includeMeta ? record : record.handle;
  }

  async getHandles(serviceNames, options = {}) {
    return this._call('handles', serviceNames);
  }

  async getStatus(serviceName) {
    return this._call('status', serviceName);
  }
}

module.exports = Mediator;
module.exports.default = Mediator;
module.exports.CredentialRetrievalError = CredentialRetrievalError;
