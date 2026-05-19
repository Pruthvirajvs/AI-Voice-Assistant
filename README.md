# AI Voice Assistant

A polished project showcase for an AI-powered voice assistant concept. The repository now includes a clean static interface, professional project documentation, and a practical roadmap for turning the demo into a production-ready voice assistant.

> Current status: static front-end demo and project documentation. The next milestone is connecting real speech-to-text, LLM, and text-to-speech services.

## Highlights

- Professional landing/demo interface for the assistant
- Responsive layout that works on desktop and mobile
- Clear feature positioning for voice input, AI reasoning, automation, and speech output
- Roadmap for moving from concept to functional assistant
- Contribution, security, and licensing files for a complete GitHub presentation

## Demo Files

| File | Purpose |
| --- | --- |
| `index.html` | Main project interface |
| `styles.css` | Responsive visual design |
| `script.js` | Small UI interactions and demo command rendering |
| `docs/ROADMAP.md` | Product and engineering roadmap |

## Planned Architecture

```text
Microphone input
  -> Speech-to-text
  -> Intent detection / LLM reasoning
  -> Tool execution layer
  -> Response generation
  -> Text-to-speech output
```

## Getting Started

Open `index.html` in a browser to view the current static demo.

For a future Python/JavaScript implementation, keep secrets such as API keys in environment variables and never commit them to GitHub.

## Suggested Next Milestones

1. Add a real microphone capture flow with browser permissions.
2. Integrate speech-to-text using Whisper, Web Speech API, or another STT provider.
3. Connect an LLM for natural language responses.
4. Add text-to-speech playback.
5. Create safe automation tools such as web search, notes, reminders, and app launch commands.
6. Add tests, CI, and deployment instructions.

## Repository Cleanup

This branch replaces raw downloaded bundle fragments with a clean, maintainable project structure. The goal is to make the repository readable to recruiters, collaborators, and future contributors.

## License

MIT License. See [LICENSE](LICENSE).