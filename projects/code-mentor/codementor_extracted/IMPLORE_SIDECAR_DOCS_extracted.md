# Implore Sidecar Documentation

The sidecar was built as a lightweight, CLI-native scanner and matcher for grant intelligence, designed to be portable and effective in restricted environments (like Termux).

## Components
- `implore_sidecar.py`: Scans a directory and produces `project_profile.json` (languages, dependencies, README snippet).
- `matcher.py`: Ingests `project_profile.json` and performs keyword matching against grant opportunities (currently mocked).

## Future Roadmap (Unfinished Items)
1. **API Integration:** Replace mock grants in `matcher.py` with live API calls to SAM.gov, Grants.gov Search2, and Simpler.Grants.gov gateway.
2. **Embeddings:** Implement dense semantic matching using `all-MiniLM-L6-v2` or similar to move beyond keyword matching.
3. **Narrative Generator:** Integrate with Claude/OpenAI APIs to draft grant proposals based on matched solicitation criteria.
4. **Formatter:** Implement SF-424 family (SF-424, 424A) form population from JSON.
5. **Validator:** Add a compliance validator to check page limits, attachment requirements, and budget consistency.
