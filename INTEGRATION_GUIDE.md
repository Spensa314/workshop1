# Step-by-Step Integration Guide

This guide will walk you through setting up Notion and OpenRouter integrations, keeping your API keys secure, and using the application to generate social media posts.

## Part 1: Understanding API Key Security

### How `.gitignore` Protects Your Secrets

Your project already has a `.gitignore` file that includes `.env` on line 30. This means:

1. **Git will never track your `.env` file** - When you commit code, Git will ignore the `.env` file completely
2. **Your secrets stay local** - The `.env` file only exists on your computer
3. **The template is safe to commit** - `env.template` doesn't contain real keys, so it's safe to share

**Important**: Never commit your actual `.env` file with real API keys. Always use the template file for reference.

---

## Part 2: Setting Up Notion Integration

### Step 1: Create a Notion Integration

1. **Go to Notion Integrations**
   - Visit: https://www.notion.so/my-integrations
   - You'll need to be logged into your Notion account

2. **Create a New Integration**
   - Click the "+ New integration" button
   - Give it a name (e.g., "Social Media Generator")
   - Select your workspace
   - Choose "Internal" integration type
   - Click "Submit"

3. **Copy Your Integration Token**
   - After creating the integration, you'll see a page with details
   - Find the "Internal Integration Token" section
   - Click "Show" and copy the token (it starts with `secret_`)
   - **Save this somewhere safe** - you'll need it in a moment

4. **Note the Integration Capabilities**
   - Make sure "Read content" is enabled (it should be by default)
   - You can leave other permissions as default for now

### Step 2: Prepare Your Notion Database

Your application needs a Notion database that contains your company information. Here's how to set it up:

1. **Create or Use an Existing Database**
   - You can use any Notion database (table, board, list, etc.)
   - Each page in the database will be treated as a company document
   - The application will combine all pages into one context for the AI

2. **Add Your Company Information**
   - Create pages in your database with:
     - Company description
     - Branding guidelines
     - Visual language/style guide
     - Company values
     - Any other relevant information
   - You can organize this however you like - the app will read all pages

3. **Share the Database with Your Integration**
   - Open your Notion database
   - Click the "..." menu (three dots) in the top right
   - Select "Connections" or "Add connections"
   - Find and select your integration (the one you just created)
   - Click "Confirm"

### Step 3: Get Your Database ID

The application needs to know which database to read from. Here's how to find the database ID:

1. **Open Your Database in Notion**
   - Go to the database you want to use
   - Make sure it's shared with your integration (from Step 2)

2. **Extract the Database ID from the URL**
   - Look at your browser's address bar
   - The URL will look something like:
     ```
     https://www.notion.so/workspace/32-char-hex-string?v=...
     ```
   - The database ID is the 32-character hexadecimal string (with dashes)
   - It looks like: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

3. **Alternative Method: Using the Notion API**
   - If you have trouble finding it, you can also query your integrations to see accessible databases
   - The ID is always 32 characters, separated by dashes in the format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**Example**: If your URL is:
```
https://www.notion.so/myworkspace/12345678-1234-1234-1234-123456789abc?v=...
```

Then your database ID is: `12345678-1234-1234-1234-123456789abc`

---

## Part 3: Setting Up OpenRouter

### Step 1: Create an OpenRouter Account

1. **Sign Up for OpenRouter**
   - Visit: https://openrouter.ai/
   - Click "Sign Up" or "Get Started"
   - Create an account (you can use Google/GitHub login)

2. **Add Credits**
   - OpenRouter uses a credit-based system
   - Go to your dashboard and add credits (they have a free tier to start)
   - You'll need credits to make API calls

### Step 2: Get Your API Key

1. **Navigate to API Keys**
   - Once logged in, go to: https://openrouter.ai/keys
   - Or find "API Keys" in your account menu

2. **Create a New Key**
   - Click "Create Key" or "New Key"
   - Give it a name (e.g., "Social Media Generator")
   - Copy the API key immediately (it starts with `sk-or-` or similar)
   - **Save this somewhere safe** - you won't be able to see it again

3. **Choose Your Model** (Optional)
   - The default is `anthropic/claude-3.5-sonnet` which is excellent
   - You can change this in your `.env` file later
   - Other good options:
     - `anthropic/claude-3-opus` (more powerful, more expensive)
     - `openai/gpt-4` (alternative)
     - `google/gemini-pro` (cost-effective)

---

## Part 4: Creating Your `.env` File

Now that you have both API keys, let's set up your environment file:

### Step 1: Create the `.env` File

1. **Copy the Template**
   - In your project folder, you have an `env.template` file
   - Copy it to create your actual `.env` file
   - You can do this in your file explorer or terminal

2. **Open the `.env` File**
   - Use any text editor (VS Code, TextEdit, etc.)
   - Make sure you're editing `.env`, not `env.template`

### Step 2: Fill in Your API Keys

Replace the placeholder values with your actual keys:

```env
# Notion API Configuration
NOTION_API_KEY=secret_your_actual_notion_token_here
NOTION_DATABASE_ID=your-actual-database-id-here

# OpenRouter API Configuration
OPENROUTER_API_KEY=sk-or-your-actual-openrouter-key-here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Mastodon Configuration (for future use - leave as is for now)
MASTODON_INSTANCE_URL=https://your-instance.mastodon.social
MASTODON_ACCESS_TOKEN=your_mastodon_access_token_here
```

**Important Notes:**
- Don't use quotes around the values (just the text after the `=`)
- Don't leave spaces around the `=` sign
- Make sure there are no extra spaces at the end of lines
- The Mastodon fields can stay as placeholders for now

### Step 3: Verify Your `.env` File is Ignored

1. **Check Git Status** (optional but recommended)
   - Open a terminal in your project folder
   - Run: `git status`
   - You should NOT see `.env` in the list of files
   - If you do see it, that means `.gitignore` isn't working (check the file)

2. **Double-Check `.gitignore`**
   - Open `.gitignore` in your editor
   - Make sure line 30 says `.env` (it should already be there)

---

## Part 5: Understanding How the Application Works

### The Workflow: From Notion to Social Media Post

Here's what happens when you run the application:

1. **Fetching Notion Documents**
   - The app connects to Notion using your API key
   - It queries your database using the database ID
   - It retrieves all pages from that database
   - For each page, it extracts the text content (headings, paragraphs, lists, etc.)
   - It combines all pages into one comprehensive document

2. **Building the Context**
   - All your company information is combined into a single text document
   - This includes: company description, branding, visual language, values, etc.
   - This becomes the "context" that the AI will use

3. **Generating the Post**
   - The app sends a request to OpenRouter with:
     - Your company context (from Notion)
     - Instructions to create a social media post
     - Any specific topic or post type you requested
   - OpenRouter uses the LLM (Claude, GPT-4, etc.) to generate a post
   - The post is designed to match your brand and tone

4. **Preview and Approval**
   - The generated post is displayed in a nice preview format
   - You can review it and decide if you like it
   - If approved, it's ready for posting (Mastodon integration coming later)
   - If not, you can generate another one

### What Information Should Be in Your Notion Database?

For best results, include pages with:

- **Company Overview**: What your company does, mission, vision
- **Brand Voice**: Tone of voice (professional, casual, friendly, etc.)
- **Visual Language**: Color schemes, design style, aesthetic
- **Target Audience**: Who you're speaking to
- **Content Themes**: Topics you typically post about
- **Examples**: Sample posts or content that represents your brand

The more context you provide, the better the AI can match your brand!

---

## Part 6: Running the Application

### Step 1: Activate Your Virtual Environment

The virtual environment (`.venv`) contains all the Python packages you need. You need to activate it:

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

You'll know it's activated when you see `(.venv)` at the start of your terminal prompt.

### Step 2: Run the Application

```bash
python src/main.py
```

### Step 3: Using the Application

1. **First Run**
   - The app will connect to Notion and fetch your documents
   - You'll see a message like "📚 Fetching company documents from Notion..."
   - If successful, you'll see "✓ Company documents loaded"

2. **Generate a Post**
   - Choose option 1 or 2 from the menu
   - Option 1: Generate a general post
   - Option 2: Generate a post with a specific topic
   - You can optionally specify a post type (announcement, tip, question, etc.)

3. **Review the Preview**
   - The generated post will be displayed in a formatted preview
   - Read it carefully to see if it matches your brand

4. **Approve or Regenerate**
   - If you like it, approve it
   - If not, you can generate another one
   - The app will keep running so you can generate multiple posts

---

## Troubleshooting

### "NOTION_API_KEY not found in environment variables"
- Make sure your `.env` file exists in the project root
- Check that the variable name is exactly `NOTION_API_KEY` (case-sensitive)
- Verify there are no spaces around the `=` sign
- Make sure you're running the app from the project directory

### "NOTION_DATABASE_ID not found"
- Same checks as above, but for `NOTION_DATABASE_ID`
- Verify you copied the full database ID (32 characters with dashes)

### "Unable to access database"
- Make sure you shared the database with your integration in Notion
- Go back to Notion, open the database, and check "Connections"
- Your integration should be listed there

### "OpenRouter API error"
- Check that your API key is correct
- Verify you have credits in your OpenRouter account
- Make sure the model name is correct (check OpenRouter's available models)

### "No content found in Notion database"
- Make sure your database has at least one page
- Verify the pages have content (not just empty pages)
- Check that the database is shared with your integration

---

## Next Steps

Once you have everything working:

1. **Refine Your Notion Content**: Add more detailed information about your brand
2. **Experiment with Post Types**: Try different topics and post types
3. **Adjust the Model**: Try different LLM models in OpenRouter
4. **Prepare for Mastodon**: When ready, we'll add the Mastodon posting functionality

Happy posting! 🚀
