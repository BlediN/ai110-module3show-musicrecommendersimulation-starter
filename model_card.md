# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

**Goal / Task.** VibeMatch suggests songs a user is likely to enjoy. It takes a short "taste profile" and returns a ranked list of the top matches from a small song catalog, with a plain reason for each pick.

This is a **classroom learning project**, not a real product. It is built to show how a simple, transparent recommender turns data into ranked suggestions. It assumes the user can describe their taste in four ways: a favorite genre, a favorite mood, a target energy level, and whether they like acoustic music.

**Non-intended use.** It should not be used as a real music service or to make decisions about people. The catalog is tiny (17 songs), the taste profile is very simple, and the scoring rules are hand-picked, not learned from real listening data. It does not know about lyrics, language, culture, or an artist's popularity.

---

## 3. How the Model Works  

Each song has a few labels and numbers: its genre, its mood, and scores from 0 to 1 for energy and how acoustic it sounds. The user profile lists a favorite genre, a favorite mood, a target energy, and whether they like acoustic music.

To score a song, the model gives out points. A matching genre earns the most points. A matching mood earns some points. For energy, the closer the song's energy is to what the user wants, the more points it gets — so it rewards songs that are *close*, not just loud or quiet. It also gives a small bonus if the song's acoustic feel matches the user's taste. All the points are added up into one score.

Once every song has a score, the model sorts them from highest to lowest and shows the top few. Each recommendation comes with the list of reasons it earned points, so the user can see *why* it was chosen. Compared to the starter code (which just returned the first few songs), I added the real scoring rules, the ranking, and the human-readable reasons.

---

## 4. Data  

The catalog has **17 songs**. Each song has ten fields: id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The model only uses four of these for scoring (genre, mood, energy, acousticness); the rest are display info or saved for later experiments.

The starter file had 10 songs, mostly pop, lofi, and a few others. I **added 7 songs** to widen the range, bringing in genres like hip-hop, classical, electronic, r&b, country, metal, and folk, and moods like romantic, aggressive, and nostalgic.

Even after that, the dataset is very small and still a little uneven — lofi (3 songs) and pop (2) appear more than any single new genre (1 each). Big parts of real musical taste are missing: there are no lyrics, no languages other than the labels, no sub-genres, and no sense of what is actually popular.

---

## 5. Strengths  

The system works well for users with a **clear, consistent taste**. When a profile's genre, mood, and energy all point the same way, the right songs rise to the top. For example, the "Chill Lofi" profile correctly puts the two lofi/chill tracks first, and the "Deep Intense Rock" profile puts the rock/intense song first.

It also captures the idea that **similar-but-not-exact songs are still good matches**. A chill ambient song shows up for a lofi/chill user because it matches mood and energy even without the exact genre. The energy rule behaves the way I hoped — it favors songs near the target instead of just the highest-energy ones.

Finally, every recommendation is **explainable**. The reasons list shows exactly which rules fired and how many points they added, so the results are easy to trust and easy to debug. In my testing, the rankings usually matched my intuition about which songs "fit" each profile.

---

## 6. Limitations and Bias 

The clearest weakness I found is **genre over-prioritization creating a filter bubble.** Because a genre match awards a flat +2.0 — more than any other rule — a song in the user's favorite genre can win even when it contradicts every other preference. My "Calm Acoustic Metal" adversarial profile (metal genre, but wanting calm, acoustic, romantic music) still ranked *Iron Verdict* — a loud, aggressive, non-acoustic metal track — at #1, purely on the genre bonus. In practice this means the system keeps recommending more of what the user already listens to and rarely surfaces great cross-genre matches, which is exactly how real-world filter bubbles form.

A second, subtler bias comes from how the **"energy gap" is calculated.** The linear formula `1.5 × (1 − |target − energy|)` gives users with *extreme* energy targets (near 0.0 or 1.0) a wide, discriminating range of energy scores, while users with *mid-range* targets (around 0.5) see all songs score similarly on energy (the largest possible gap is only ~0.5). So mid-energy listeners get less useful energy differentiation, and their rankings end up dominated by genre and mood. Finally, the model ignores `valence`, `danceability`, and `tempo` entirely, and treats genre/mood as all-or-nothing (a lofi fan gets the same zero for closely-related `ambient` as for `metal`), so users with nuanced or in-between tastes are served poorly.

---

## 7. Evaluation  

**Profiles tested.** I stress-tested the recommender against six profiles: three realistic tastes — **High-Energy Pop** (pop/happy/0.9), **Chill Lofi** (lofi/chill/0.35/acoustic), and **Deep Intense Rock** (rock/intense/0.9) — and three adversarial edge cases — **Calm Acoustic Metal** (conflicting preferences), **Unknown Genre & Mood** (`kpop`/`euphoric`, neither in the catalog), and **Sparse: Energy Only** (a single preference). For each I ran `python -m src.main` and inspected the top 5 songs, their scores, and the reasons behind them, checking whether the right songs surfaced and whether the ordering matched my intuition. The full outputs are in the README's *Experiments You Tried* section.

**What surprised me.** Two things. First, a genre match could completely override three contradicting preferences — the metal track winning the "calm acoustic" profile was more extreme than I expected and made the genre-weight bias concrete. Second, when I gave an unknown genre and mood, the system still returned a confident-looking top 5 with no indication it had found nothing matching the user's stated taste; I expected some visible "weak match" signal, but the scores just quietly dropped.

**Pairwise comparisons.**

- **High-Energy Pop vs. Chill Lofi** — These are near-opposites and the outputs confirm it: the pop profile surfaces bright, non-acoustic, high-energy tracks (*Sunrise City*, *Gym Hero*), while the lofi profile shifts entirely toward calm, acoustic, low-energy songs (*Library Rain*, *Midnight Coding*). Almost no overlap in the two top-5 lists, which is what you'd want from genuinely different tastes.
- **High-Energy Pop vs. Deep Intense Rock** — Both want high energy (0.9) and non-acoustic music, so their lower ranks *overlap* (both include *Neon Horizon* and other high-energy tracks). The difference is at the top: each profile's own genre wins #1 (*Sunrise City* vs *Storm Runner*), showing the genre bonus is what separates two otherwise-similar high-energy users.
- **Chill Lofi vs. Deep Intense Rock** — Opposite on every axis (energy 0.35 vs 0.9, acoustic vs non-acoustic), and the results are cleanly disjoint: soft acoustic songs for one, loud aggressive songs for the other. This is the clearest "the preferences are actually doing something" comparison.
- **Deep Intense Rock vs. Sparse: Energy Only** — Both favor high-energy songs, so *Iron Verdict*, *Gym Hero*, and *Storm Runner* appear in both lists. But the rock profile *reorders* them using its genre + mood bonuses (rock/intense jumps to #1), while the energy-only profile ranks them purely by raw energy closeness. This isolates exactly what the genre/mood rules add on top of the energy signal.
- **Chill Lofi vs. Calm Acoustic Metal** — Both ask for low energy and acoustic music, and indeed calm acoustic tracks (*Elegy in Grey*, *Spacewalk Thoughts*, *Library Rain*) appear in both. The revealing difference: the metal profile's genre bonus drags the loud, non-acoustic *Iron Verdict* to #1 anyway, whereas the lofi profile's genre choice *agrees* with its other preferences, so its #1 is a true all-around match. Same acoustic/energy request, very different quality of result — a direct illustration of the genre-override bias.

---

## 8. Future Work  

If I kept building VibeMatch, I would:

1. **Fix the genre over-priority.** Right now one genre match can beat every other signal. I would lower the genre bonus or reduce a song's score when it clearly contradicts the user's energy and mood, so the results stop forming a filter bubble.
2. **Use the features I'm ignoring.** Valence, danceability, and tempo are already in the data. Adding them (and scaling tempo to 0–1 first) would let the model tell apart songs that currently look identical.
3. **Give partial credit for similar genres and moods.** Instead of all-or-nothing, treat `ambient` as "close to" `lofi` so users with in-between tastes get better matches. I'd also add a "no strong match found" message when nothing really fits.

---

## 9. Personal Reflection  

**Biggest learning moment.** My biggest "aha" was seeing that a recommender is really two separate jobs: scoring one song, and ranking the whole list. Once I split those into two functions, everything got easier to test and change. I also learned how much a single weight can matter — the adversarial "calm acoustic metal" profile showed me that my +2.0 genre bonus could completely override three other preferences, which is exactly how real filter bubbles form.

**Using AI tools.** AI coding help was great for moving fast — writing the CSV loader, formatting the terminal output, and suggesting adversarial test profiles I wouldn't have thought of. But I had to double-check it. It got an import path wrong (`from recommender` vs `from src.recommender`) that broke the run command, and I needed to verify the scoring math by hand against my worked example before trusting the numbers. The lesson was to treat AI output as a draft, then run it and check the results myself.

**What surprised me.** I was surprised how much a handful of simple `if` statements and one distance formula could "feel" like a real recommendation. There's no machine learning here, yet the ranked lists with reasons look convincing. That made me realize how much of a product's "smart" feel can come from clear rules and good explanations — and also how easily a simple, confident-looking system can hide a bias.

**What I'd try next.** I'd extend the profile to include more features (valence, danceability), add a bit of "exploration" so the list isn't always the same safe genre, and try learning the weights from example ratings instead of picking them by hand. That would be a small step toward how services like Spotify actually work.
