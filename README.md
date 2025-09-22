# 🏔️ Meghalaya Tourism Bot

A production-ready Streamlit chatbot application that provides comprehensive tourism information about Meghalaya, India. The bot uses Retrieval-Augmented Generation (RAG) with MongoDB vector search and OpenAI GPT-4 to deliver accurate, contextual responses about Meghalaya's attractions, culture, festivals, and travel resources.

## ✨ Features

- **🤖 Intelligent Chat Interface**: Powered by OpenAI GPT-4 with context-aware responses
- **🔍 Vector Search**: MongoDB Atlas Vector Search for relevant document retrieval
- **📚 Source Attribution**: Shows sources and relevance scores for transparency
- **🎨 Responsive UI**: Modern, mobile-friendly Streamlit interface
- **🐳 Docker Ready**: Production-ready containerization
- **⚙️ Configurable**: Environment-based configuration management
- **🛡️ Error Handling**: Graceful error handling with user feedback
- **📊 Analytics**: Session statistics and response metadata

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   RAG Pipeline   │    │  MongoDB Vector │
│                 │◄──►│                  │◄──►│     Store       │
│  - Chat Interface│    │  - Document      │    │                 │
│  - Source Display│    │    Retrieval    │    │  - Tourism Docs │
│  - Error Handling│    │  - Response      │    │  - Vector Index │
└─────────────────┘    │    Generation    │    └─────────────────┘
                       └──────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │                 │
                       │  - GPT-4 Model  │
                       │  - Embeddings   │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- MongoDB Atlas account with vector search enabled
- OpenAI API key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd meghalaya-tourism-bot
```

### 2. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your configuration:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=meghalaya_tourism
MONGODB_COLLECTION=tourism_documents

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

# Retrieval Parameters
TOP_K_DOCUMENTS=5
TEMPERATURE=0.7
MAX_TOKENS=1000

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### 3. Build and Run with Docker

```bash
# Build the Docker image
docker build -t meghalaya-chatbot .

# Run the container
docker run -p 8501:8501 --env-file .env meghalaya-chatbot
```

### 4. Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t meghalaya-chatbot .
```

### Run Container

```bash
# Using environment file
docker run -p 8501:8501 --env-file .env meghalaya-chatbot

# Using environment variables directly
docker run -p 8501:8501 \
  -e MONGODB_URI="your_mongodb_uri" \
  -e OPENAI_API_KEY="your_openai_key" \
  -e MONGODB_DATABASE="meghalaya_tourism" \
  meghalaya-chatbot
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  meghalaya-bot:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with Docker Compose:

```bash
docker-compose up -d
```

## 📊 MongoDB Setup

### 1. Create Vector Search Index

In MongoDB Atlas, create a vector search index on your collection:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    }
  ]
}
```

### 2. Document Schema

Your tourism documents should follow this schema:

```json
{
  "_id": "ObjectId",
  "page_content": "Document content text...",
  "metadata": {
    "title": "Document title",
    "source": "Source URL or file",
    "type": "attraction|festival|culture|travel_tip",
    "location": "Specific location in Meghalaya",
    "tags": ["tag1", "tag2", "tag3"]
  },
  "embedding": [0.1, 0.2, ...] // Vector embedding
}
```

## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | Required |
| `MONGODB_DATABASE` | Database name | `meghalaya_tourism` |
| `MONGODB_COLLECTION` | Collection name | `tourism_documents` |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | GPT model to use | `gpt-4` |
| `OPENAI_EMBEDDING_MODEL` | Embedding model | `text-embedding-3-large` |
| `TOP_K_DOCUMENTS` | Number of documents to retrieve | `5` |
| `TEMPERATURE` | Response creativity (0-2) | `0.7` |
| `MAX_TOKENS` | Maximum response length | `1000` |

## 🛠️ Development

### Local Development Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Locally**:
   ```bash
   streamlit run app.py
   ```

3. **Environment Variables**:
   Set up your `.env` file as described above.

### Project Structure

```
meghalaya-tourism-bot/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration management
├── vector_store.py       # MongoDB vector store operations
├── rag_pipeline.py       # RAG pipeline implementation
├── ui_components.py      # Streamlit UI components
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── env.example          # Environment variables template
└── README.md            # This file
```

## 🧪 Testing

### Health Check

The application includes a health check endpoint:
```
GET http://localhost:8501/_stcore/health
```

### Manual Testing

1. Start the application
2. Ask questions about Meghalaya tourism
3. Verify source attribution is displayed
4. Check error handling with invalid queries

## 📈 Monitoring and Logging

The application includes comprehensive logging:

- **Application logs**: Component initialization and errors
- **Query logs**: User queries and processing times
- **Performance metrics**: Response generation times
- **Error tracking**: Detailed error information

## 🔒 Security Considerations

- **Environment Variables**: Sensitive data stored in environment variables
- **Non-root User**: Docker container runs as non-root user
- **Input Validation**: User input is validated and sanitized
- **Error Handling**: Sensitive information is not exposed in error messages

## 🚀 Production Deployment

### Cloud Deployment

The application is ready for deployment on:

- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **Kubernetes clusters**
- **Any Docker-compatible platform**

### Scaling Considerations

- **Horizontal Scaling**: Run multiple container instances
- **Load Balancing**: Use a load balancer for multiple instances
- **Database**: Ensure MongoDB Atlas can handle concurrent connections
- **Caching**: Consider Redis for response caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the documentation
2. Review the logs for error messages
3. Verify your configuration
4. Open an issue on GitHub

## 🙏 Acknowledgments

- **LangChain** for RAG pipeline framework
- **MongoDB Atlas** for vector search capabilities
- **OpenAI** for language models and embeddings
- **Streamlit** for the web interface
- **Meghalaya Tourism** for the inspiration

---

**Built with ❤️ for travelers exploring the beautiful state of Meghalaya**
