# Lecture-note production workflow

The NPTEL IIT Bombay course recordings provide the chronological spine of this
independent textbook rewrite. Lectures 1–56 are grouped into 20 topic chapters;
lectures 57–60 and tutorials 1–2 supply practice material. The separate course
introduction is outside the selected scope.

1. Enumerate recordings and preserve lecture order, labels, durations, and source
   URLs in the source manifest.
2. Produce local faster-whisper `small.en` machine transcripts and retain source
   media and slide evidence privately. Machine recognition can introduce errors.
3. Read assigned transcripts and develop substantial exposition with definitions,
   prerequisites, notation, derivations, and explicit assumptions.
4. Inspect source frames and accessible primary references for cited claims.
   Preserve uncertainty and unavailable-reference labels instead of inventing
   page-level verification.
5. Develop original teaching constructions, runnable Python examples, and worked
   problems. Distinguish these constructions from lecture statements and
   empirical observations.
6. Obtain independent chapter scientific review, repair findings, and record
   review rounds. Full acceptance requires an independent zero-blocking verdict.
7. Check prose and cross-chapter parity while retaining review evidence.
8. Wrap authored bodies in the shared reader, preserving exact content digests.
   Validate links, timestamps, mathematics rendering, controls, and desktop/mobile
   layouts with bundled CSS, JavaScript, and MathJax.
9. Keep chapter commits, assemble public documentation and curated evidence,
   and publish only after explicit authorization. Raw sources and internal
   editorial material remain outside the repository.

All 20 chapters are written. The final recorded review rounds for chapters 3
and 16–20 still contained findings, subsequently repaired according to the
handoff; independent sign-off on those repairs remains outstanding. Chapter 6's
added practice exercises also need follow-up independent review. The
[editorial record](editorial-review-summary.json) preserves this distinction.
Historical review verdicts are not retrospectively rewritten, and content
inventory or rendering success is not scientific acceptance.

Publication retains the exact scientific chapter bodies from `31a41f2`.
It adds the same root-level HTML, sidecars, bundled assets, tools, README preview,
workflow documentation, and evidence-record arrangement used by the other NPTEL
repositories. The numerical laboratory indexes and launches the existing chapter
programs. Its execution checks reproduce teaching constructions; they do not
validate real turbulent flows or independently review the derivations.

The builder operates entirely on a downloaded repository. It does not require
private media, transcripts, original authoring folders, or a network connection.
The command-line code checker executes listings in separate Python processes and
records their output comparisons. Browser verification checks actual offline
reader behavior. Source-free export and live-publication checks are recorded
separately when performed.
