import requests
from PIL import Image
from io import BytesIO
import base64

# Constants
IMAGE_TO_TEXT_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
SENTIMENT_API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
IMAGE_API_KEY = "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"  # Image-to-Text API Key
SENTIMENT_API_KEY = "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"  # Sentiment Analysis API Key

def get_image_description(image_url):
    """Fetches an image from a URL and generates a description using the BLIP model."""
    try:
        # Fetch the image
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Open the image
        image = Image.open(BytesIO(response.content))

        # Convert image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        headers = {"Authorization": f"Bearer {IMAGE_API_KEY}", "Content-Type": "application/json"}
        data = {"inputs": img_str}

        # Send the image data
        response = requests.post(
            IMAGE_TO_TEXT_API_URL,
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            response_data = response.json()
            # Debugging: Print the response to understand its structure
            print("Image-to-Text API Response:", response_data)
            
            if isinstance(response_data, list) and len(response_data) > 0:
                description = response_data[0].get('generated_text', 'No description available')
            else:
                description = "Error: Unexpected response format"
        else:
            description = "Error: Unable to retrieve description"
            print("Image-to-Text API Response:", response.text)
        
    except requests.RequestException as e:
        description = f"Network error: {e}"
    except IOError as e:
        description = f"Image error: {e}"
    
    return description

def analyze_sentiment(text):
    """Analyzes the sentiment of the given text using the DistilBERT model."""
    headers = {
        "Authorization": f"Bearer {SENTIMENT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"inputs": text}
    
    try:
        response = requests.post(
            SENTIMENT_API_URL,
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            # Debugging: Print the response to understand its structure
            print("Sentiment API Response:", result)
            
            if isinstance(result, list) and len(result) > 0:
                sentiment_data = result[0]
                sentiment_label = sentiment_data[0].get('label', 'No sentiment label found')
            else:
                sentiment_label = "Error: Unexpected response format"
        else:
            sentiment_label = f"Error: Received status code {response.status_code}"
            print("Response Text:", response.text)
    except requests.RequestException as e:
        sentiment_label = f"Network error: {e}"
    
    return sentiment_label

def main():
    """Main function to drive the script."""
    image_url = input("Enter the image URL: ")
    description = get_image_description(image_url)
    
    # Check if description was retrieved successfully before sentiment analysis
    if "No description available" not in description:
        sentiment = analyze_sentiment(description)
    else:
        sentiment = "Unable to analyze sentiment due to description error"
    
    print(f"Image Description: {description}")
    print(f"Sentiment: {sentiment}")

if __name__ == "__main__":
    main()
