# AI Visionary - Zeus Agent

🚀 **Advanced AI Content Creation Platform**

AI Visionary is a comprehensive platform powered by the Zeus AI agent, offering automated content creation services across multiple formats and platforms.

## 🌟 Features

### Core Services
- **Social Content Generation** - Automated LinkedIn posts, Twitter threads
- **Video Creation** - Script generation, storyboarding, automated editing
- **Podcast Production** - Complete episode creation with AI voices
- **Smart Reports** - Data analysis and professional report generation
- **Weekly Content** - Automated content calendars and planning
- **Visual Identity** - AI portraits, logos, and brand elements

### Platform Integration
- **Fiverr** - Professional AI content services
- **Upwork** - Expert AI project consultation
- **Malt** - Freelance AI solutions
- **ComeUp** - Microservices for quick AI tasks
- **Gumroad** - Digital products and templates

## 🛠️ Technology Stack

- **Backend**: Python FastAPI
- **AI Integration**: OpenAI GPT-4, DALL-E 3
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Docker, Nginx
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/NeousAxis/ai-service-website.git
cd ai-service-website

# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r zeus_agent/requirements.txt

# Set up environment variables
cp zeus_agent/.env.example zeus_agent/.env
# Edit .env with your API keys

# Run the Zeus agent
cd zeus_agent
python main.py
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Website: http://localhost
# API: http://localhost/api
# Admin Dashboard: http://localhost/dashboard
```

## 📁 Project Structure