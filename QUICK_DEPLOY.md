# 🚀 Quick Deploy Guide - Meghalaya Tourism Bot

## ⚡ Fastest Way to Deploy (5 minutes)

### Step 1: Push to GitHub
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Deploy Meghalaya Tourism Bot"

# Create GitHub repo and push
# Go to GitHub.com → Create new repository → Copy the commands below
git remote add origin https://github.com/YOUR_USERNAME/meghalaya-tourism-bot.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud
1. **Go to:** https://share.streamlit.io/
2. **Sign in** with GitHub
3. **Click:** "New app"
4. **Select:** Your repository `meghalaya-tourism-bot`
5. **Main file:** `app.py`
6. **App URL:** `meghalaya-tourism-bot` (or your choice)

### Step 3: Configure Secrets
In the "Secrets" section, paste this:

```toml
[mongodb]
uri = "mongodb+srv://mybtp:mybtp@node-api.cqbp1.mongodb.net/?retryWrites=true&w=majority&appName=Node-API"
database = "xlayer"
collection = "MeghalayaEmbeddings1"

[openai]
api_key = "your_openai_api_key_here"
model = "gpt-4"
embedding_model = "text-embedding-3-large"

[retrieval]
top_k_documents = 5
temperature = 0.7
max_tokens = 1000
```

### Step 4: Deploy!
- **Click:** "Deploy!"
- **Wait:** 2-3 minutes
- **Access:** Your app at `https://meghalaya-tourism-bot.streamlit.app/`

## ✅ That's it! Your bot is live!

### 🔧 Troubleshooting

**If deployment fails:**
1. Check the logs in Streamlit Cloud
2. Verify all secrets are correct
3. Ensure MongoDB allows connections from Streamlit Cloud IPs
4. Check OpenAI API key is valid

**If app doesn't load:**
1. Wait 2-3 minutes for full deployment
2. Refresh the page
3. Check the logs for errors

### 📱 Your App Features
- ✅ Chat with Meghalaya Tourism Bot
- ✅ Source attribution
- ✅ Session statistics
- ✅ Quick questions
- ✅ Mobile responsive

### 🎯 Test Your Deployed App
Try asking:
- "Tell me about living root bridges"
- "What festivals are in Meghalaya?"
- "Best places to visit in Shillong"

---

**Need help?** Check the full `DEPLOYMENT.md` guide for detailed instructions.
