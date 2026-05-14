# =============================================
# PROJECT — Smart Word Counter
# =============================================

def clean_text(text):
    text = text.lower()
    text = text.strip()
    # remove common punctuation
    for char in [".", ",", "!", "?", ":", ";", "'", '"']:
        text = text.replace(char, "")
    return text

def count_words(text):
    words = text.split()
    word_freq = {}

    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    return word_freq

def top_words(word_freq, n=5):
    # sort by frequency — highest first
    sorted_words = sorted(word_freq.items(),
                         key=lambda x: x[1],
                         reverse=True)
    return sorted_words[:n]

def display_results(text, word_freq):
    words = text.split()
    unique = set(words)

    print("\n" + "=" * 40)
    print("         WORD COUNTER RESULTS")
    print("=" * 40)
    print(f"Total words      : {len(words)}")
    print(f"Unique words     : {len(unique)}")
    print(f"Longest word     : {max(words, key=len)}")
    print(f"Shortest word    : {min(words, key=len)}")
    print(f"Average length   : {sum(len(w) for w in words) // len(words)}")
    print("-" * 40)
    print("Top 5 most used words:")
    for i, (word, count) in enumerate(top_words(word_freq)):
        bar = "█" * count
        print(f"{i+1}. {word:15} {count:3}x  {bar}")
    print("=" * 40)

def save_results(text, word_freq, filename="word_count_result.txt"):
    with open(filename, "w") as f:
        f.write("WORD COUNTER RESULTS\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total words: {len(text.split())}\n")
        f.write(f"Unique words: {len(set(text.split()))}\n\n")
        f.write("All words and frequencies:\n")
        for word, count in sorted(word_freq.items()):
            f.write(f"{word}: {count}\n")
    print(f"\nResults saved to {filename}")

# --- MAIN PROGRAM ---
def main():
    print("=" * 40)
    print("     SAMIULLAH'S WORD COUNTER")
    print("=" * 40)
    print("Enter your text below (press Enter twice when done):")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    if not lines:
        print("No text entered.")
        return

    raw_text = " ".join(lines)
    cleaned = clean_text(raw_text)
    word_freq = count_words(cleaned)

    display_results(cleaned, word_freq)
    save_results(cleaned, word_freq)

main()