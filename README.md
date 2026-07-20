# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify and YouTube predict what you'll love next by combining a few core ideas: **collaborative filtering** ("people with taste like yours also liked this"), **content-based filtering** ("this song sounds like things you already play"), and **implicit feedback** from your behavior — skips, replays, and how long you listen. Modern platforms stack these into a pipeline that first narrows millions of songs down to a handful of candidates, then ranks them using deep-learning models that also weigh context like time of day and listening history. My version is a small, transparent **content-based** recommender: instead of learning from a crowd, it scores each song by how well its features (genre, mood, energy, and acousticness) match a user's stated taste profile, then ranks the results and shows the top matches. I prioritize **explainability and simplicity over accuracy at scale** — every recommendation comes with a plain-language reason, so it's easy to see *why* a song was chosen rather than treating the system as a black box.

### Song features

Each `Song` stores ten fields. Four are used directly by the scoring logic; the rest are metadata or reserved for future experiments.

- **Scored:** `genre`, `mood`, `energy` (0–1), `acousticness` (0–1)
- **Metadata / display:** `id`, `title`, `artist`
- **Carried but not yet scored:** `tempo_bpm` (needs scaling), `valence` (0–1), `danceability` (0–1)

### What the `UserProfile` stores

A simple taste profile with four preferences, one per scored feature:

| Field | Example | Compared against |
|---|---|---|
| `favorite_genre` | `"lofi"` | `song.genre` |
| `favorite_mood` | `"chill"` | `song.mood` |
| `target_energy` | `0.35` | `song.energy` |
| `likes_acoustic` | `True` | `song.acousticness` |

### The plan — data flow

The system runs as a three-stage pipeline:

```
INPUT                    PROCESS (the loop)                 OUTPUT (the ranking)
user_prefs (dict)   ─►   for each song:                ─►   sort by score, desc
songs from CSV           score_song() → (score, reasons)    tie-break, take top k
                         collect all scored songs           return top recommendations
```

The **scoring rule** judges one song at a time (it never sees the others); the **ranking rule** is the only stage that looks at all songs together to order them. Keeping these separate is what makes each part easy to test and change.

### Algorithm Recipe (finalized)

Every song starts at **0 points**. Points are added by four rules (maximum possible score = **5.0**):

| Rule | Points | Max |
|---|---|---|
| **Genre match** | `+2.0` if `song.genre == favorite_genre`, else `0` | +2.0 |
| **Mood match** | `+1.0` if `song.mood == favorite_mood`, else `0` | +1.0 |
| **Energy similarity** | `+1.5 × (1 − abs(target_energy − song.energy))` | +1.5 |
| **Acoustic fit** | `+0.5 × acoustic_fit` *(acoustic_fit = acousticness if `likes_acoustic` else 1 − acousticness)* | +0.5 |

```
score = genre_points + mood_points + energy_points + acoustic_points
```

**Why these weights:** genre is the strongest, most committed taste signal, so it counts most; energy similarity is nearly as important and is the one *graded* rule (it rewards songs whose energy is *close* to the target, not just high or low), which breaks ties; mood is a softer, context-dependent preference; acoustic fit is a fine tie-breaker.

**Ranking:** after scoring, sort by score (descending), break ties by energy closeness then `id`, and return the top `k` (default 5). Each recommendation carries a plain-language explanation built from the rules that fired.

### Potential biases

- **Genre over-prioritization.** At +2.0, genre can outweigh a great cross-genre match. A jazz/relaxed song that perfectly fits a user's mood, energy, and acoustic taste may still rank below a same-genre song that matches nothing else — so the system can bury excellent recommendations from adjacent genres.
- **All-or-nothing categories.** Genre and mood give no partial credit: for a `lofi` fan, `ambient` (a close cousin) scores exactly the same `0` as `metal` (the opposite). The system can't express "lofi first, but ambient is fine too."
- **Popularity/majority skew in the data.** The recommender can only surface what's in the catalog. If the dataset over-represents certain genres or moods, users with rarer tastes get worse, narrower recommendations.
- **Ignored features.** `valence`, `danceability`, and `tempo_bpm` don't affect scoring yet, so two songs that differ a lot in danceability or tempo can look identical to the system.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



