#!/usr/bin/env python3
"""
Sample data script for Meghalaya Tourism Bot.
This script helps populate MongoDB with sample tourism documents for testing.
"""

import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

class SampleDataGenerator:
    """Generate sample tourism data for Meghalaya."""
    
    def __init__(self):
        """Initialize the sample data generator."""
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.mongodb_database = os.getenv("MONGODB_DATABASE", "meghalaya_tourism")
        self.mongodb_collection = os.getenv("MONGODB_COLLECTION", "tourism_documents")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.mongodb_uri or not self.openai_api_key:
            raise ValueError("MONGODB_URI and OPENAI_API_KEY must be set in environment variables")
        
        # Initialize clients
        self.mongo_client = MongoClient(self.mongodb_uri)
        self.database = self.mongo_client[self.mongodb_database]
        self.collection = self.database[self.mongodb_collection]
        self.openai_client = OpenAI(api_key=self.openai_api_key)
    
    def get_sample_documents(self) -> List[Dict[str, Any]]:
        """Get sample tourism documents about Meghalaya."""
        return [
            {
                "title": "Living Root Bridges of Meghalaya",
                "content": """
                The Living Root Bridges of Meghalaya are a unique natural phenomenon found in the Khasi and Jaintia Hills. 
                These bridges are created by training the roots of the Ficus elastica tree across rivers and streams. 
                The most famous living root bridge is the double-decker bridge in Nongriat village, which takes about 3-4 hours to reach from Cherrapunji. 
                These bridges can support the weight of 50 or more people and become stronger over time. 
                The process of creating these bridges takes 15-30 years and requires careful maintenance by the local communities.
                """,
                "metadata": {
                    "type": "attraction",
                    "location": "Nongriat, Cherrapunji",
                    "tags": ["nature", "unique", "trekking", "unesco"],
                    "difficulty": "moderate",
                    "best_time": "October to May"
                }
            },
            {
                "title": "Cherrapunji - The Wettest Place on Earth",
                "content": """
                Cherrapunji, also known as Sohra, holds the record for the highest annual rainfall in the world. 
                Located in the East Khasi Hills, it receives an average of 11,777 mm of rainfall annually. 
                The town is famous for its spectacular waterfalls, including the Seven Sisters Falls, Nohkalikai Falls, and Dainthlen Falls. 
                The landscape is characterized by deep gorges, limestone caves, and lush green valleys. 
                Cherrapunji offers breathtaking views of the Bangladesh plains and is a paradise for nature lovers and photographers.
                """,
                "metadata": {
                    "type": "attraction",
                    "location": "Cherrapunji, East Khasi Hills",
                    "tags": ["waterfalls", "rainfall", "photography", "nature"],
                    "best_time": "May to October",
                    "activities": ["sightseeing", "photography", "trekking"]
                }
            },
            {
                "title": "Nongkrem Festival - Khasi Harvest Festival",
                "content": """
                Nongkrem Festival is one of the most important festivals of the Khasi tribe, celebrated annually in November. 
                The festival is held at Smit, near Shillong, and lasts for five days. 
                It is a harvest festival that includes traditional dances, music, and rituals to thank the gods for a good harvest. 
                The highlight is the Pomblang ceremony, where a goat is sacrificed to appease the deity. 
                The festival features the famous Nongkrem dance performed by unmarried girls in traditional attire, 
                and the Shad Suk Mynsiem dance performed by men. Visitors can witness the rich cultural heritage and traditional customs of the Khasi people.
                """,
                "metadata": {
                    "type": "festival",
                    "location": "Smit, near Shillong",
                    "tags": ["culture", "harvest", "dance", "traditional"],
                    "month": "November",
                    "duration": "5 days"
                }
            },
            {
                "title": "Mawsynram - Wettest Place on Earth",
                "content": """
                Mawsynram, located in the East Khasi Hills, is recognized as the wettest place on Earth, 
                receiving an average annual rainfall of 11,872 mm. The village is situated at an altitude of 1,400 meters 
                and is surrounded by lush green hills and valleys. The unique geographical location and monsoon winds 
                create the perfect conditions for heavy rainfall. Mawsynram is famous for its living root bridges, 
                limestone caves, and spectacular waterfalls. The village offers a peaceful retreat for nature enthusiasts 
                and provides opportunities for trekking and exploring the pristine natural beauty of Meghalaya.
                """,
                "metadata": {
                    "type": "attraction",
                    "location": "Mawsynram, East Khasi Hills",
                    "tags": ["rainfall", "nature", "trekking", "caves"],
                    "altitude": "1400m",
                    "best_time": "May to October"
                }
            },
            {
                "title": "Shillong - The Scotland of the East",
                "content": """
                Shillong, the capital of Meghalaya, is often called the "Scotland of the East" due to its rolling hills, 
                pine forests, and pleasant climate. The city is located at an altitude of 1,496 meters and offers 
                a perfect blend of urban amenities and natural beauty. Popular attractions include Ward's Lake, 
                Elephant Falls, Shillong Peak, and the Don Bosco Museum. The city is known for its vibrant music scene, 
                with many local bands and musicians. Shillong serves as the gateway to Meghalaya and offers excellent 
                accommodation, dining, and shopping options for tourists. The city has a cosmopolitan atmosphere with 
                a mix of traditional Khasi culture and modern influences.
                """,
                "metadata": {
                    "type": "city",
                    "location": "Shillong, East Khasi Hills",
                    "tags": ["capital", "music", "shopping", "dining"],
                    "altitude": "1496m",
                    "best_time": "March to June, September to November"
                }
            },
            {
                "title": "Garo Hills - Tribal Culture and Nature",
                "content": """
                The Garo Hills region in western Meghalaya is home to the Garo tribe and offers a unique cultural experience. 
                The area is characterized by rolling hills, dense forests, and traditional villages. 
                Popular attractions include the Nokrek National Park, which is a UNESCO Biosphere Reserve, 
                and the Siju Caves, known for their limestone formations. The region is famous for its traditional 
                Wangala festival, which celebrates the harvest season. The Garo Hills offer opportunities for wildlife 
                spotting, trekking, and experiencing the traditional lifestyle of the Garo people. 
                The area is less touristy compared to other parts of Meghalaya, making it perfect for offbeat travel experiences.
                """,
                "metadata": {
                    "type": "region",
                    "location": "Garo Hills, Western Meghalaya",
                    "tags": ["tribal", "wildlife", "trekking", "offbeat"],
                    "best_time": "October to April",
                    "activities": ["wildlife", "trekking", "cultural"]
                }
            }
        ]
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using OpenAI."""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-large",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []
    
    def create_vector_documents(self) -> List[Dict[str, Any]]:
        """Create documents with embeddings for vector search."""
        sample_docs = self.get_sample_documents()
        vector_docs = []
        
        for doc in sample_docs:
            # Generate embedding for the content
            embedding = self.generate_embeddings(doc["content"])
            
            if embedding:
                vector_doc = {
                    "page_content": doc["content"],
                    "metadata": doc["metadata"],
                    "embedding": embedding
                }
                vector_docs.append(vector_doc)
        
        return vector_docs
    
    def populate_database(self):
        """Populate the database with sample documents."""
        print("Creating sample documents with embeddings...")
        
        vector_docs = self.create_vector_documents()
        
        if not vector_docs:
            print("No documents created. Check your OpenAI API key.")
            return False
        
        try:
            # Clear existing documents (optional)
            # self.collection.delete_many({})
            
            # Insert new documents
            result = self.collection.insert_many(vector_docs)
            print(f"Successfully inserted {len(result.inserted_ids)} documents")
            
            # Create vector search index (this needs to be done in MongoDB Atlas)
            print("\nNote: You need to create a vector search index in MongoDB Atlas:")
            print("1. Go to your MongoDB Atlas dashboard")
            print("2. Navigate to your cluster")
            print("3. Go to Search tab")
            print("4. Create a vector search index with:")
            print("   - Field name: 'embedding'")
            print("   - Dimensions: 3072 (for text-embedding-3-large)")
            print("   - Similarity: cosine")
            
            return True
            
        except Exception as e:
            print(f"Error inserting documents: {e}")
            return False
    
    def verify_data(self):
        """Verify that data was inserted correctly."""
        try:
            count = self.collection.count_documents({})
            print(f"Total documents in collection: {count}")
            
            # Show sample document
            sample = self.collection.find_one()
            if sample:
                print(f"Sample document title: {sample['metadata'].get('title', 'N/A')}")
                print(f"Has embedding: {'embedding' in sample}")
            
            return True
            
        except Exception as e:
            print(f"Error verifying data: {e}")
            return False

def main():
    """Main function to populate sample data."""
    print("🏔️ Meghalaya Tourism Bot - Sample Data Generator")
    print("=" * 60)
    
    try:
        generator = SampleDataGenerator()
        
        print("Generating sample tourism documents...")
        if generator.populate_database():
            print("✅ Sample data generated successfully!")
            
            print("\nVerifying data...")
            if generator.verify_data():
                print("✅ Data verification completed!")
                print("\nYour MongoDB is now ready for the Meghalaya Tourism Bot!")
            else:
                print("❌ Data verification failed")
        else:
            print("❌ Failed to generate sample data")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your environment variables and try again.")

if __name__ == "__main__":
    main()
