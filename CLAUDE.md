# Live Coding Gym: working rules

Local interview-training app. Design: `docs/design.md`. Run commands from this folder with `uv` (Python 3.12; the system Python 3.9 must not be used).

## Mandatory workflow tools

These are required, not optional. The goal is to spend as few tokens as possible without lowering quality.

1. **Ponytail** (`ponytail:ponytail`). Write the least code that works. Walk its ladder (does it need to exist, is it already here, stdlib, native feature, installed dependency) before writing anything new. No speculative abstractions, no new dependency for a few lines of code. Mark deliberate shortcuts with a `ponytail:` comment naming the ceiling.
2. **Superpowers**. Use its skills at the matching moment:
   - `superpowers:brainstorming` before any new feature or behaviour change.
   - `superpowers:writing-plans` before multi-step work, then `superpowers:executing-plans` or `superpowers:subagent-driven-development` to run the plan.
   - `superpowers:test-driven-development` for every feature and bug fix: failing test first.
   - `superpowers:systematic-debugging` for any failure, before proposing a fix.
   - `superpowers:verification-before-completion` before saying anything is done: run the command and read the output.
3. **Graphify** (`graphify`, CLI at `~/.local/bin/graphify`). Answer questions about the code, architecture or file relationships with `graphify query "<question>"` first, and read source files only for what the graph does not answer. This replaces broad grepping and reading whole files.
4. **Caveman** replies in chat while working. Code, commits, docs and this file stay in normal prose.

## Keeping the graph current

The graph exists at `graphify-out/graph.json` (built 2026-11-14) and must never go stale. SQL files are not yet in it (missing `tree_sitter_sql`; optional: `uv pip install "graphifyy[sql]"`).

- After any task that adds, removes, renames or substantially changes files, run `graphify update .` (re-extracts changed code files, no LLM needed) before the commit, and include `graphify-out/` in that commit. For docs, specs or content changes, run `/graphify . --update` in the assistant instead.
- If `graphify watch .` is running, it keeps code files current, but still run the update after editing docs, specs or content.
- Never hand-edit files in `graphify-out/`.
- If the graph is missing, build it once with `graphify update .` after the first code lands (not before: an empty project has nothing to map).

## Token habits

- Read only the lines you need (`offset` and `limit`), never whole large files.
- Prefer a graph query or one targeted search over reading several files.
- Delegate wide reading to a subagent so only its conclusion enters the conversation.
- Do not re-read a file you just edited.
- Keep commit messages and replies short.

## Project rules

- Content (lessons, exercises, flashcards) lives in `content/` as plain files. App code never contains lesson or exercise text.
- Run `uv run python -m gym.check_content` after any content change. No exercise ships if its own solution fails its own tests.
- The Gemini key lives only in `.env` (gitignored). Never print it, log it, commit it or copy it into any other file.
- Run `uv run pytest` before every commit. A failing test blocks the commit.
- This is a single-user local tool: rough finish is fine, comprehensive content is not negotiable.
