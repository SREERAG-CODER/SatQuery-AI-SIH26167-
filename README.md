# SatQuery AI (SIH26167) — Build Roadmap

Scope: SAR-based change detection between two dates, an LLM layer that answers
plain-English questions about the detected changes, and a minimal web app tying
it together. Goal is a working end-to-end prototype for the proposal/screening
stage — not the full production system.

---

## Phase 0 — Setup (Day 0)

- [ ] Create a project repo (GitHub), with folders: `data/`, `preprocessing/`,
      `change_detection/`, `backend/`, `frontend/`
- [ ] Set up a Python virtual environment; install `numpy`, `rasterio` or `GDAL`,
      `opencv-python`, `scikit-image`, `matplotlib`
- [ ] Install `fastapi`, `uvicorn` for the backend
- [ ] Confirm Node/Next.js setup for the frontend
- [ ] Decide on LLM access: an API (OpenAI/Anthropic/etc.) or a local model —
      pick whichever you already have credentials/infra for, don't add a new
      dependency mid-project

## Phase 1 — Get SAR Data (Day 0–1)

- [ ] Create a free Copernicus Open Access Hub / Alaska Satellite Facility (ASF)
      account — both distribute Sentinel-1 SAR imagery at no cost
- [ ] Pick ONE small, well-known area with a clear before/after change (a flood
      event, a reservoir filling/draining, urban construction) — search
      "Sentinel-1 flood example" or similar to find a documented case, so you
      have ground truth to sanity-check against
- [ ] Download two Sentinel-1 SAR scenes of that area: one "before," one
      "after" the change event
- [ ] (Optional, if time allows) Download a matching optical image (Sentinel-2)
      of the same area/dates for a nicer visual, not required for the core logic

## Phase 2 — SAR Preprocessing (Day 1–2)

This is the part with a learning curve — budget real time here.

- [ ] Read up on the basics: SAR images store *backscatter intensity*, not
      color; they need calibration and speckle-noise filtering before use
- [ ] Apply radiometric calibration to both scenes (tools: ESA's SNAP software,
      or Python libraries like `snappy`/`pyroSAR` — SNAP's GUI is the easier
      on-ramp if this is your first time touching SAR)
- [ ] Apply a speckle filter (e.g., Lee filter or median filter) to reduce
      SAR's characteristic grainy noise
- [ ] Co-register the two images so the same pixel in each corresponds to the
      same real-world location (SNAP can do this, or manual reprojection with
      `rasterio`/`GDAL` if scenes are already geocoded)
- [ ] Export both preprocessed scenes as aligned arrays/GeoTIFFs you can load
      in Python

## Phase 3 — Change Detection Baseline (Day 2–3)

Start with the simplest thing that works, then improve only if time remains.

- [ ] **Baseline v1:** compute a pixel-wise difference image (or log-ratio
      image, which is more standard for SAR) between the two calibrated scenes
- [ ] Apply a threshold to the difference image to flag "changed" vs
      "unchanged" pixels — start with a simple statistical threshold (e.g.,
      mean + N × std deviation)
- [ ] Visualize the resulting change mask over the original image; sanity
      check against your known before/after event
- [ ] **Baseline v2 (stretch, only if v1 works and time remains):** replace the
      threshold step with a small classifier (e.g., a shallow CNN or even
      k-means clustering on the difference image) trained/tuned on your one
      example — don't over-invest here, v1 is a legitimate baseline for a
      proposal stage
- [ ] Turn the output into structured facts your LLM step can use: e.g.
      "X% of the region changed," "largest connected changed area is at
      (approx coordinates)," "change consistent with flooding/new
      construction" (a simple heuristic label is fine)

## Phase 4 — LLM Query Layer (Day 3–4)

This is the part that plays to your existing strengths — should move fastest.

- [ ] Design a simple prompt template: feed the structured facts from Phase 3
      into the LLM as context, plus the user's natural-language question
- [ ] Write a small Python function `answer_query(question, change_facts) -> str`
      that formats the prompt and calls the LLM API
- [ ] Test it manually with a handful of example questions: "what changed
      here," "how much of the area was affected," "where is the biggest
      change" — refine the prompt until answers are grounded in your actual
      extracted facts (not hallucinated)
- [ ] (Optional) Add simple RAG structure if you want to scale beyond one
      scene later: store facts per-scene in a small local store (even a JSON
      file or SQLite is enough for a prototype) and retrieve the right one
      based on which image the user is asking about

## Phase 5 — Backend API (Day 4)

- [ ] Set up a FastAPI app with two endpoints:
      - `POST /analyze` — accepts two image uploads (or a stored pair ID),
        runs Phase 2+3 pipeline, returns the change mask + facts
      - `POST /query` — accepts a question + the facts from `/analyze`,
        returns the LLM's answer
- [ ] Wire your Phase 3 and Phase 4 functions into these endpoints
- [ ] Test both endpoints with `curl` or Postman before touching the frontend

## Phase 6 — Frontend (Day 4–5)

- [ ] Build a minimal Next.js page: image upload (or a "load example scene"
      button for the demo), a text input for questions, and a results panel
- [ ] Display the change-mask overlay on the image (canvas overlay or a
      transparent PNG on top of the base image)
- [ ] Display the LLM's answer as text below/beside the image
- [ ] Keep styling minimal — function over polish at this stage

## Phase 7 — Integration Test (Day 5)

- [ ] Run the full flow end-to-end: load example scene → see change mask →
      ask a question → get an answer
- [ ] Fix any breakages in data format handoff between phases (this is where
      most bugs hide — mismatched array shapes, coordinate systems, etc.)
- [ ] Test with 2–3 different example questions to confirm the LLM answers
      stay grounded and don't contradict the visible change mask

## Phase 8 — Proposal Packaging (Day 5–6)

- [ ] Write up the pipeline in the proposal doc: problem → approach →
      architecture diagram → current results
- [ ] Include the before/after SAR images, the change mask, and 1–2 example
      Q&A pairs as evidence the pipeline works
- [ ] Be upfront in the proposal about what's a placeholder for the full
      version (e.g., "v1 uses threshold-based change detection; final version
      will incorporate a trained deep model and support optical+SAR fusion")
      — screening panels respond well to honest scoping, not overclaiming
- [ ] Record a short screen capture of the demo flow as backup in case live
      demo has issues

---

## If you're short on time, the minimum viable cut is:

Phases 0, 1, 2, 3(v1 only), 4, and a bare Phase 5/6 (even a simple script or
Jupyter notebook demo instead of a full web app is acceptable for the
screening stage — the app-level polish matters more if/when you advance).
