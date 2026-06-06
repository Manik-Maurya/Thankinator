# Contributing to Thankinator

First of all — thanks for wanting to contribute! 🙏 (Yes, that counted.)

---

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists in [Issues](../../issues)
2. If not, open a new issue with:
   - What happened
   - What you expected to happen
   - Steps to reproduce it
   - Your Python version and OS

### Suggesting Features

Open an issue with the label `enhancement` and describe:
- What you want
- Why it would be useful
- Any implementation ideas you have

### Submitting Code

1. **Fork** the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test that the bot still runs correctly
5. Commit with a clear message: `git commit -m "Add: weekly leaderboard reset command"`
6. Push: `git push origin feature/your-feature-name`
7. Open a **Pull Request** with a description of what you changed and why

---

## Ideas We'd Love Help With

- Additional language detections (open an issue with the language + patterns)
- Per-channel leaderboards
- Weekly / monthly stats that auto-reset
- A `!mystats` graph showing your count over time
- Web dashboard to view leaderboard outside Discord
- Docker support for easier self-hosting
- Unit tests for the detection engine

---

## Code Style

- Keep it readable — clear variable names, brief comments where needed
- New detection patterns go in the `_THANK_PATTERNS` list in `bot.py`
- Test your regex patterns before submitting — [regex101.com](https://regex101.com) is your friend
- Keep all bot responses friendly, funny, and non-offensive

---

## Questions?

Open an issue and tag it `question`. Happy to help.

*And yes — every thank you in your PR description counts toward your theoretical Thankinator score.*
