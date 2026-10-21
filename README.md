# Apple Local Chat

Chat with Apple's on-device Foundation Model from your terminal. The app keeps
one conversation open, so the model remembers earlier messages until you use
`/new` or quit.

Need current information? Run `/search` followed by your question. DDGS fetches
up to five search results, and the Apple model uses those snippets to write its
answer. Regular messages stay on your Mac. A `/search` request sends the query
and network details to external search providers.

No account or API key is needed. The app does not save your prompts, search
results, or chat history.

## Before you start

You will need:

- macOS 26 or newer on a Mac that supports Apple Intelligence
- Apple Intelligence switched on, with its model downloaded and ready
- Xcode 26 or newer, opened once with its agreements accepted
- Python 3.10 or newer
- An internet connection when you use `/search`

Check your Python version first:

```bash
python3 --version
```

Some Macs still point `python3` at an older system version. If yours is below
3.10, install a newer Python release before continuing.

## Install

Clone the repository, then create a virtual environment:

```bash
git clone https://github.com/jagan-jijo/apple-ai-toolkit.git
cd apple-ai-toolkit
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `python3` is older than 3.10, use the command for your newer installation,
such as `python3.11`.

## Start chatting

```bash
python main.py
```

The app checks whether Apple's model is ready before opening the prompt. When
something is missing, it prints the reason reported by the SDK instead of
dropping you into a broken session.

Type a message and press Return:

```text
You > Rewrite this so it sounds friendlier: Please respond at your earliest convenience.
AI  > Could you get back to me when you have a chance?
```

The available commands are:

| Command | What it does |
| --- | --- |
| `/search <query>` | Searches the web and asks the local model to answer from the snippets |
| `/new` | Clears the current conversation and starts a fresh one |
| `/help` | Shows the command guide and search privacy note |
| `/exit` | Closes the app |

Ctrl+C and Ctrl+D close the app too. Empty messages are ignored.

## Using web search

Search only runs when you type `/search`. For example:

```text
You > /search latest Python release
Searching the web...
AI  > Based on the search results, ...
Sources:
[1] Python downloads | Python.org - https://www.python.org/downloads/
```

DDGS returns titles, links, and short snippets. The app does not open each page,
so the model is working from search summaries rather than complete articles.
Those summaries can be stale or wrong.

Every result is marked as untrusted before it reaches the model. Control
characters are removed, and any instructions buried inside a title or snippet
are treated as page content. The source links printed below the answer come
straight from DDGS, even when the model forgets to cite them.

## Fixing setup problems

### `Could not import apple-fm-sdk`

Activate the virtual environment, then install the dependencies again:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The error message includes the original import failure, which can help track
down a missing package or native library.

### `full Xcode installation is required`

Apple's Python SDK needs the full Xcode application. Command Line Tools on their
own cannot build it. Install Xcode, open it once, accept the agreements, and
point `xcode-select` at the application:

```bash
xcode-select -p
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
xcodebuild -version
```

Once `xcode-select -p` shows a path inside `Xcode.app`, run the dependency
installation again.

### `Apple model unavailable`

Read the reason printed beside the error. Check that Apple Intelligence is on
and its model has finished downloading. Also confirm that your Mac supports
Apple Intelligence and that your Xcode version suits the installed macOS
release.

### `The conversation context is too large`

Shorten the message or use `/new`. The SDK decides the available context size,
so the app does not assume a fixed limit.

### `Search failed`

Your local chat still works. DDGS may have timed out, lost its connection, or
hit a provider limit. Try the same search later.

## What this version covers

Version 1 focuses on terminal chat and search you trigger yourself. It does not
run a server, execute code, browse full web pages, save conversations, or switch
between model providers. Apple handles chat generation on the device. DDGS
handles search over the network.

## References

- [Apple Foundation Models SDK for Python](https://github.com/apple/python-apple-fm-sdk)
- [Apple SDK setup guide](https://apple.github.io/python-apple-fm-sdk/getting_started.html)
- [LanguageModelSession reference](https://apple.github.io/python-apple-fm-sdk/api/session.html)
- [DDGS](https://github.com/deedy5/ddgs)

## Licence

Released under the [MIT Licence](LICENSE).
