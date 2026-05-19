# Roadmap

This roadmap turns the current assistant into a more reliable and production-quality desktop AI project.

## Phase 1: Stability

- Add automated syntax checks for Python and static files
- Improve optional dependency handling
- Add better microphone error messages
- Add settings for assistant voice, speech speed, and language

## Phase 2: Configuration

- Load `.env` files automatically for local development
- Add a settings screen for folders and API keys
- Store notes and memories in a dedicated `data/` folder
- Add export/import support for user settings

## Phase 3: AI Reasoning Layer

- Add an LLM backend for open-ended conversation
- Store prompts and response rules in versioned files
- Add guardrails for unsafe commands
- Return structured assistant actions instead of plain text only

## Phase 4: Speech Output

- Add voice selection controls
- Add mute and replay controls
- Clean response text before speaking
- Add accessibility support for users who prefer text-only mode

## Phase 5: Automation Tools

- Notes and reminders
- Web search summaries
- Local file/project helper actions
- Calendar and task integrations
- Explicit approval step before sensitive actions

## Phase 6: Production Quality

- Add unit tests for command parsing and tool routing
- Add CI checks for Python syntax and repo health
- Add screenshots and a demo video to the README
- Package the assistant as a Windows executable
