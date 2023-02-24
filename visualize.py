import matplotlib.pyplot as plt
from collections import Counter
import json
import numpy as np


def visualize(file_name, key):
    with open(file_name, 'r', encoding="utf-8") as f:
        data = json.load(f)

    # Get a list of all words from the titles
    words = []
    for item in data:
        words.extend(item[key].lower().split())

    # Count the occurrence of each word
    word_counts = Counter(words)

    # Get the 10 most common words
    top_words = word_counts.most_common(40)

    # Create a horizontal bar chart of the top words
    fig, ax = plt.subplots(figsize=(8, 5))

    # Add color to the bars
    bar_colors = plt.cm.viridis(np.linspace(0, 1, len(top_words)))
    ax.barh([word[0] for word in top_words], [word[1] for word in top_words], color=bar_colors)

    # Add labels to the bars
    for i, word in enumerate(top_words):
        ax.text(word[1]+0.1, i, str(word[1]), ha='left', va='center', fontsize=10)

    # Add a horizontal grid
    ax.grid(axis='x')

    # Add a horizontal line at the mean or median frequency of the words
    mean_freq = sum([word[1] for word in top_words])/len(top_words)
    ax.axvline(x=mean_freq, linestyle='--', color='gray')
    ax.text(mean_freq, -6, 'Mean Frequency', ha='center', va='center', fontsize=10)

    # # Rotate the y-axis labels
    # ax.set_yticklabels([word[0] for word in top_words], rotation=0, fontsize=10)

    # Add title and labels
    ax.set_title("Most Common Words", fontsize=14)
    ax.set_xlabel("Frequency", fontsize=12)
    ax.set_ylabel("Words", fontsize=12)

    # Adjust the layout
    plt.tight_layout()

    # Show the plot
    plt.show()