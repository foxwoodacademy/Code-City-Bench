# CaptCoder Phase 1 - Starter Bundle

This bundle contains a focused Phase 1 implementation for the Guided Repair Assistant:
- Centralized AppContext with persistence
- PermissionsGate (camera/mic preflight)
- ErrorBoundary (no white-screen crashes)
- SettingsView (verbose dev settings + privacy)
- AssistantView (single-screen conversational UI)

How to run:
1. Install dependencies:
   - `npm install` or `yarn`
2. Start dev server:
   - `npm run dev` or `yarn dev`
3. Open the URL shown by Vite.

Notes:
- This is a minimal Vite + React + TypeScript starter. It intentionally avoids any mock AI service; wire `src/services/api.ts` to your backend.
- API keys are stored locally in browser localStorage in this template.
- Test permissions flow on desktop Chrome and mobile Safari (iOS permission model differs).

Files are safe to inspect and modify. Good hunting.
