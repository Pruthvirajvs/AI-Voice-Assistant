# Roadmap

This roadmap turns the current static showcase into a working AI voice assistant.

## Phase 1: Browser Voice Prototype

- Add microphone permission handling
- Capture audio from the browser
- Use Web Speech API or a speech-to-text provider
- Display live transcript text
- Add clear error states for unsupported browsers and denied permissions

## Phase 2: AI Reasoning Layer

- Add a backend service for LLM requests
- Store prompts and response rules in versioned files
- Add guardrails for unsafe commands
- Return structured assistant actions instead of plain text only

## Phase 3: Speech Output

- Add text-to-speech playback
- Provide mute, replay, and voice selection controls
- Clean response text before speaking
- Add accessibility support for users who prefer text-only mode

## Phase 4: Automation Tools

- Notes and reminders
- Web search summaries
- Local file/project helper actions
- Calendar and task integrations
- Explicit approval step before sensitive actions

## Phase 5: Production Quality

- Add tests for command parsing and tool routing
- Add CI checks
- Document environment variables
- Add deployment instructions
- Create screenshots and demo video for the README
