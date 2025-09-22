# 🚀 Meghalaya Tourism Bot - Deployment Guide

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free)
- MongoDB Atlas account
- OpenAI API account

### Step 1: Prepare Your Repository

1. **Initialize Git Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Meghalaya Tourism Bot"
   ```

2. **Create GitHub Repository:**
   - Go to GitHub.com
   - Create a new repository named `meghalaya-tourism-bot`
   - Don't initialize with README (we already have files)

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/yourusername/meghalaya-tourism-bot.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create New App:**
   - Click "New app"
   - Select your repository: `yourusername/meghalaya-tourism-bot`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: `meghalaya-tourism-bot` (or your preferred name)

3. **Configure Secrets:**
   In the "Secrets" section, add:
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

4. **Deploy:**
   - Click "Deploy!"
   - Wait for deployment to complete (2-3 minutes)

### Step 3: Access Your Deployed App

Your app will be available at:
`https://meghalaya-tourism-bot.streamlit.app/`

## Alternative Deployment Options

### Heroku Deployment

1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App:**
   ```bash
   heroku create meghalaya-tourism-bot
   ```

3. **Set Environment Variables:**
   ```bash
   heroku config:set MONGODB_URI="your_mongodb_uri"
   heroku config:set OPENAI_API_KEY="your_openai_key"
   # ... other variables
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

### Docker Deployment

1. **Build Docker Image:**
   ```bash
   docker build -t meghalaya-tourism-bot .
   ```

2. **Run Container:**
   ```bash
   docker run -p 8501:8501 \
     -e MONGODB_URI="your_mongodb_uri" \
     -e OPENAI_API_KEY="your_openai_key" \
     meghalaya-tourism-bot
   ```

3. **Deploy to Cloud:**
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances
   - DigitalOcean App Platform

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `MONGODB_URI` | MongoDB connection string | Yes |
| `MONGODB_DATABASE` | Database name | No (default: meghalaya_tourism) |
| `MONGODB_COLLECTION` | Collection name | No (default: tourism_documents) |
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `OPENAI_MODEL` | GPT model to use | No (default: gpt-4) |
| `OPENAI_EMBEDDING_MODEL` | Embedding model | No (default: text-embedding-3-large) |
| `TOP_K_DOCUMENTS` | Number of documents to retrieve | No (default: 5) |
| `TEMPERATURE` | Response creativity (0-2) | No (default: 0.7) |
| `MAX_TOKENS` | Maximum response length | No (default: 1000) |

## Troubleshooting

### Common Issues:

1. **Import Errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **MongoDB Connection Issues:**
   - Verify MongoDB URI is correct
   - Check network access in MongoDB Atlas
   - Ensure IP whitelist includes Streamlit Cloud IPs

3. **OpenAI API Issues:**
   - Verify API key is valid
   - Check API usage limits
   - Ensure sufficient credits

4. **Memory Issues:**
   - Streamlit Cloud has memory limits
   - Optimize vector search queries
   - Consider reducing `TOP_K_DOCUMENTS`

### Performance Optimization:

1. **Reduce Response Time:**
   - Lower `TOP_K_DOCUMENTS` value
   - Use faster embedding models
   - Implement response caching

2. **Reduce Memory Usage:**
   - Optimize document retrieval
   - Use smaller models if possible
   - Implement connection pooling

## Monitoring and Maintenance

1. **Check Logs:**
   - Streamlit Cloud provides built-in logs
   - Monitor for errors and performance issues

2. **Update Dependencies:**
   - Regularly update `requirements.txt`
   - Test updates in development first

3. **Monitor Usage:**
   - Track API usage and costs
   - Monitor MongoDB usage
   - Set up alerts for high usage

## Security Best Practices

1. **Never commit secrets:**
   - Use `.gitignore` to exclude sensitive files
   - Use environment variables or secrets management

2. **API Key Security:**
   - Rotate API keys regularly
   - Use least-privilege access
   - Monitor API usage

3. **Database Security:**
   - Use strong passwords
   - Enable IP whitelisting
   - Use SSL connections

## Support

For deployment issues:
1. Check Streamlit Cloud documentation
2. Review application logs
3. Test locally first
4. Check GitHub issues for similar problems

---

**Happy Deploying! 🚀**
