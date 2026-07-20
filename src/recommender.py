import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.

    Numeric columns are converted from strings so the scoring logic can do
    math on them later: `id` and `tempo_bpm` become ints, and the 0-1 audio
    features become floats. Everything else stays a string.

    Required by src/main.py
    """
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = dict(row)
            for field in int_fields:
                if field in song:
                    song[field] = int(song[field])
            for field in float_fields:
                if field in song:
                    song[field] = float(song[field])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences (the Algorithm Recipe).

    Points are additive, starting from 0 (max possible = 5.0):
      - Genre match      : +2.0
      - Mood match       : +1.0
      - Energy similarity : up to +1.5, based on how CLOSE the song's energy
                            is to the target (rewards nearness, not magnitude)
      - Acoustic fit      : up to +0.5

    Returns a tuple of (score, reasons), where `reasons` is a list of
    human-readable strings explaining which rules fired and how many points
    they awarded (e.g. "genre match: lofi (+2.0)").

    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Rule 1: Genre match (+2.0)
    fav_genre = user_prefs.get("favorite_genre")
    if fav_genre is not None and song.get("genre") == fav_genre:
        score += 2.0
        reasons.append(f"genre match: {fav_genre} (+2.0)")

    # Rule 2: Mood match (+1.0)
    fav_mood = user_prefs.get("favorite_mood")
    if fav_mood is not None and song.get("mood") == fav_mood:
        score += 1.0
        reasons.append(f"mood match: {fav_mood} (+1.0)")

    # Rule 3: Energy similarity (up to +1.5) — closer to target = more points
    target_energy = user_prefs.get("target_energy")
    if target_energy is not None and "energy" in song:
        energy_points = 1.5 * (1.0 - abs(target_energy - song["energy"]))
        score += energy_points
        reasons.append(
            f"energy close to {target_energy} (+{energy_points:.2f})"
        )

    # Rule 4: Acoustic fit (up to +0.5)
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None and "acousticness" in song:
        fit = song["acousticness"] if likes_acoustic else 1.0 - song["acousticness"]
        acoustic_points = 0.5 * fit
        score += acoustic_points
        label = "acoustic feel" if likes_acoustic else "non-acoustic feel"
        reasons.append(f"{label} (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
