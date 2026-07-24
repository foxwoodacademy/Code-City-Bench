# 🧬 Meatsuit TODO (Human-Only Ops)

*Operational tasks requiring physical presence or off-platform authorization.*

## 🔋 Hardware & Environment
- [ ] **Hardening**: Disable battery optimization for Termux (Android Settings).
- [ ] **Networking**: Confirm static IP on the tablet to prevent swarm discovery drops.
- [ ] **Power**: Ensure a reliable, long-term power source is connected; setup `termux-wake-lock`.

## 💳 Service & Access
- [ ] **API Keys**: Manually rotate/verify Ollama and any cloud API keys in `.env` (NEVER commit these).
- [ ] **Nostr/LNbits**: Manually authorize and backup your primary signing keys for the value generation loop.
- [ ] **Market Access**: Periodic manual verification of Upwork/Freelance account logins if session cookies expire (OAuth bypass).

## 🗄️ Repository Hygiene
- [ ] **Sync Check**: Run `git status` on all secondary devices before starting heavy sessions to ensure local state matches remote.
- [ ] **Database Pruning**: Periodic `vacuum` or cleanup of local SQLite databases if the file size grows beyond 500MB (keep the swarm lean!).

---
*If the swarm asks for these, it's trapped in a loop. Perform these actions, then tell the swarm: `ENVIRONMENT_HARDENED`.*
