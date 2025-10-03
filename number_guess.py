#!/usr/bin/env python3
"""
number_guess.py
Single-file Number Guessing game.

Usage:
    python3 number_guess.py
"""

import json
import os
import random
import time

SCORES_FILE = "scores.json"

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_score(name, attempts, time_taken, difficulty):
    scores = load_scores()
    scores.append({
        "name": name,
        "attempts": attempts,
        "time_taken": round(time_taken, 2),
        "difficulty": difficulty,
        "timestamp": int(time.time())
    })
    # keep only best 20 by attempts then time
    scores = sorted(scores, key=lambda s: (s["attempts"], s["time_taken"]))[:20]
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

def show_leaderboard():
    scores = load_scores()
    if not scores:
        print("\nNo leaderboard yet — be the first!\n")
        return
    print("\n--- Leaderboard (best first) ---")
    for i, s in enumerate(scores, 1):
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(s["timestamp"]))
        print(f"{i}. {s['name']:12} | attempts: {s['attempts']:2} | time: {s['time_taken']:5}s | {s['difficulty']:6} | {ts}")
    print("-------------------------------\n")

def ask_int(prompt, minv=None, maxv=None):
    while True:
        val = input(prompt).strip()
        if not val:
            print("Please enter a value.")
            continue
        if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
            n = int(val)
            if (minv is not None and n < minv) or (maxv is not None and n > maxv):
                rng = f" between {minv} and {maxv}" if minv is not None and maxv is not None else ""
                print(f"Enter an integer{rng}.")
                continue
            return n
        print("That's not an integer. Try again.")

def choose_difficulty():
    print("Choose difficulty:")
    print("  1) Easy   (range 1-10, attempts 6)")
    print("  2) Medium (range 1-50, attempts 7)")
    print("  3) Hard   (range 1-100, attempts 8)")
    print("  4) Custom (you choose range and attempts)")
    while True:
        choice = input("Enter 1/2/3/4: ").strip()
        if choice == "1":
            return ("Easy", 1, 10, 6)
        if choice == "2":
            return ("Medium", 1, 50, 7)
        if choice == "3":
            return ("Hard", 1, 100, 8)
        if choice == "4":
            low = ask_int("Enter lower bound (integer): ")
            high = ask_int("Enter upper bound (integer, > lower): ")
            if high <= low:
                print("Upper bound must be greater than lower bound.")
                continue
            attempts = ask_int("Enter max attempts (>=1): ", minv=1)
            return ("Custom", low, high, attempts)
        print("Invalid choice, try again.")

def play_round(name=None):
    difficulty, low, high, max_attempts = choose_difficulty()
    secret = random.randint(low, high)
    print(f"\nI've picked a number between {low} and {high}. You have {max_attempts} attempts. Good luck!\n")
    start = time.time()
    attempts = 0
    guessed = False
    last_diff = None

    while attempts < max_attempts:
        attempts += 1
        guess = ask_int(f"[Attempt {attempts}/{max_attempts}] Your guess: ", minv=low, maxv=high)
        if guess == secret:
            guessed = True
            break
        # Hint system
        if guess < secret:
            hint = "higher"
        else:
            hint = "lower"
        # extra feedback: closeness
        diff = abs(secret - guess)
        closeness = ""
        if diff == 0:
            closeness = ""
        elif diff <= max(1, (high - low) // 20):
            closeness = " (very close!)"
        elif diff <= max(1, (high - low) // 5):
            closeness = " (close)"
        print(f"Nope — try {hint}.{closeness}\n")
        last_diff = diff

    time_taken = time.time() - start
    if guessed:
        print(f"\n🎉 Correct! The number was {secret}.")
        print(f"Attempts: {attempts}, Time: {round(time_taken,2)}s, Difficulty: {difficulty}")
        if not name:
            name = input("Enter your name for the leaderboard (or press Enter to stay anonymous): ").strip() or "Anon"
        save_score(name, attempts, time_taken, difficulty)
    else:
        print(f"\n☹️ Out of attempts! The number was {secret}. Better luck next time.")
    print()
    return guessed, attempts, time_taken, difficulty

def main():
    print("=== Number Guessing Game ===")
    player = input("What's your name? (press Enter for 'Player'): ").strip() or "Player"

    while True:
        print("\nMenu:")
        print("  1) Play")
        print("  2) Leaderboard")
        print("  3) About / Help")
        print("  4) Exit")
        choice = input("Choose 1/2/3/4: ").strip()

        if choice == "1":
            play_round(name=player)
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            print("\nAbout:")
            print("  Guess the secret number in limited attempts. Hints will tell you higher/lower.")
            print("  Leaderboard stores best scores in 'scores.json' in the same folder.")
            print("  Tip: choosing a smaller range makes it easier; custom mode lets you practice.")
        elif choice == "4":
            print("Goodbye — thanks for playing!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
