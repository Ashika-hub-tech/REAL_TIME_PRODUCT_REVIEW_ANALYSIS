# REAL_TIME_PRODUCT_REVIEW_ANALYSIS
Real-time Streamlit tool for scraping Flipkart reviews, detecting customer emotions using HuggingFace Transformers, classifying sentiment (positive/negative/neutral), and visualizing brand perception with interactive charts.

🚀 Features

- 🔍 *Flipkart Review Scraper* – Enter any product URL to scrape reviews (name, title, rating, comment)
- 😊 *Emotion Detection* – Uses SamLowe/roberta-base-go_emotions model to detect emotions in text
- 📊 *Interactive Visualizations* – Bar & Pie charts for emotion categories (Positive / Negative / Neutral)
- ✍ *Manual Text Analysis* – Try customized text snippets for emotion detection
- 💬 *Sentiment Classifier* – Predict user-entered review text sentiment (Positive/Negative/Neutral)
- 📁 *CSV Upload* – Upload your own dataset and visualize emotions instantly

🛠 Tech Stack

| Component      | Tool/Library                                      |
| -------------- | ------------------------------------------------- |
| Web Framework  | Streamlit                                         |
| NLP Model      | HuggingFace Transformers (GoEmotions)             |
| Visualization  | Plotly Express                                    |
| Scraping       | requests, BeautifulSoup                           |
| Data Handling  | pandas                                            |

📦 Installation

```bash
git clone https://github.com/Ashika-hub-tech/REAL_TIME_PRODUCT_REVIEW_ANALYSIS.git
cd <REAL_TIME_PRODUCT_REVIEW_ANALYSIS>

# Create and activate virtual env (optional but recommended)
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

📦 To Create Environment & Install Requirements
conda create -n flipkart311 python=3.11
conda activate flipkart311
pip install streamlit==1.34.0 pandas==2.2.2 transformers==4.41.2 torch==2.3.0 plotly==5.22.0 requests==2.31.0 beautifulsoup4==4.12.3

📦 Run the Application
 streamlit run app.py 

📦 Usage Flow
Scrape reviews
→ Enter product name + Flipkart URL, click Scrape Reviews
→ CSV file is saved and automatic emotion plot is displayed

Upload CSV
→ Upload any CSV file containing a Comment column
→ Emotions are detected & visualized

Manual Text Input (Emotion Detection)
→ Type/paste any sentence and see top emotion outputs

Predict Sentiment (Positive / Negative / Neutral)
→ Enter a review and get its sentiment prediction with visual GIF outputs


