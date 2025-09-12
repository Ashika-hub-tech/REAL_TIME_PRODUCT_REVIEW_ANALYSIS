# Importing required libraries
import streamlit as st  # For building the Streamlit web app
import pandas as pd  # For data manipulation and analysis
from transformers import pipeline  # For using pre-trained NLP models
import plotly.express as px  # For creating interactive plots
import requests  # For making HTTP requests (used for web scraping)
from bs4 import BeautifulSoup  # For parsing HTML (used for scraping reviews)

# Set Streamlit page configurations
st.set_page_config(
    page_title="Sentiment Analysis tool",  # Page title
    page_icon="😊",  # Page icon
    layout="wide"  # Full-width layout
)

# Display app title
st.title("Real Time Brand Monitoring and Interactive Analysis💕")

# Global list to store emotion results
detected_emotions_list = []

# Load emotion detection pipeline using Roberta model fine-tuned on GoEmotions dataset
emotion = pipeline("text-classification",
                   model="SamLowe/roberta-base-go_emotions",
                   device=-1)  # Use CPU for inference
emotion.model.to("cpu")  # Explicitly load model weights off meta device into CPU

# Function to read and process uploaded CSV file
def process_csv_input(file):
    encoding_list = ['utf-8', 'latin-1', 'ISO-8859-1']  # Possible encodings

    for encoding in encoding_list:
        try:
            df = pd.read_csv(file, encoding=encoding)  # Try reading CSV with each encoding
            st.success(f"CSV file successfully loaded using encoding: {encoding}")
            st.table(df)  # Display uploaded data in table format
            sentences = df["Comment"].tolist()  # Extract comments from 'Comment' column
            perform_emotion_analysis(sentences)  # Perform emotion analysis
            break
        except UnicodeDecodeError:
            st.warning(f"Failed to decode using encoding: {encoding}")
            continue
    else:
        st.error("Unable to decode the CSV file using any of the tried encodings. Please check the file encoding.")

# Function to perform emotion detection on list of sentences
def perform_emotion_analysis(sentences):
    detected_emotions_list.clear()  # Clear previous results
    for sentence in sentences:
        emotion_labels = emotion(sentence)  # Predict emotion using pipeline
        detected_emotion = emotion_labels[0]['label']  # Extract top emotion label
        detected_emotions_list.append((sentence, detected_emotion))  # Append to global list

    # Display results
    st.write("Emotion Analysis Results:")
    result_df = pd.DataFrame(detected_emotions_list, columns=["Comment", "Detected_Emotion"])
    st.table(result_df)

# Function to plot bar and pie chart of emotions
def plot_emotions(filename, product_name):
    st.header(f"Detected Emotions Distribution for {filename}")

    if detected_emotions_list:
        df_emotions = pd.DataFrame(detected_emotions_list, columns=['Comment', 'Detected_Emotion'])

        # Count occurrences of each emotion
        emotion_counts = df_emotions['Detected_Emotion'].value_counts().reset_index()
        emotion_counts.columns = ['Emotion', 'Count']

        # Classify each emotion into Positive, Negative, or Neutral
        positive_emotions = ['admiration', 'amusement', 'approval', 'caring', 'desire', 'excitement', 'gratitude', 'joy', 'love', 'optimism', 'pride', 'realization', 'relief']
        negative_emotions = ['anger', 'annoyance', 'disappointment', 'disapproval', 'disgust', 'embarrassment', 'fear', 'grief', 'nervousness', 'remorse', 'sadness']
        df_emotions['Emotion Category'] = df_emotions['Detected_Emotion'].apply(lambda x: 'Positive' if x in positive_emotions else ('Negative' if x in negative_emotions else 'Neutral'))

        # Count emotions per category
        emotion_category_counts = df_emotions['Emotion Category'].value_counts().reset_index()
        emotion_category_counts.columns = ['Emotion Category', 'Count']

        # Show bar chart
        fig_bar = px.bar(emotion_category_counts, x='Emotion Category', y='Count', labels={'Emotion Category': 'Emotion Category', 'Count': 'Count'}, color='Emotion Category')
        st.plotly_chart(fig_bar)

        # Show pie chart
        fig_pie = px.pie(emotion_category_counts, values='Count', names='Emotion Category', title=f'Detected Emotions Distribution for {filename}', color='Emotion Category')
        st.plotly_chart(fig_pie)
    else:
        st.info("No emotions detected yet.")

# Function to scrape reviews from Flipkart product page
def scrape_reviews_and_save_to_csv(product_name, url):
    headers = {
        'User-Agent': 'Your_User_Agent_Here',  # Required header to avoid bot detection
        'Accept-Language': 'en-us,en;q=0.5'
    }

    customer_names = []
    review_title = []
    ratings = []
    comments = []

    # Loop over paginated review pages (1 to 43)
    for i in range(1, 44):
        page = requests.get(url.format(i), headers=headers)  # Request review page
        soup = BeautifulSoup(page.content, 'html.parser')  # Parse page content

        # Extract customer names
        names = soup.find_all('p', class_='_2sc7ZR')
        for name in names:
            customer_names.append(name.get_text(strip=True))

        # Extract review titles
        titles = soup.find_all('p', class_='_2-N8zT')
        for title in titles:
            review_title.append(title.get_text(strip=True))

        # Extract star ratings
        ratings_all = soup.find_all('div', class_='col _2wzgFH K0kLPL')
        for rating in ratings_all:
            ratings.append(rating.div.text.strip())

        # Extract full review comments
        comments_all = soup.find_all('div', class_='t-ZTKy')
        for comment in comments_all:
            comment_text = comment.div.div.get_text(strip=True)
            comments.append(comment_text)

    # Truncate lists to same length
    min_length = min(len(customer_names), len(review_title), len(ratings), len(comments))
    customer_names = customer_names[:min_length]
    review_title = review_title[:min_length]
    ratings = ratings[:min_length]
    comments = comments[:min_length]

    # Save to CSV
    data = {
        'Customer Name': customer_names,
        'Review Title': review_title,
        'Rating': ratings,
        'Comment': comments
    }

    df = pd.DataFrame(data)
    filename = f'{product_name}_reviews.csv'
    df.to_csv(filename, index=False)
    return filename  # Return saved file path

# Main function of the Streamlit app
def main():
    st.header("Scrape Reviews and Save to CSV")

    # Input fields for product scraping
    product_name = st.text_input("Enter Product Name:")
    url = st.text_input("Enter URL for Scraping (Flipkart URL)", value='https://www.flipkart.com/motorola-g84-5g-viva-magneta-256-gb/product-reviews/itmed938e33ffdf5?pid=MOBGQFX672GDDQAQ&lid=LSTMOBGQFX672GDDQAQSSIAM2&marketplace=FLIPKART&page={}')

    # Button to trigger scraping
    if st.button("Scrape Reviews"):
        if product_name and url:
            st.info("Scraping reviews and saving to CSV...")
            filename = scrape_reviews_and_save_to_csv(product_name, url)
            st.success(f"Reviews scraped and saved to {filename} successfully!")
            plot_emotions(filename, product_name)  # Plot emotion distribution
        else:
            st.warning("Please enter both product name and URL.")

    # CSV upload for custom review file
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        if st.button("Process CSV Input"):
            process_csv_input(uploaded_file)
            plot_emotions(uploaded_file.name, uploaded_file.name)  # Visualize results

    # Manual text input for emotion analysis
    st.header("Text Input for Emotion Analysis")
    text_input = st.text_area("Type or paste your text here:", height=200)
    if st.button("Analyze Text"):
        if text_input.strip() != "":
            sentences = [text_input]
            perform_emotion_analysis(sentences)
            plot_emotions("Input Text", "Input Text")  # Plot results
        else:
            st.warning("Please input some text to analyze.")

# Entry point of the script
if __name__ == "__main__":
    main()



