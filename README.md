# Quick Translate — Alfred Workflow

[![GitHub Release](https://img.shields.io/github/v/release/snazzybean/alfred-quick-translate)](https://github.com/snazzybean/alfred-quick-translate/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/snazzybean/alfred-quick-translate/total)](https://github.com/snazzybean/alfred-quick-translate/releases)
[![License](https://img.shields.io/github/license/snazzybean/alfred-quick-translate)](https://github.com/snazzybean/alfred-quick-translate/blob/main/LICENSE)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/Y8Y31VP2VK)

Translate text straight from Alfred. Auto-detects the input language, shows dictionary entries for single words, and gives you alternative translations.

![Quick Translate Demo](screenshots/demo.png)

## Features

- **Auto language detection**: type anything, the workflow handles the rest
- **Smart direction**: text in your primary language goes to your target language; anything else comes back to your primary language
- **Dictionary mode**: single words get translations broken down by word class (noun, verb, adjective…)
- **Alternative translations**: shows multiple top translations as separate results
- **Transliteration**: romanized pronunciation for non-Latin scripts (Japanese, Korean, Arabic…)
- **Autocorrect**: catches typos and suggests the corrected version
- **Parallel requests**: fires both translation directions at once, uses whichever fits
- **Configurable**: set your languages and keyword in the workflow settings
- Supports 130+ languages with flag emojis

## Installation

1. Download the latest `.alfredworkflow` from [Releases](https://github.com/snazzybean/alfred-quick-translate/releases)
2. Double-click to import into Alfred
3. Set your preferred languages in the workflow config (defaults to German ↔ English)

> Requires [Alfred](https://www.alfredapp.com/) with Powerpack.

## Usage

Type your keyword (default: `t`) followed by what you want to translate:

| Input | Result |
|-------|--------|
| `t how are you` | Wie geht es dir |
| `t Sehenswürdigkeiten` | Sightseeing attractions |
| `t bonjour le monde` | Hallo Welt |
| `t house` | Haus + dictionary (noun, verb, adjective) |

Hit **Enter** to copy the translation to your clipboard.

## Configuration

Right-click the workflow → **Configure…**

| Setting | Default | Description |
|---------|---------|-------------|
| Primary Language | Deutsch | Your native language |
| Target Language | English | Where your primary language gets translated to |
| Keyword | `t` | Alfred keyword to start translating |

## How it works

Two API requests fire in parallel. One for each possible translation direction. The workflow checks which language was detected and picks the right result. This way you get a response in about the same time regardless of what language you typed in.

When you enter a single word, the API also returns dictionary data: word classes, synonyms, and alternative meanings. These show up below the main translation, grouped by part of speech.

> **Note:** This uses Google Translate's unofficial `gtx` API endpoint. No API key needed, but it's not officially supported by Google and could change at any time.

## License

MIT — see [LICENSE](LICENSE).
