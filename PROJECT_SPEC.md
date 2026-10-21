# Apple Local Chat v1 specification

## Objective

Provide a minimal terminal application for multi-turn chat with Apple's
on-device system language model. Add network search only when the user enters
`/search <query>`.

## Required behavior

- Start with `python main.py` and check model availability before the prompt.
- Keep one `LanguageModelSession` for ordinary and searched turns.
- Support `/help`, `/search <query>`, `/new`, and `/exit`.
- Fetch no more than five DDGS result titles, URLs, and 500-character snippets.
- Mark search results as untrusted model context and always print returned URLs.
- Recover from empty input, missing search queries, no results, search failures,
  generation failures, oversized context, Ctrl+C, and Ctrl+D.
- Store no prompts or transcripts.
- Use only `apple-fm-sdk`, `ddgs`, and the Python standard library.

## Privacy boundary

Ordinary prompts do not call DDGS. `/search` sends the query and network
metadata to external search infrastructure. Search snippets are not complete
page contents and may be stale or inaccurate.

## Non-goals

No HTTP API, GUI, model server, code execution, autonomous tools, automatic
browsing, page fetching, database, persistent memory, or multi-provider routing.

## Acceptance

- Two ordinary prompts use the same in-memory session.
- `/new` creates a new session.
- Search and generation failures return control to the prompt.
- Help documents the network privacy boundary.
- Manual checks cover commands, session lifecycle, search grounding, source
  output, unavailable models, error recovery, and clean terminal exit.
