# Quiet Queue

A local task batching prototype prepared for DEV's Slow and Steady challenge, October 2026. It suggests Reply, Read or Arrange and leaves unfamiliar tasks for review. It keeps every original task. It has no email, calendar, file deletion or external API tools.

## Run locally

Use Python 3.12. Create a virtual environment, install `requirements.txt`, then run `python quiet_queue.py`. Open `http://127.0.0.1:8771`. The server listens on the loopback interface only. Stop it with Ctrl+C.

## What is open

The text model uses scikit-learn's TF-IDF features and logistic regression, trained locally on 24 synthetic examples included in the source. It does not download model weights, contact a hosted AI service or need a paid account. scikit-learn uses the BSD-3-Clause licence; dependencies retain their own licences. The small task vocabulary is a limitation, not a general inbox understanding claim. Category probabilities are not calibrated and are not presented as certainty.

## Provenance and limits

New code and synthetic examples were produced by Codex on 20 October 2026, under Alex C. Christou's direction. No existing competition project was imported. Alex confirmed review and approved publication on 20 October 2026. This source is released under the MIT licence; third-party dependencies retain their own licences. Publication of this repository alone does not establish completion or acceptance of a competition entry.

The demo uses synthetic tasks. Functional checks cover retention, duplicate flags, abstention and invalid input. No real inbox, timing comparison, human usage or productivity benefit has been established. Text stays in memory in the local process and is not written to a log. Browser extensions, browser history and the host operating system are outside that limited claim.
