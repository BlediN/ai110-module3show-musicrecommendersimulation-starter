"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

It defines several taste profiles - three "normal" ones plus a set of
adversarial / edge-case profiles used to stress test the scoring logic -
and prints the top recommendations for each.
"""

from src.recommender import load_songs, recommend_songs


# Distinct, realistic taste profiles
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    # --- Adversarial / edge-case profiles (System Evaluation) ---
    # Internally contradictory: wants calm, acoustic, romantic... but in metal.
    "Conflicting: Calm Acoustic Metal": {
        "favorite_genre": "metal",
        "favorite_mood": "romantic",
        "target_energy": 0.1,
        "likes_acoustic": True,
    },
    # Genre and mood that do not exist in the catalog at all.
    "Unknown Genre & Mood": {
        "favorite_genre": "kpop",
        "favorite_mood": "euphoric",
        "target_energy": 0.6,
        "likes_acoustic": False,
    },
    # Nearly empty profile: only a single, extreme preference is stated.
    "Sparse: Energy Only": {
        "target_energy": 1.0,
    },
}


def print_recommendations(name: str, prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one named profile."""
    print("\n" + "=" * 64)
    print(f"PROFILE: {name}")
    print("=" * 64)
    print("Preferences:", prefs if prefs else "(none)")

    recommendations = recommend_songs(prefs, songs, k=k)
    print(f"\nTop {len(recommendations)} recommendations:")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']}  by {song['artist']}  "
              f"[{song['genre']} / {song['mood']}]")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs, k=5)


if __name__ == "__main__":
    main()
