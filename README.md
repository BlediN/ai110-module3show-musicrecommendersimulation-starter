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

Running `python -m src.main` with the default **pop / happy** profile produces the following (song titles, scores, and the reasons generated by the scoring function):

```
Loaded songs: 17

User profile:
  favorite_genre: pop
  favorite_mood: happy
  target_energy: 0.8
  likes_acoustic: False

============================================================
Top 5 recommendations
============================================================

1. Sunrise City  by Neon Echo
   Score: 4.88
   Reasons:
     - genre match: pop (+2.0)
     - mood match: happy (+1.0)
     - energy close to 0.8 (+1.47)
     - non-acoustic feel (+0.41)

2. Gym Hero  by Max Pulse
   Score: 3.78
   Reasons:
     - genre match: pop (+2.0)
     - energy close to 0.8 (+1.30)
     - non-acoustic feel (+0.47)

3. Rooftop Lights  by Indigo Parade
   Score: 2.77
   Reasons:
     - mood match: happy (+1.0)
     - energy close to 0.8 (+1.44)
     - non-acoustic feel (+0.33)

4. Concrete Verses  by Aze Marlo
   Score: 1.89
   Reasons:
     - energy close to 0.8 (+1.43)
     - non-acoustic feel (+0.46)

5. Neon Horizon  by Pulsewave
   Score: 1.84
   Reasons:
     - energy close to 0.8 (+1.36)
     - non-acoustic feel (+0.47)
```

**How to read it:** *Sunrise City* (pop, happy, energy 0.82) tops the list because it's the only song that fires all four rules. *Gym Hero* (pop, but *intense*) is second — it wins on genre but misses the mood bonus. *Rooftop Lights* (indie pop, *happy*) is third — it matches mood but not the exact `pop` genre. The remaining slots go to high-energy, non-acoustic songs that match neither genre nor mood, which is exactly why their scores drop below 2.0.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Stress test with diverse and adversarial profiles

I ran `python -m src.main` against six user profiles: three realistic "normal" tastes and three adversarial / edge cases designed to try to trick the scoring logic. Each block below is the actual terminal output (top 5 recommendations, scores, and reasons).

**1. High-Energy Pop** — behaves as expected: the pop/happy song wins outright, and a same-genre (pop/intense) song beats a same-mood (indie pop/happy) song, confirming genre outweighs mood.

```
================================================================
PROFILE: High-Energy Pop
================================================================
Preferences: {'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.9, 'likes_acoustic': False}

Top 5 recommendations:

1. Sunrise City  by Neon Echo  [pop / happy]
   Score: 4.79
   Reasons:
     - genre match: pop (+2.0)
     - mood match: happy (+1.0)
     - energy close to 0.9 (+1.38)
     - non-acoustic feel (+0.41)

2. Gym Hero  by Max Pulse  [pop / intense]
   Score: 3.93
   Reasons:
     - genre match: pop (+2.0)
     - energy close to 0.9 (+1.46)
     - non-acoustic feel (+0.47)

3. Rooftop Lights  by Indigo Parade  [indie pop / happy]
   Score: 2.62
   Reasons:
     - mood match: happy (+1.0)
     - energy close to 0.9 (+1.29)
     - non-acoustic feel (+0.33)

4. Neon Horizon  by Pulsewave  [electronic / uplifting]
   Score: 1.96
   Reasons:
     - energy close to 0.9 (+1.48)
     - non-acoustic feel (+0.47)

5. Storm Runner  by Voltline  [rock / intense]
   Score: 1.93
   Reasons:
     - energy close to 0.9 (+1.48)
     - non-acoustic feel (+0.45)
```

**2. Chill Lofi** — the two lofi/chill tracks lead, then lofi/focused, then cross-genre chill/relaxed songs fill the remaining slots on mood + energy + acoustic fit.

```
================================================================
PROFILE: Chill Lofi
================================================================
Preferences: {'favorite_genre': 'lofi', 'favorite_mood': 'chill', 'target_energy': 0.35, 'likes_acoustic': True}

Top 5 recommendations:

1. Library Rain  by Paper Lanterns  [lofi / chill]
   Score: 4.93
   Reasons:
     - genre match: lofi (+2.0)
     - mood match: chill (+1.0)
     - energy close to 0.35 (+1.50)
     - acoustic feel (+0.43)

2. Midnight Coding  by LoRoom  [lofi / chill]
   Score: 4.75
   Reasons:
     - genre match: lofi (+2.0)
     - mood match: chill (+1.0)
     - energy close to 0.35 (+1.40)
     - acoustic feel (+0.35)

3. Focus Flow  by LoRoom  [lofi / focused]
   Score: 3.81
   Reasons:
     - genre match: lofi (+2.0)
     - energy close to 0.35 (+1.42)
     - acoustic feel (+0.39)

4. Spacewalk Thoughts  by Orbit Bloom  [ambient / chill]
   Score: 2.85
   Reasons:
     - mood match: chill (+1.0)
     - energy close to 0.35 (+1.40)
     - acoustic feel (+0.46)

5. Coffee Shop Stories  by Slow Stereo  [jazz / relaxed]
   Score: 1.92
   Reasons:
     - energy close to 0.35 (+1.47)
     - acoustic feel (+0.45)
```

**3. Deep Intense Rock** — rock/intense wins with a perfect-ish score; note the mood-matching pop/intense song beats several high-energy songs that match neither genre nor mood.

```
================================================================
PROFILE: Deep Intense Rock
================================================================
Preferences: {'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.9, 'likes_acoustic': False}

Top 5 recommendations:

1. Storm Runner  by Voltline  [rock / intense]
   Score: 4.93
   Reasons:
     - genre match: rock (+2.0)
     - mood match: intense (+1.0)
     - energy close to 0.9 (+1.48)
     - non-acoustic feel (+0.45)

2. Gym Hero  by Max Pulse  [pop / intense]
   Score: 2.93
   Reasons:
     - mood match: intense (+1.0)
     - energy close to 0.9 (+1.46)
     - non-acoustic feel (+0.47)

3. Neon Horizon  by Pulsewave  [electronic / uplifting]
   Score: 1.96
   Reasons:
     - energy close to 0.9 (+1.48)
     - non-acoustic feel (+0.47)

4. Concrete Verses  by Aze Marlo  [hip-hop / energetic]
   Score: 1.88
   Reasons:
     - energy close to 0.9 (+1.42)
     - non-acoustic feel (+0.46)

5. Iron Verdict  by Ashen Forge  [metal / aggressive]
   Score: 1.88
   Reasons:
     - energy close to 0.9 (+1.40)
     - non-acoustic feel (+0.48)
```

### Adversarial / edge cases

**4. Conflicting — "Calm Acoustic Metal"** (genre=metal, mood=romantic, target_energy=0.1, likes_acoustic=True). **This one tricks the system.** Iron Verdict (metal/*aggressive*, energy 0.97, acousticness 0.03) still ranks #1 — purely on the flat +2.0 genre bonus — even though it violates *every* other stated preference (it's loud and non-acoustic when the user asked for calm and acoustic). This is the clearest demonstration of the **genre over-prioritization bias**: a single categorical match can outweigh three contradicting signals.

```
================================================================
PROFILE: Conflicting: Calm Acoustic Metal
================================================================
Preferences: {'favorite_genre': 'metal', 'favorite_mood': 'romantic', 'target_energy': 0.1, 'likes_acoustic': True}

Top 5 recommendations:

1. Iron Verdict  by Ashen Forge  [metal / aggressive]
   Score: 2.21
   Reasons:
     - genre match: metal (+2.0)
     - energy close to 0.1 (+0.20)
     - acoustic feel (+0.01)

2. Velvet Hours  by Sable Rose  [r&b / romantic]
   Score: 2.07
   Reasons:
     - mood match: romantic (+1.0)
     - energy close to 0.1 (+0.90)
     - acoustic feel (+0.17)

3. Elegy in Grey  by Halden Quartet  [classical / melancholy]
   Score: 1.77
   Reasons:
     - energy close to 0.1 (+1.29)
     - acoustic feel (+0.47)

4. Spacewalk Thoughts  by Orbit Bloom  [ambient / chill]
   Score: 1.69
   Reasons:
     - energy close to 0.1 (+1.23)
     - acoustic feel (+0.46)

5. Library Rain  by Paper Lanterns  [lofi / chill]
   Score: 1.55
   Reasons:
     - energy close to 0.1 (+1.12)
     - acoustic feel (+0.43)
```

**5. Unknown Genre & Mood** (genre=kpop, mood=euphoric — neither exists in the catalog). The genre and mood rules never fire, so ranking silently collapses to energy + acoustic only. The system still returns 5 confident-looking results with no signal that it found nothing matching the user's actual genre/mood taste — a **graceful-but-silent degradation** risk.

```
================================================================
PROFILE: Unknown Genre & Mood
================================================================
Preferences: {'favorite_genre': 'kpop', 'favorite_mood': 'euphoric', 'target_energy': 0.6, 'likes_acoustic': False}

Top 5 recommendations:

1. Velvet Hours  by Sable Rose  [r&b / romantic]
   Score: 1.68
   Reasons:
     - energy close to 0.6 (+1.35)
     - non-acoustic feel (+0.33)

2. Night Drive Loop  by Neon Echo  [synthwave / moody]
   Score: 1.67
   Reasons:
     - energy close to 0.6 (+1.27)
     - non-acoustic feel (+0.39)

3. Dust Road Home  by Clay Hollow  [country / nostalgic]
   Score: 1.60
   Reasons:
     - energy close to 0.6 (+1.41)
     - non-acoustic feel (+0.18)

4. Rooftop Lights  by Indigo Parade  [indie pop / happy]
   Score: 1.58
   Reasons:
     - energy close to 0.6 (+1.26)
     - non-acoustic feel (+0.33)

5. Concrete Verses  by Aze Marlo  [hip-hop / energetic]
   Score: 1.58
   Reasons:
     - energy close to 0.6 (+1.12)
     - non-acoustic feel (+0.46)
```

**6. Sparse — "Energy Only"** (only target_energy=1.0 provided). Confirms the scoring is **robust to missing keys**: the genre/mood/acoustic rules simply don't fire, and songs rank purely by energy closeness (highest-energy songs win). No crash despite three of four preferences being absent.

```
================================================================
PROFILE: Sparse: Energy Only
================================================================
Preferences: {'target_energy': 1.0}

Top 5 recommendations:

1. Iron Verdict  by Ashen Forge  [metal / aggressive]
   Score: 1.46
   Reasons:
     - energy close to 1.0 (+1.46)

2. Gym Hero  by Max Pulse  [pop / intense]
   Score: 1.40
   Reasons:
     - energy close to 1.0 (+1.40)

3. Storm Runner  by Voltline  [rock / intense]
   Score: 1.36
   Reasons:
     - energy close to 1.0 (+1.36)

4. Neon Horizon  by Pulsewave  [electronic / uplifting]
   Score: 1.33
   Reasons:
     - energy close to 1.0 (+1.33)

5. Concrete Verses  by Aze Marlo  [hip-hop / energetic]
   Score: 1.27
   Reasons:
     - energy close to 1.0 (+1.27)
```

### What the stress test revealed

- **Normal profiles behave correctly** — the right songs surface, and the genre > mood > energy > acoustic priority is visible in the rankings.
- **Genre over-prioritization is real** (profile 4): a flat +2.0 genre bonus can override an energy/mood/acoustic combination that all point the other way. A future fix could scale the genre bonus by how well the other features agree, or cap a song's score when it strongly contradicts stated preferences.
- **No "no good match" signal** (profile 5): when nothing matches a user's genre/mood, the system still returns a full top-5 as if confident. A confidence threshold or a "no strong matches found" message would be more honest.
- **The scoring is robust** (profile 6): partial/sparse profiles don't crash — missing preferences just skip their rule.

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



