# import  the required libraries and  load the dataset
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
try:
    df = pd.read_csv('metadata.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: The file 'metadata.csv' was not found.")
    exit()
# Part 1: basic data exploration of the dataset,
print(df.head())# to see the first few rows of the dataset
print(df.shape) # to see the number of rows and columns
print(df.info())# to see the data types and non-null values
print(df.isnull().sum())# to see the number of missing values in each column
print(df.describe())# to see the summary statistics of the numerical columns

# -----------------------
# Part 2: Data Cleaning
# -----------------------

# 1. Handle missing values more carefully
# Instead of dropping everything, handle per column
df['title'] = df['title'].fillna("No Title")
df['abstract'] = df['abstract'].fillna("No Abstract")
df['journal'] = df['journal'].fillna("Unknown Journal")
df['source_x'] = df['source_x'].fillna("Unknown Source")

# Drop rows where publish_time is completely missing (since year analysis needs it)
df = df.dropna(subset=['publish_time'])

# 2. Remove duplicates (important!)
df = df.drop_duplicates()

# 3. Convert publish_time to datetime and extract year
df['publish_time'] = pd.to_datetime(df['publish_time'], errors="coerce")
df = df.dropna(subset=['publish_time'])  # drop rows that still fail to convert
df['year'] = df['publish_time'].dt.year

# 4. Create new features
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(x.split()))

# 5. Standardize text data (optional but useful)
df['journal'] = df['journal'].str.strip().str.title()  # consistent capitalization
df['source_x'] = df['source_x'].str.strip().str.title()


#Part 3: data analysis and visualization
#count papers by publication year
papers_by_year = df['year'].value_counts().sort_index()

#top journals in the COVID-19 RESEARCH dataset
top_journals = df['journal'].value_counts().head(10)

# find most frequent words in titles(using simple word frequency)
from collections import Counter
import re
all_titles = ' '.join(df['title'].dropna().tolist()).lower()
words = re.findall(r'\b\w+\b', all_titles)
word_counts = Counter(words)
most_common_words = word_counts.most_common(10)
most_common_words_df = pd.DataFrame(most_common_words, columns=['word', 'count'])

# --- Visualization Section ---

# plot number of publications over time
plt.figure(figsize=(10, 6))
sns.lineplot(x=papers_by_year.index, y=papers_by_year.values)
plt.title('Number of Publications Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.show()

# bar chart of top journals
plt.figure(figsize=(10, 6))
sns.barplot(
    x=top_journals.values,
    y=top_journals.index,
    hue=top_journals.index,   # set hue same as y
    palette='viridis',
    legend=False              # turn off redundant legend
)
plt.title('Top 10 Journals by Number of Publications')
plt.xlabel('Number of Publications')
plt.ylabel('Journal')
plt.show()

# generate word cloud for paper titles
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Paper Titles')
plt.show()

# plot distribution of paper count by source
plt.figure(figsize=(10, 6))
sns.countplot(
    y='source_x',
    data=df,
    order=df['source_x'].value_counts().index,
    hue='source_x',          # set hue same as y
    palette='magma',
    legend=False             # turn off redundant legend
)
plt.title('Distribution of Paper Count by Source')
plt.xlabel('Number of Papers')
plt.ylabel('Source')
plt.show()

