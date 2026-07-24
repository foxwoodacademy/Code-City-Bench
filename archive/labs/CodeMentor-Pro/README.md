# CodeMentor Pro

**🚀 Unified AI Coding Mentor SaaS Platform**

An integrated, scalable, marketable SaaS platform combining:
- **Kimi-Code** - Adaptive coding mentor with Six Thinking Hats
- **CodeMentor-MVP** - AI explanation engine & analytics
- **CodeMentor Extension** - VS Code integration layer

## Features

### 🎯 Core Capabilities
- **Adaptive Learning** - Progressive difficulty scaling based on performance
- **Six Thinking Hats** - Edward de Bono's methodology for comprehensive code analysis
- **Multi-Language** - Python, JavaScript, Rust, Go, C++ support
- **Model-Agnostic API** - Works with Kimi, Gemini, OpenRouter, Claude, and local models
- **Static Analysis** - Built-in code metrics without external dependencies
- **Gamified Progression** - XP, levels, achievements, and skill trees

### 🏢 SaaS Features
- **Multi-Tenancy** - Team/organization support with role-based access
- **Subscription Tiers** - Free, Pro, Enterprise pricing models
- **Analytics Dashboard** - Usage metrics, progress tracking, team reports
- **API Gateway** - REST & WebSocket endpoints for integrations
- **Webhook Support** - Event-driven integrations
- **Rate Limiting** - Fair usage policies

### 🎮 Gamification
- **XP & Levels** - Earn experience through challenges and learning
- **Achievements** - Unlock badges for milestones
- **Leaderboards** - Compete with peers (optional)
- **Streaks** - Daily practice rewards
- **Sandbox Mode** - Safe experimentation environment

### 🔌 Integrations
- **VS Code Extension** - In-editor learning and explanation
- **CLI Tool** - Terminal-based access
- **Web Dashboard** - Full-featured web interface
- **API Access** - Programmatic integration
- **Webhooks** - Custom event handling

## Architecture

```
CodeMentor-Pro/
├── core/                      # Core domain logic
│   ├── engines/               # Learning, progression, challenge engines
│   ├── models/               # Data models and schemas
│   ├── services/             # Business logic services
│   └── utils/                # Shared utilities
├── api/                      # API Layer
│   ├── bridges/              # Model provider bridges
│   ├── handlers/             # HTTP/WebSocket handlers
│   ├── middleware/           # Auth, rate limiting, etc.
│   └── routes/               # API route definitions
├── web/                      # Web Application
│   ├── ui/                   # Frontend components
│   │   ├── components/       # React/Vue components
│   │   ├── pages/            # Application pages
│   │   ├── styles/           # CSS/SCSS modules
│   │   └── assets/           # Static assets
│   └── server/               # Backend for web
├── services/                 # Infrastructure services
│   ├── auth/                 # Authentication & authorization
│   ├── billing/              # Subscription management
│   ├── analytics/            # Usage tracking & reporting
│   └── cache/                # Caching layer
├── scripts/                  # Utility scripts
│   ├── setup/                # Installation & configuration
│   ├── migration/            # Data migrations
│   └── deploy/               # Deployment scripts
├── config/                   # Configuration files
├── data/                     # Persistent data storage
├── tests/                    # Test suites
└── docs/                     # Documentation
```

## Quick Start

### Development Setup

```bash
# Clone and setup
cd /storage/emulated/0/RootBase/CodeMentor-Pro
git init

# Install Python dependencies
pip install -r requirements.txt

# Configure API keys
python scripts/setup/configure.py

# Run development server
python -m api.server --port 8767

# Or run full stack
./scripts/deploy/run_dev.sh
```

### Docker Deployment

```bash
# Build image
docker build -t codementor-pro .

# Run container
docker run -p 8000:8000 -p 8767:8767 \
  -v codementor-data:/app/data \
  codementor-pro
```

## API Endpoints

### Public Endpoints
- `GET /api/v1/status` - System health
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/learn/languages` - Available languages
- `GET /api/v1/learn/tracks` - Available learning tracks

### Authenticated Endpoints
- `GET /api/v1/user/me` - User profile
- `GET /api/v1/user/progress` - Learning progress
- `GET /api/v1/challenges` - Available challenges
- `POST /api/v1/challenges/{id}/submit` - Submit solution
- `GET /api/v1/analytics` - Personal analytics
- `POST /api/v1/explain` - Code explanation
- `GET /api/v1/hats` - Six Hats analysis
- `GET /api/v1/skill-tree` - Skill progression tree

### Admin Endpoints
- `GET /api/v1/admin/users` - User management
- `GET /api/v1/admin/analytics` - System analytics
- `POST /api/v1/admin/announcements` - Create announcement

## Configuration

```yaml
# config/application.yaml
app:
  name: CodeMentor Pro
  version: 1.0.0
  environment: development
  debug: true
  port: 8000
  cors_origins: ["http://localhost:3000", "http://localhost:8767"]

database:
  type: sqlite
  path: data/codementor.db

api_providers:
  primary: kimi
  fallback: gemini
  providers:
    kimi:
      enabled: true
      api_key: ${KIMI_API_KEY}
      model: kimi-k2-6
      max_tokens: 4096
      temperature: 0.7
    gemini:
      enabled: true
      api_key: ${GEMINI_API_KEY}
      model: gemini-2.0-flash
      max_tokens: 2048
    openrouter:
      enabled: true
      api_key: ${OPENROUTER_API_KEY}
      model: anthropic/claude-3.5-sonnet
      max_tokens: 4096
    local:
      enabled: false
      endpoint: http://localhost:11434/v1
      model: codellama

subscription:
  free_tier:
    daily_requests: 50
    features: ["explain", "challenges_basic", "progress_tracking"]
  pro_tier:
    monthly_price: 19.99
    features: ["all_free", "challenges_advanced", "six_hats", "analytics", "priority_support"]
  enterprise:
    custom_pricing: true
    features: ["all_pro", "team_management", "custom_models", "sso", "dedicated_support"]

gamification:
  xp_per_challenge: 100
  xp_per_explanation: 25
  xp_per_perfect_solution: 50
  level_thresholds: [1000, 3000, 7000, 15000, 30000]
```

## Version Control

This project follows semantic versioning:
- **MAJOR** - Breaking changes, new architecture
- **MINOR** - New features, backwards compatible
- **PATCH** - Bug fixes, small improvements

### Branch Strategy
- `main` - Production-ready releases
- `develop` - Integration branch for next release
- `feature/*` - New feature development
- `fix/*` - Bug fixes
- `release/*` - Release preparation

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `BREAKING CHANGE`

Example:
```
feat(api): add Six Hats analysis endpoint

- Add /api/v1/analyze/hats endpoint
- Support all 6 hat perspectives
- Include difficulty-based prompts

BREAKING CHANGE: Removes deprecated /api/v1/analyze endpoint
```

## License

AGPL-3.0 - Affero General Public License

This project is open source but requires that any SaaS deployment provides source access to users.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- **Kimi-Code** - Base adaptive learning engine
- **CodeMentor-MVP** - AI explanation and analytics
- **VS Code Extension** - In-editor integration
- **Edward de Bono** - Six Thinking Hats methodology

---

Built with 💚 for developers, by developers.
