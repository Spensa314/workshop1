# Notion Social Media Generator

Generate social media posts from your Notion company documents using OpenRouter's LLM API.

## Features

- 📚 Fetches company documents from Notion (branding, visual language, company details)
- 🤖 Generates social media posts using OpenRouter (supports multiple LLM models)
- 👀 Preview posts before posting
- 🐘 Mastodon integration (coming soon - will only post after approval)

## Setup

> 📖 **New to this?** Check out the detailed [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for step-by-step instructions on setting up Notion and OpenRouter, keeping your API keys secure, and understanding how the application works.

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Notion API integration token
- OpenRouter API key
- Notion database ID containing your company documents

### Installation

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create virtual environment and install dependencies**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. **Configure environment variables**:
   Copy the template and fill in your API keys:
   ```bash
   cp env.template .env
   ```

   Then edit `.env` with your actual API keys:
   ```env
   NOTION_API_KEY=your_notion_integration_token_here
   NOTION_DATABASE_ID=your_notion_database_id_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

   # Optional (for future Mastodon integration)
   MASTODON_INSTANCE_URL=https://your-instance.mastodon.social
   MASTODON_ACCESS_TOKEN=your_mastodon_access_token_here
   ```

### Getting API Keys

#### Notion API
1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the "Internal Integration Token"
4. Share your Notion database with the integration
5. Get your database ID from the database URL

#### OpenRouter API
1. Go to https://openrouter.ai/
2. Sign up and get your API key
3. Choose a model (default: `anthropic/claude-3.5-sonnet`)

## Usage

Activate the virtual environment (if not already activated):
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Run the application:
```bash
python src/main.py
```

The application will:
1. Fetch your company documents from Notion
2. Allow you to generate social media posts
3. Preview the generated posts
4. Ask for approval before posting (Mastodon integration coming soon)

## Project Structure

```
.
├── .env                 # Environment variables (not in git)
├── .gitignore
├── pyproject.toml       # Project dependencies
├── README.md
└── src/
    ├── __init__.py
    ├── main.py          # Main application
    ├── notion_client.py # Notion API integration
    ├── openrouter_client.py # OpenRouter LLM integration
    └── mastodon_client.py # Mastodon integration (future)
```

## Development

Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

## License

MIT
