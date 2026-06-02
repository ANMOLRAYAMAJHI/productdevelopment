"""
Sentiment Analysis module for the Helpdesk System
Uses TextBlob for basic sentiment analysis
"""
from textblob import TextBlob
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Analyzes sentiment of ticket messages"""
    
    POSITIVE_THRESHOLD = 0.1
    NEGATIVE_THRESHOLD = -0.1
    
    @staticmethod
    def analyze(text):
        """
        Analyze sentiment of text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Contains sentiment (str) and polarity (float)
        """
        try:
            if not text or len(text.strip()) == 0:
                return {'sentiment': 'Neutral', 'polarity': 0.0}
            
            # Create TextBlob and get polarity
            blob = TextBlob(str(text))
            polarity = blob.sentiment.polarity
            
            # Classify sentiment based on polarity
            if polarity > SentimentAnalyzer.POSITIVE_THRESHOLD:
                sentiment = 'Positive'
            elif polarity < SentimentAnalyzer.NEGATIVE_THRESHOLD:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
            
            logger.info(f'Sentiment analysis: {sentiment} (polarity: {polarity})')
            
            return {
                'sentiment': sentiment,
                'polarity': round(polarity, 3)
            }
        except Exception as e:
            logger.error(f'Error analyzing sentiment: {str(e)}')
            return {'sentiment': 'Neutral', 'polarity': 0.0}
    
    @staticmethod
    def get_priority(sentiment):
        """
        Determine priority based on sentiment
        
        Args:
            sentiment (str): Sentiment classification
            
        Returns:
            str: Priority level (Normal or Urgent)
        """
        if sentiment == 'Negative':
            return 'Urgent'
        return 'Normal'
    
    @staticmethod
    def analyze_batch(texts):
        """
        Analyze multiple texts at once
        
        Args:
            texts (list): List of texts to analyze
            
        Returns:
            list: List of sentiment analysis results
        """
        return [SentimentAnalyzer.analyze(text) for text in texts]
