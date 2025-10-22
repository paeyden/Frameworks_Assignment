import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re

st.title("CORD-19 Data Explorer 🧬")
st.write("An interactive app to explore COVID-19 research papers metadata.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('metadata.csv')
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(x.split()))
    return df

df = load_data()
st.success("Dataset loaded successfully!")

# Show sample
if st.checkbox("Show dataset sample"):
    st.dataframe(df.head(10))

# Year range filter
year_min, year_max = int(df['year'].min()), int(df['year'].max())
year_range = st.slider("Select year range", year_min, year_max, (year_min, year_max))
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.subheader("Publications Over Time")
papers_by_year = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=papers_by_year.index, y=papers_by_year.values, ax=ax)
ax.set_title('Number of Publications Over Time')
ax.set_xlabel('Year')
ax.set_ylabel('Publications')
st.pyplot(fig)

st.subheader("Top 10 Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_journals.values, y=top_journals.index, hue=top_journals.index, legend=False, palette='viridis', ax=ax)
ax.set_title('Top 10 Journals')
ax.set_xlabel('Publications')
ax.set_ylabel('Journal')
st.pyplot(fig)

st.subheader("Word Cloud of Paper Titles")
all_titles = ' '.join(filtered_df['title'].dropna().tolist()).lower()
words = re.findall(r'\b\w+\b', all_titles)
word_counts = Counter(words)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

st.subheader("Distribution of Papers by Source")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(y='source_x', data=filtered_df, hue='source_x', legend=False, palette='magma', ax=ax,
              order=filtered_df['source_x'].value_counts().index)
ax.set_title('Distribution of Papers by Source')
ax.set_xlabel('Number of Papers')
ax.set_ylabel('Source')
st.pyplot(fig)
