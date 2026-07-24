# ROOTBASE: The ModMind Agentic Stack

This is the master map of the RootBase ecosystem. This stack is designed for high-autonomy, non-KYC revenue generation and agentic education.

## 🗺️ System Architecture

### 1. [Thoth Orchestrator](./thoth_orchestrator/)
**Role:** The Brain / CEO.
- Coordinates all other systems.
- Manages the "Revenue Funnel."
- Triggers deployments and audits.
- **Entry Point:** `thoth.py`

### 2. [Mrs. Higgins SaaS](./mrs_higgins_saas/)
**Role:** The Sales & Front Office.
- Product Catalog (`saas_packages/`).
- AI Copywriting (`copywriter.py`).
- Invoice Generation (`front_desk_lady.py`).
- Lead Closing (`the_closer.py`).

### 3. [ZeroClaw Broker](./zeroclaw_broker/)
**Role:** The Labor Market.
- Bridges the gap between a "Paid Order" and "Worker Execution."
- Manages task claims, results, and evidence.
- **Core:** `zeroclaw_lab_broker/broker.py`

### 4. [Lough System](./lough_system/)
**Role:** The Event Spine / Audit Log.
- Records every single action in the system.
- Provides the "Truth" for payment reconciliation.
- **API:** `field_server.py` (Port 7070).

### 5. [DataCampus](./datacampus/)
**Role:** The Curriculum & Sandbox.
- Defines the "Labs" and "Assignments" that are sold as SaaS.
- Manages student/customer records.

### 6. [Molt Bleak](./molt_bleak/) & [OpenClaw](./openclaw/)
**Role:** The Engine & Framework.
- The underlying agentic logic and process supervision.
- Powering the actual workers that fulfill the ZeroClaw tasks.

### 7. [Coach Bleak](./coach_bleak/)
**Role:** The Accountability Engine / Recovery.
- Aggressive debt recovery and legal pressure.
- The "Bad Cop" for unpaid invoices and contract breaches.

### 8. [Terminal Titans](./terminal_titans/)
**Role:** Technical Hardening & Combat.
- Advanced terminal utilities and agentic "fighting" logic.
- Used for hardening worker agents and testing resilience.

### 9. [ModMind Dashboard](./ModMind_dashboard/)
**Role:** Real-time Monitoring & UI.
- Dynamic HTML dashboard for visualizing the Lough Event Spine.
- Real-time stats on agents, tasks, and revenue.
- **Entry Point:** `index.html`

## 💰 The Money Path (Non-KYC)

`Mrs. Higgins (Offer)` $
ightarrow$ `Voltage/LNbits (Payment)` $
ightarrow$ `ZeroClaw (Task Unlock)` $
ightarrow$ `OpenClaw Worker (Execution)` $
ightarrow$ `Lough (Audit)` $
ightarrow$ `Customer (Delivery)`.

---
*Status: Operational. Managed by Thoth.*
