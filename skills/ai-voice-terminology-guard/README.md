# AI Voice Terminology Guard

## Purpose

Improve speech-to-text correction for AI engineering terminology. The goal is not only transcription accuracy, but preservation of technical meaning after AI cleanup.

## Core Problem

Voice systems frequently confuse:

- N / M sounds
- Acronyms
- Product names
- IDE suffixes
- AI framework names

Example failures:

- MCP → NCP
- ANTIGRAVITY IDE → ANTIGRAVITY ID / ANTIGRAVITY
- Cursor IDE → cursor
- VS Code → generic words

## Correction Pipeline

1. Raw transcription
2. Technical terminology detection
3. Context analysis
4. Product-name validation
5. Final correction

Never perform ordinary language normalization before technical validation.

## IDE Preservation Rule

When a user refers to a development environment or AI coding product:

- Preserve `IDE` if context indicates the IDE product.
- Do not remove `IDE` during correction.
- Distinguish:

Correct:
- ANTIGRAVITY IDE
- Cursor IDE
- VS Code
- Windsurf IDE

Incorrect:
- ANTIGRAVITY
- Cursor (when IDE is explicitly intended)

## AI Terminology Dictionary

Protect these terms:

### Protocols
- MCP
- MCP Server
- API

### AI Tools
- ANTIGRAVITY IDE
- Cursor
- VS Code
- Cline
- Roo Code
- Devin

### Frameworks
- LangChain
- LangGraph
- AutoGen
- CrewAI
- OpenHands
- Braintrust
- Langfuse

### Models
- GPT
- Claude
- Gemini
- Llama
- Mistral
- Qwen

## Ambiguity Handling

If a correction is uncertain:

Do not replace with a common word.

Keep the technical candidate and mark uncertainty.

Example:

`可能是 MCP (Model Context Protocol)`

## Context Priority

Technical context overrides phonetic similarity.

Signals increasing confidence:

- GitHub
- Agent
- AI
- IDE
- Plugin
- MCP
- Server
- Coding
- Repository

## Objective

Maximize preservation of AI engineering terminology during speech recognition and AI rewriting.
