# Testing and external side effects

The original scripts in tests/ are manual integration exercises. They now run only when invoked directly, so pytest collection does not generate paid content, start OAuth, render a video or upload to YouTube. In particular, test_youtube.py performs a public upload when explicitly executed; use a private test configuration before running it.

The current offline suite checks import safety of those scripts. It does not validate Gemini, stock-video providers, voice services, ffmpeg, or YouTube. Those integrations require configured credentials and explicit manual execution. Existing local README, YouTube-service and experiment-notebook edits have been preserved outside the cleanup commit.
