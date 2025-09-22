"""
Meghalaya Tourism Bot - Minimal Streamlit Application
A basic chatbot for Meghalaya tourism information.
"""

import streamlit as st
import os
from datetime import datetime

def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="Meghalaya Tourism Bot",
        page_icon="🏔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 4px solid #2a5298;
        }
        .user-message {
            background-color: #e3f2fd;
            margin-left: 20%;
        }
        .bot-message {
            background-color: #f5f5f5;
            margin-right: 20%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_stats" not in st.session_state:
        st.session_state.session_stats = {
            "total_queries": 0,
            "start_time": datetime.now()
        }
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🏔️ Meghalaya Tourism Bot</h1>
            <p>Your virtual guide to the beautiful state of Meghalaya, India</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Bot Information")
        st.success("✅ Bot is ready!")
        
        st.subheader("🚀 Quick Actions")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.subheader("📊 Session Statistics")
        stats = st.session_state.session_stats
        st.metric("Total Queries", stats["total_queries"])
        
        st.subheader("💡 Quick Questions")
        quick_questions = [
            "Tell me about living root bridges",
            "What festivals are in Meghalaya?",
            "Best places to visit in Shillong",
            "What to do in Cherrapunji?",
            "Adventure activities in Meghalaya"
        ]
        
        for question in quick_questions:
            if st.button(f"❓ {question}", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": question,
                    "timestamp": datetime.now().isoformat()
                })
                st.rerun()
        
        st.subheader("ℹ️ About")
        st.info("""
        **Meghalaya Tourism Bot** is your AI-powered guide to explore the beautiful state of Meghalaya.
        
        Ask me about:
        • Tourist attractions
        • Cultural festivals
        • Travel tips
        • Local cuisine
        • Adventure activities
        """)
    
    # Main chat interface
    st.markdown("### 💬 Chat with Meghalaya Tourism Bot")
    
    # Display chat messages
    if not st.session_state.messages:
        st.markdown("""
        <div class="chat-message bot-message">
            <h3>Welcome to Meghalaya Tourism Bot! 🏔️</h3>
            <p>I'm here to help you discover the beautiful state of Meghalaya. You can ask me about:</p>
            <ul>
                <li>🏞️ Tourist attractions and places to visit</li>
                <li>🎭 Cultural festivals and traditions</li>
                <li>🏨 Accommodation and travel tips</li>
                <li>🍽️ Local cuisine and dining</li>
                <li>🚗 Transportation and getting around</li>
                <li>📅 Best times to visit</li>
                <li>🎒 Adventure activities and trekking</li>
            </ul>
            <p><strong>What would you like to know about Meghalaya?</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Meghalaya tourism..."):
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            response = generate_response(prompt)
            st.markdown(response)
            
            # Add to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
        
        # Update stats
        st.session_state.session_stats["total_queries"] += 1
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #666; border-top: 1px solid #eee; margin-top: 2rem;">
            <p>🏔️ Meghalaya Tourism Bot | Powered by AI</p>
            <p>Built with ❤️ for travelers exploring the beautiful state of Meghalaya</p>
        </div>
    """, unsafe_allow_html=True)

def generate_response(user_input: str):
    """Generate a response based on user input."""
    # Simple keyword-based responses
    input_lower = user_input.lower()
    
    if "living root bridge" in input_lower:
        return """
        **Living Root Bridges of Meghalaya** 🌿
        
        The Living Root Bridges are one of Meghalaya's most unique attractions! These incredible natural bridges are created by training the roots of the Ficus elastica tree across rivers and streams.
        
        **Key Facts:**
        - Located in Nongriat village near Cherrapunji
        - Takes 15-30 years to create
        - Can support 50+ people
        - Most famous is the double-decker bridge
        - 3-4 hour trek from Cherrapunji
        
        **Best Time to Visit:** October to May
        **Difficulty Level:** Moderate to challenging trek
        
        These bridges are a testament to the harmony between nature and human ingenuity!
        """
    
    elif "festival" in input_lower:
        return """
        **Festivals of Meghalaya** 🎭
        
        Meghalaya celebrates several vibrant festivals throughout the year:
        
        **Nongkrem Festival (November)**
        - 5-day harvest festival
        - Traditional dances and rituals
        - Held at Smit near Shillong
        
        **Wangala Festival (October-November)**
        - Garo tribe harvest festival
        - Traditional music and dance
        - Celebrated in Garo Hills
        
        **Behdienkhlam Festival (July)**
        - Jaintia tribe festival
        - Colorful processions
        - Traditional sports and games
        
        **Shad Suk Mynsiem (April)**
        - Khasi thanksgiving festival
        - Traditional dances
        - Community celebrations
        
        Each festival offers a unique glimpse into Meghalaya's rich cultural heritage!
        """
    
    elif "shillong" in input_lower:
        return """
        **Shillong - The Scotland of the East** 🏔️
        
        Shillong, the capital of Meghalaya, is often called the "Scotland of the East" due to its rolling hills, pine forests, and pleasant climate.
        
        **Top Attractions:**
        - **Ward's Lake** - Beautiful lake with boating
        - **Elephant Falls** - Three-tiered waterfall
        - **Shillong Peak** - Highest point with panoramic views
        - **Don Bosco Museum** - Cultural heritage center
        - **Police Bazaar** - Shopping and dining hub
        
        **Best Time to Visit:** March to June, September to November
        **Altitude:** 1,496 meters
        **Specialty:** Music scene and local bands
        
        Shillong serves as the perfect gateway to explore Meghalaya!
        """
    
    elif "cherrapunji" in input_lower:
        return """
        **Cherrapunji - The Wettest Place on Earth** 💧
        
        Cherrapunji (Sohra) holds the record for the highest annual rainfall in the world, receiving an average of 11,777 mm of rainfall annually!
        
        **Must-Visit Waterfalls:**
        - **Seven Sisters Falls** - Spectacular seven-tiered waterfall
        - **Nohkalikai Falls** - Tallest plunge waterfall in India
        - **Dainthlen Falls** - Beautiful cascading falls
        - **Wah Kaba Falls** - Hidden gem waterfall
        
        **Other Attractions:**
        - **Mawsmai Caves** - Limestone cave system
        - **Living Root Bridges** - Natural bridges
        - **Bangladesh Plains View** - Breathtaking vistas
        
        **Best Time to Visit:** May to October (monsoon season)
        **Note:** Bring rain gear and waterproof bags!
        """
    
    elif "adventure" in input_lower or "trek" in input_lower:
        return """
        **Adventure Activities in Meghalaya** 🎒
        
        Meghalaya offers incredible adventure opportunities for thrill-seekers:
        
        **Trekking:**
        - **Living Root Bridge Trek** - 3-4 hours to Nongriat
        - **Shillong Peak Trek** - Easy to moderate
        - **Cherrapunji Trails** - Various difficulty levels
        
        **Caving:**
        - **Mawsmai Caves** - Easy limestone caves
        - **Krem Liat Prah** - Longest cave in India
        - **Siju Caves** - Stalactite formations
        
        **Water Sports:**
        - **River Rafting** - Thrilling rapids
        - **Swimming** - Natural pools and waterfalls
        - **Kayaking** - Scenic river routes
        
        **Other Activities:**
        - **Rock Climbing** - Limestone cliffs
        - **Camping** - Under the stars
        - **Photography** - Stunning landscapes
        
        **Safety:** Always go with experienced guides and proper equipment!
        """
    
    elif "food" in input_lower or "cuisine" in input_lower:
        return """
        **Meghalaya Cuisine** 🍽️
        
        Meghalaya offers unique and delicious local cuisine:
        
        **Must-Try Dishes:**
        - **Jadoh** - Traditional rice dish with meat
        - **Doh Khlieh** - Pork salad with onions
        - **Tungrymbai** - Fermented soybean curry
        - **Nakham Bitchi** - Dried fish curry
        - **Pumaloi** - Rice powder sweet
        
        **Local Specialties:**
        - **Smoked Pork** - Traditional preparation
        - **Bamboo Shoots** - Fresh and fermented
        - **Wild Mushrooms** - Forest varieties
        - **Local Rice** - Sticky and aromatic
        
        **Beverages:**
        - **Kyat** - Local rice beer
        - **Tea** - Grown in Meghalaya
        - **Fresh Juices** - Local fruits
        
        **Where to Eat:** Local markets, traditional restaurants, and homestays offer authentic experiences!
        """
    
    else:
        return f"""
        Thank you for your question: "{user_input}"
        
        I'm the Meghalaya Tourism Bot! 🏔️ I can help you with information about:
        
        **🏞️ Tourist Attractions**
        - Living Root Bridges
        - Cherrapunji waterfalls
        - Shillong city
        - Caves and natural wonders
        
        **🎭 Culture & Festivals**
        - Traditional festivals
        - Local customs
        - Tribal heritage
        - Cultural experiences
        
        **🎒 Adventure Activities**
        - Trekking trails
        - Caving expeditions
        - Water sports
        - Photography spots
        
        **🍽️ Food & Cuisine**
        - Local delicacies
        - Traditional dishes
        - Best restaurants
        - Food markets
        
        **🏨 Travel Tips**
        - Best times to visit
        - Accommodation options
        - Transportation
        - Weather information
        
        Please ask me about any specific aspect of Meghalaya tourism, and I'll provide detailed information!
        """

if __name__ == "__main__":
    main()
