const { pipeline } = require('@xenova/transformers');

class DeepSeekMobile {
  constructor(options = {}) {
    this.model = options.model || 'Xenova/codegen-350M-mono';
    this.maxNewTokens = options.maxNewTokens || 128;
    this.temperature = options.temperature ?? 0.2;
    this.initialized = false;
    this.generator = null;
  }

  async init() {
    if (this.initialized) return;
    this.generator = await pipeline('text-generation', this.model);
    this.initialized = true;
  }

  async generateCode(prompt, options = {}) {
    await this.init();
    const result = await this.generator(prompt, {
      max_new_tokens: options.maxNewTokens || this.maxNewTokens,
      temperature: options.temperature ?? this.temperature,
    });
    return result?.[0]?.generated_text || '';
  }
}

module.exports = DeepSeekMobile;
