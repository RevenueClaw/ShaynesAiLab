# Model Comparison: phi4-mini vs DeepSeek V4 Flash
## Article: ChatGPT vs Claude vs Gemini

### Generation Stats

| Metric | phi4-mini (3.8B) | DeepSeek V4 Flash |
|--------|-----------------|-------------------|
| Model source | Omen GPU (:11434) | OpenRouter API |
| Cost | Free (local) | ~$0.06 |
| Generation time | ~3 min (incl. 1 retry) | ~1 min |
| Passes needed | 2 (1 fail + retry) | 1 |
| File size | 11,829 bytes | 14,708 bytes |
| Slop flags | "robust" (first pass) | None |

### Quality Observations
- phi4-mini needed a stricter prompt to avoid slop phrases like "robust" and "dive in"
- DeepSeek produced clean output on first attempt with no slop filter triggers
- DeepSeek's output was more nuanced with specific pricing and use-case details
- phi4-mini's output was more generic and template-like in structure
- DeepSeek articles averaged ~830 words vs phi4-mini's ~750

### What This Means for Training Data
- Same prompt, same topic, same system instructions
- Different model outputs show the quality gap between a 3.8B local model and a frontier API model
- Useful for fine-tuning smaller models on higher-quality output patterns
- Can also be used to train a quality classifier (identify which model produced which)
