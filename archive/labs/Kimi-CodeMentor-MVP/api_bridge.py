
# API Bridge - connects to Kimi (me) and other AI providers
api_bridge_py = '''"""
Kimi-Code: API Bridge
Connects to Kimi API, Gemini, OpenRouter, and local models.
Designed to call back to Kimi for advanced analysis.
"""
import json
import urllib.request
import urllib.error
import os
from typing import Dict, Optional, Any
from datetime import datetime

class APIBridge:
    """Unified API bridge for multiple AI providers."""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), '..', 'config.json'
        )
        self.config = self._load_config()
        self.cache = {}  # Simple in-memory cache
    
    def _load_config(self) -> Dict:
        """Load API configuration."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration with Kimi as primary."""
        return {
            "primary_provider": "kimi",
            "fallback_provider": "gemini",
            "providers": {
                "kimi": {
                    "enabled": True,
                    "endpoint": "https://api.moonshot.cn/v1/chat/completions",
                    "api_key": "",
                    "model": "kimi-k2-6",
                    "max_tokens": 4096,
                    "temperature": 0.7,
                    "system_prompt": "You are Kimi, an expert code mentor and software architect."
                },
                "gemini": {
                    "enabled": False,
                    "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
                    "api_key": "",
                    "model": "gemini-2.0-flash",
                    "max_tokens": 2048,
                    "temperature": 0.7
                },
                "openrouter": {
                    "enabled": False,
                    "endpoint": "https://openrouter.ai/api/v1/chat/completions",
                    "api_key": "",
                    "model": "anthropic/claude-3.5-sonnet",
                    "max_tokens": 4096,
                    "temperature": 0.7
                },
                "local": {
                    "enabled": False,
                    "endpoint": "http://localhost:11434/v1/chat/completions",
                    "model": "codellama",
                    "max_tokens": 2048
                }
            },
            "retry_policy": {
                "max_retries": 3,
                "backoff_factor": 2,
                "timeout": 60
            },
            "features": {
                "caching": True,
                "streaming": False,
                "analytics": True
            }
        }
    
    def save_config(self):
        """Save current configuration."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def set_provider_key(self, provider: str, api_key: str):
        """Set API key for a provider."""
        if provider in self.config["providers"]:
            self.config["providers"][provider]["api_key"] = api_key
            self.config["providers"][provider]["enabled"] = True
            self.save_config()
    
    def call_kimi(self, prompt: str, context: Dict = None, 
                  system_override: str = None) -> str:
        """Call Kimi API for analysis.
        
        This is the primary method - designed to leverage Kimi's
        capabilities for code mentoring.
        """
        provider = self.config["providers"]["kimi"]
        
        if not provider.get("api_key"):
            return self._fallback_call(prompt, context, "Kimi API key not configured")
        
        system_prompt = system_override or provider.get("system_prompt", "")
        
        # Enhance prompt with Kimi-Code context
        enhanced_prompt = self._enhance_prompt(prompt, context)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": enhanced_prompt}
        ]
        
        payload = {
            "model": provider["model"],
            "messages": messages,
            "max_tokens": provider.get("max_tokens", 4096),
            "temperature": provider.get("temperature", 0.7)
        }
        
        return self._make_request(provider["endpoint"], payload, provider["api_key"])
    
    def call_gemini(self, prompt: str, context: Dict = None) -> str:
        """Call Gemini API as fallback."""
        provider = self.config["providers"]["gemini"]
        
        if not provider.get("api_key"):
            return self._fallback_call(prompt, context, "Gemini API key not configured")
        
        model = provider["model"]
        url = f"{provider['endpoint']}/{model}:generateContent?key={provider['api_key']}"
        
        enhanced = self._enhance_prompt(prompt, context)
        
        payload = {
            "contents": [{
                "parts": [{"text": enhanced}]
            }],
            "generationConfig": {
                "maxOutputTokens": provider.get("max_tokens", 2048),
                "temperature": provider.get("temperature", 0.7)
            }
        }
        
        try:
            body = json.dumps(payload).encode()
            req = urllib.request.Request(
                url, data=body,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read())
                return result["candidates"][0]["content"]["parts"][0]["text"]
        
        except Exception as e:
            return self._fallback_call(prompt, context, f"Gemini error: {e}")
    
    def call_openrouter(self, prompt: str, context: Dict = None) -> str:
        """Call OpenRouter API."""
        provider = self.config["providers"]["openrouter"]
        
        if not provider.get("api_key"):
            return self._fallback_call(prompt, context, "OpenRouter key not configured")
        
        enhanced = self._enhance_prompt(prompt, context)
        
        payload = {
            "model": provider["model"],
            "messages": [
                {"role": "system", "content": "You are an expert code mentor."},
                {"role": "user", "content": enhanced}
            ],
            "max_tokens": provider.get("max_tokens", 4096)
        }
        
        headers = {
            "Authorization": f"Bearer {provider['api_key']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://kimi-code.local",
            "X-Title": "Kimi-Code"
        }
        
        return self._make_request(provider["endpoint"], payload, None, headers)
    
    def explain_code(self, code: str, language: str = "python", 
                     mode: str = "standard", difficulty: int = 5,
                     hats_mode: bool = False) -> Dict[str, Any]:
        """Main entry point for code explanation.
        
        Args:
            code: The code to analyze
            language: Programming language
            mode: Explanation mode (standard, detailed, beginner, expert)
            difficulty: Complexity level (1-15)
            hats_mode: Whether to use Six Thinking Hats
        
        Returns:
            Dict with explanation, analytics, and metadata
        """
        if hats_mode:
            from .six_hats import SixHatsEngine
            hats = SixHatsEngine()
            prompt = hats.generate_full_analysis_prompt(code)
        else:
            prompt = self._build_explanation_prompt(code, language, mode, difficulty)
        
        # Try primary provider first
        primary = self.config.get("primary_provider", "kimi")
        
        if primary == "kimi" and self.config["providers"]["kimi"]["enabled"]:
            result = self.call_kimi(prompt)
        elif primary == "gemini" and self.config["providers"]["gemini"]["enabled"]:
            result = self.call_gemini(prompt)
        elif primary == "openrouter" and self.config["providers"]["openrouter"]["enabled"]:
            result = self.call_openrouter(prompt)
        else:
            result = self.call_kimi(prompt)  # Always try Kimi
        
        return {
            "explanation": result,
            "provider_used": primary,
            "mode": mode,
            "language": language,
            "difficulty": difficulty,
            "hats_mode": hats_mode,
            "timestamp": datetime.now().isoformat()
        }
    
    def _build_explanation_prompt(self, code: str, language: str, 
                                   mode: str, difficulty: int) -> str:
        """Build a standard explanation prompt."""
        mode_prompts = {
            "standard": "Explain this code clearly with key concepts.",
            "detailed": "Provide a comprehensive analysis including architecture, patterns, and trade-offs.",
            "beginner": "Explain this as if teaching a beginner programmer. Use simple analogies.",
            "expert": "Deep technical analysis for senior developers. Focus on edge cases, optimization, and design patterns.",
            "security": "Security-focused analysis. Identify vulnerabilities, attack vectors, and hardening recommendations.",
            "performance": "Performance analysis. Identify bottlenecks, optimization opportunities, and complexity.",
            "review": "Code review format. Strengths, weaknesses, and actionable improvements."
        }
        
        base_prompt = mode_prompts.get(mode, mode_prompts["standard"])
        
        return f"""{base_prompt}

Language: {language}
Complexity Level: {difficulty}/15

Code:
```{language}
{code}
```

Provide your response in HTML format with:
1. Executive summary (2-3 sentences)
2. Detailed breakdown with code references
3. Key takeaways
4. Suggested next learning topics

Use syntax highlighting and clear section headers.
"""
    
    def _enhance_prompt(self, prompt: str, context: Dict = None) -> str:
        """Enhance prompt with Kimi-Code context."""
        if not context:
            return prompt
        
        enhancements = []
        
        if "user_level" in context:
            enhancements.append(f"User is at level {context['user_level']}. Adjust depth accordingly.")
        
        if "weak_skills" in context:
            enhancements.append(f"Focus on improving: {', '.join(context['weak_skills'])}")
        
        if "strong_skills" in context:
            enhancements.append(f"User excels at: {', '.join(context['strong_skills'])}")
        
        if "session_goals" in context:
            enhancements.append(f"Session goals: {context['session_goals']}")
        
        if enhancements:
            context_block = "\n".join(enhancements)
            return f"""[Context: {context_block}]

{prompt}"""
        
        return prompt
    
    def _make_request(self, endpoint: str, payload: Dict, api_key: str = None,
                     headers: Dict = None) -> str:
        """Make HTTP request to API endpoint."""
        default_headers = {"Content-Type": "application/json"}
        if api_key:
            default_headers["Authorization"] = f"Bearer {api_key}"
        
        if headers:
            default_headers.update(headers)
        
        try:
            body = json.dumps(payload).encode()
            req = urllib.request.Request(
                endpoint, data=body,
                headers=default_headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read())
                
                # Extract content based on API format
                if "choices" in result:
                    return result["choices"][0]["message"]["content"]
                elif "candidates" in result:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    return str(result)
        
        except urllib.error.HTTPError as e:
            return f"API Error {e.code}: {e.reason}"
        except Exception as e:
            return f"Request failed: {e}"
    
    def _fallback_call(self, prompt: str, context: Dict, error_msg: str) -> str:
        """Handle fallback when primary API fails."""
        fallback = self.config.get("fallback_provider", "gemini")
        
        if fallback == "gemini" and self.config["providers"]["gemini"]["enabled"]:
            return self.call_gemini(prompt, context)
        elif fallback == "openrouter" and self.config["providers"]["openrouter"]["enabled"]:
            return self.call_openrouter(prompt, context)
        
        return f"""<h3>API Error</h3>
<p>{error_msg}</p>
<p>Please configure an API key using:</p>
<pre>kimi-code --setup</pre>
"""
'''

with open(f"{base_dir}/core/api_bridge.py", 'w') as f:
    f.write(api_bridge_py)

print("✅ api_bridge.py written")