**A self-hosted gym and body-weight tracker you actually own.**

Plan your week, run guided workouts, log every set and your body weight — 
on your phone, synced across your devices, behind your own passkey login.

[](https://discord.gg/e62jY6fwVb)
[](https://discord.gg/e62jY6fwVb)
[](https://github.com/DuarteSantos8/openGym/stargazers)

[](https://github.com/DuarteSantos8/openGym/releases)
[](https://github.com/DuarteSantos8/openGym/actions/workflows/test.yml)
[](https://gitlab.com/DuarteSantos8/opengym/-/pipelines)
[](https://gitlab.com/DuarteSantos8/opengym/-/pipelines?ref=main)
[](LICENSE)

[Website](https://opengym.duarte-santos.ch) ·
[Live demo](https://opengym.duarte-santos.ch/demo/) ·
[Android APK](https://github.com/DuarteSantos8/openGym/releases/latest) ·
[Self-hosting guide](docs/SELF_HOSTING.md) ·
[Roadmap](ROADMAP.md) ·
[Changelog](CHANGELOG.md)

 Home · today's workout and weight 
 Guided workout · demos and sets 
 Stats · heatmap, charts and PRs 

## Why openGym

Most workout apps keep your data on their servers, push you towards a subscription, or vanish
when the company does. openGym runs on your own box, keeps your data in a folder you control, and
is yours to fork. It still behaves like a modern app: installable on the home screen, passkey
sign-in, works offline, syncs between your phone and your laptop.

No account on someone else's server, no subscription, no ads, no telemetry. One
`docker compose up` and it's running.

The [in-browser demo](https://opengym.duarte-santos.ch/demo/) is the real app with example data,
if you want to try it before installing anything.

## Features

**Planning**

- A routine per weekday over a library of **1,324 exercises** with animated demos, searchable and
 browsable by muscle on a body map. Filter by the equipment you own.
- Four starter plans (Push/Pull/Legs, Upper/Lower, Full Body, 5×5) that load as ordinary,
 editable routines.
- Move a session to another day without touching the weekly plan. The week starts on Monday or
 Sunday, your choice.
- Or skip the weekdays altogether: a **rotation** (A, B, C, A, ...) where the next session is
 simply the next one you haven't done, however the week went.
- Supersets, warm-up sets, drop sets and rest-pause, timed exercises (planks, hangs, carries),
 cardio by time and speed, rest time per exercise, planned deloads.
- Your own exercises, with your own photo, GIF or short video. Location data is stripped on the
 device before upload.

**Training**

- Guided sessions: today's workout starts itself, weights are pre-filled from last time, a rest
 timer runs between sets, PRs are detected as you go. On a rest day it tells you when the next
 session is.
- A quiet workout screen: one menu per exercise, the set number as the set's own menu, card or
 list view. Switches in Settings bring the old button rows back if you liked them.
- Optional effort column as RIR or RPE, colour-coded, with a plain-language line per level.
- Plate math for barbell, EZ bar, trap bar and Smith machine, worked out from the plates you own.
- Bodyweight exercises know they carry no load: log reps, add a dip belt if you use one.
- Per-side reps for lunges and single-arm work, the screen stays awake while you train, and a
 rest-timer alert can flash the screen for loud gyms.
- Swipe a set left to delete it (with Undo) or right to copy it. Pyramid sets with their own reps
 and rest per set, and a scroll wheel for any rest time up to 15 minutes.

**Progress**

- Progression rules per routine or per exercise: linear, Greyskull LP, double progression through a
 visible rep range, or adding time. Each target explains why it is that number; missed reps never
 add load, stalls trigger a deload.
- Estimated 1RM per exercise with its own curve, Structural Balance ratios (Poliquin, Thibaudeau,
 ATG), a year-long activity heatmap.
- A muscle map in three modes: where your volume went, what is still recovering, and what has gone
 untrained.
- Body-weight chart against a goal line, and progress photos on a timeline with a before/after
 slider.
- Edit any saved workout after the fact, log one you did on paper, or move it to the right date.
 Records are re-read from the corrected history.

**Accounts and data**

- Passkeys (Face ID, Touch ID, fingerprint) with per-profile data synced across devices. Password
 sign-in can be switched on per instance; new devices pair with a one-time code or QR.
- Two devices editing at once merge field by field instead of overwriting each other (see
 [sync](#how-sync-works)).
- Import from FitNotes, Strong, Hevy (CSV or API key) and Apple Health weight exports. Export
 everything as one JSON file whenever you like.
- Share a plan as a small file or print it as a PDF.
- Optional admin dashboard with invite-only signup and an activity log.
- 18 languages, including right-to-left Arabic and Traditional Chinese. Exercise names and
 instructions are translated for most of them.

**Optional extras, off by default**

- An [AI coach](docs/AI_COACH.md) that drafts a week of routines and later suggests changes based on
 what you logged. You approve every change. It runs on your server with your own provider key
 (Anthropic, OpenAI, Gemini or any OpenAI-compatible endpoint, Ollama included).
- An [MCP server](mcp/README.md) so an assistant like Claude Desktop can answer questions about your
 training history. Read-only and local; not part of the Docker build.

The full list of what changed release by release is in the [changelog](CHANGELOG.md).

## Quick start

You need [Docker](https://docs.docker.com/get-docker/) with Compose.

```bash
git clone https://github.com/DuarteSantos8/openGym
cd openGym
cp .env.example .env
docker compose pull # prebuilt images, amd64 + arm64 (skip this to build from source)
docker compose up -d
```

Open , tap **Create profile**, and you're in. The first start downloads
the exercise media (about 140 MB) once.

To reach it from your phone with passkeys you need HTTPS on a domain; that's a tw