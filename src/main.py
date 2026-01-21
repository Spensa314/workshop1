# """Social Media Post Generator using Notion and OpenRouter"""

# import os
# import requests
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# # ===== NOTION CLIENT =====
# class NotionClient:
#     """Fetch documents from Notion database."""

#     def __init__(self):
#         self.api_key = os.getenv("NOTION_API_KEY")
#         self.database_id = os.getenv("NOTION_DATABASE_ID")

#         if not self.api_key:
#             raise ValueError("NOTION_API_KEY not found in .env")
#         if not self.database_id:
#             raise ValueError("NOTION_DATABASE_ID not found in .env")

#     def get_all_documents(self):
#         """Fetch all pages from the Notion database."""
#         db_id = self.database_id.replace("-", "")
#         formatted_id = f"{db_id[0:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:32]}"

#         url = f"https://api.notion.com/v1/databases/{formatted_id}/query"
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Notion-Version": "2022-06-28",
#             "Content-Type": "application/json"
#         }

#         all_pages = []
#         has_more = True
#         start_cursor = None

#         while has_more:
#             body = {}
#             if start_cursor:
#                 body["start_cursor"] = start_cursor

#             response = requests.post(url, headers=headers, json=body)
#             response.raise_for_status()
#             data = response.json()

#             all_pages.extend(data.get("results", []))
#             has_more = data.get("has_more", False)
#             start_cursor = data.get("next_cursor")

#         documents = []
#         for page in all_pages:
#             title = self._get_page_title(page)
#             content = self._get_page_content(page["id"])
#             documents.append(f"## {title}\n\n{content}")

#         return "\n\n---\n\n".join(documents)

#     def _get_page_title(self, page):
#         properties = page.get("properties", {})
#         for prop_value in properties.values():
#             if prop_value.get("type") == "title":
#                 title_array = prop_value.get("title", [])
#                 return "".join([t.get("plain_text", "") for t in title_array])
#         return "Untitled"

#     def _get_page_content(self, page_id):
#         url = f"https://api.notion.com/v1/blocks/{page_id}/children"
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Notion-Version": "2022-06-28"
#         }

#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         blocks = response.json().get("results", [])

#         text_parts = []
#         for block in blocks:
#             block_type = block.get("type")
#             if block_type in [
#                 "paragraph",
#                 "heading_1",
#                 "heading_2",
#                 "heading_3",
#                 "bulleted_list_item",
#                 "numbered_list_item",
#             ]:
#                 rich_text = block.get(block_type, {}).get("rich_text", [])
#                 text = "".join([t.get("plain_text", "") for t in rich_text])
#                 if text:
#                     text_parts.append(text)

#         return "\n".join(text_parts)


# # ===== OPENROUTER CLIENT =====
# class SocialMediaGenerator:
#     """Generate social media posts using OpenRouter."""

#     def __init__(self):
#         api_key = os.getenv("OPENROUTER_API_KEY")
#         if not api_key:
#             raise ValueError("OPENROUTER_API_KEY not found in .env")

#         self.client = OpenAI(
#             api_key=api_key,
#             base_url="https://openrouter.ai/api/v1"
#         )

#         self.model = os.getenv(
#             "OPENROUTER_MODEL",
#             "anthropic/claude-3.5-sonnet"
#         )

#     def generate_post(self, company_context, topic=None, post_type=None):
#         system_prompt = f"""
# You are a social media content creator.

# Use the following company information to create a single Mastodon-ready post:

# {company_context}

# Rules:
# - Match the company's brand voice and values
# - Be concise and engaging
# - Stay under 480 characters
# - Avoid emoji spam
# - Include 1–3 relevant hashtags
# - No preamble, no explanation, no quotes
# - Output ONLY the final post text
# """.strip()

#         user_message = "Create a social media post"
#         if topic:
#             user_message += f" about: {topic}"
#         if post_type:
#             user_message += f" (type: {post_type})"
#         user_message += "."

#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_message},
#             ],
#         )

#         return response.choices[0].message.content.strip()


# # ===== MASTODON CLIENT =====
# class MastodonClient:
#     """Post approved content to Mastodon."""

#     def __init__(self):
#         self.instance_url = os.getenv("MASTODON_INSTANCE_URL")
#         self.access_token = os.getenv("MASTODON_ACCESS_TOKEN")

#         if not self.instance_url:
#             raise ValueError("MASTODON_INSTANCE_URL not found in .env")
#         if not self.access_token:
#             raise ValueError("MASTODON_ACCESS_TOKEN not found in .env")

#         self.headers = {
#             "Authorization": f"Bearer {self.access_token}",
#             "Content-Type": "application/json",
#         }

#     def post_status(self, text, visibility="public"):
#         url = f"{self.instance_url}/api/v1/statuses"
#         payload = {
#             "status": text,
#             "visibility": visibility,
#         }

#         response = requests.post(url, headers=self.headers, json=payload)
#         response.raise_for_status()
#         return response.json()


# # ===== MAIN APPLICATION =====
# def main():
#     print("🚀 Social Media Post Generator\n")
#     print("=" * 60)

#     print("\n📚 Fetching company documents from Notion...")
#     try:
#         notion = NotionClient()
#         company_docs = notion.get_all_documents()

#         if not company_docs.strip():
#             print("❌ No content found in Notion database")
#             return

#         print("✓ Company documents loaded\n")
#     except Exception as e:
#         print(f"❌ Error loading Notion documents: {e}")
#         return

#     try:
#         generator = SocialMediaGenerator()
#     except Exception as e:
#         print(f"❌ Error initializing OpenRouter: {e}")
#         return

#     while True:
#         print("\n" + "=" * 60)
#         print("Options:")
#         print("1. Generate a new post")
#         print("2. Generate a post with specific topic")
#         print("3. Exit")
#         print("=" * 60)

#         choice = input("\nSelect option (1-3): ").strip()

#         if choice == "3":
#             print("\n👋 Goodbye!")
#             break

#         if choice not in ["1", "2"]:
#             print("Invalid choice.")
#             continue

#         topic = None
#         post_type = None

#         if choice == "2":
#             topic = input("Enter topic (press Enter to skip): ").strip() or None

#         post_type_input = input(
#             "Post type (announcement/tip/question/story, press Enter to skip): "
#         ).strip()
#         if post_type_input:
#             post_type = post_type_input

#         print("\n🤖 Generating post with AI...")
#         try:
#             post = generator.generate_post(
#                 company_context=company_docs,
#                 topic=topic,
#                 post_type=post_type,
#             )

#             print("\n" + "=" * 60)
#             print("GENERATED POST PREVIEW")
#             print("=" * 60)
#             print(post)
#             print("=" * 60)

#             approve = input("\nApprove this post? (y/n): ").strip().lower()

#             if approve == "y":
#                 print("✓ Post approved!")

#                 try:
#                     mastodon = MastodonClient()
#                     result = mastodon.post_status(post)

#                     print("🚀 Posted to Mastodon successfully!")
#                     if result.get("url"):
#                         print(f"🔗 {result['url']}")

#                 except Exception as e:
#                     print(f"❌ Failed to post to Mastodon: {e}")
#             else:
#                 print("Post not approved. Generate another one!")

#         except Exception as e:
#             print(f"❌ Error generating post: {e}")


# if __name__ == "__main__":
#     main()

"""
AI Social Media Agent
- Notion-powered brand context
- OpenRouter LLM generation
- Mastodon posting + replies
- AI disclosure compliant
- Only generates replies for allowed instances
"""

import os
import random
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# NOTION CLIENT
# ============================================================

class NotionClient:
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        if not self.api_key or not self.database_id:
            raise ValueError("Missing Notion credentials")

    def get_all_documents(self):
        db_id = self.database_id.replace("-", "")
        formatted_id = f"{db_id[0:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:32]}"
        url = f"https://api.notion.com/v1/databases/{formatted_id}/query"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
        pages = []
        cursor = None
        has_more = True
        while has_more:
            body = {"start_cursor": cursor} if cursor else {}
            r = requests.post(url, headers=headers, json=body)
            r.raise_for_status()
            data = r.json()
            pages.extend(data["results"])
            has_more = data["has_more"]
            cursor = data["next_cursor"]

        documents = []
        for page in pages:
            title = self._get_title(page)
            content = self._get_content(page["id"])
            documents.append(f"## {title}\n{content}")
        return documents

    def _get_title(self, page):
        for prop in page["properties"].values():
            if prop["type"] == "title":
                return "".join(t["plain_text"] for t in prop["title"])
        return "Untitled"

    def _get_content(self, page_id):
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        headers = {"Authorization": f"Bearer {self.api_key}", "Notion-Version": "2022-06-28"}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        text = []
        for block in r.json()["results"]:
            btype = block["type"]
            if "rich_text" in block.get(btype, {}):
                t = "".join(rt["plain_text"] for rt in block[btype]["rich_text"])
                if t:
                    text.append(t)
        return "\n".join(text)


# ============================================================
# OPENROUTER / LLM CLIENT
# ============================================================

REPLY_SCHEMA = {
    "type": "object",
    "properties": {
        "replies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"status_id": {"type": "string"}, "reply_text": {"type": "string"}},
                "required": ["status_id", "reply_text"],
            },
        }
    },
    "required": ["replies"],
}

class SocialMediaGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
        self.model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")

    def generate_post(self, context, topic=None, post_type=None):
        system = f"""
You are a social media content creator.

Context:
{context}

Rules:
- Match brand voice and values
- Stay under 480 characters
- 1–3 relevant hashtags
- ALWAYS end with #AIGenerated
- Vary focus each time
- No preamble, no quotes
- Output ONLY the post text
"""
        user = "Create a Mastodon post"
        if topic:
            user += f" about {topic}"
        if post_type:
            user += f" ({post_type})"

        r = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "system", "content": system}, {"role": "user", "content": user}]
        )
        return r.choices[0].message.content.strip()

    def generate_replies(self, context, statuses):
        posts = "\n\n".join(f"ID: {s['id']}\nPost: {s['content']}" for s in statuses)
        system = f"""
You are a respectful brand-safe assistant.

Context:
{context}

Rules:
- Reply only if relevant
- Helpful, non-promotional
- Under 300 characters
- End with #AIGenerated
- No repetition of original content
"""
        user = f"Write a reply to EACH post below. Return JSON using the provided schema.\n\nPosts:\n{posts}"
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            response_format={"type": "json_schema", "json_schema": REPLY_SCHEMA},
        )
        return r.choices[0].message.parsed


# ============================================================
# MASTODON CLIENT
# ============================================================

class MastodonClient:
    def __init__(self):
        self.base = os.getenv("MASTODON_INSTANCE_URL")
        self.token = os.getenv("MASTODON_ACCESS_TOKEN")
        if not self.base or not self.token:
            raise ValueError("Missing Mastodon credentials")
        self.headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def post_status(self, text):
        r = requests.post(f"{self.base}/api/v1/statuses", headers=self.headers, json={"status": text})
        r.raise_for_status()
        return r.json()

    def can_access_hashtag(self, keyword):
        """Return True if hashtag timeline is allowed, False otherwise."""
        try:
            url = f"{self.base}/api/v1/timelines/tag/{keyword}"
            r = requests.get(url, headers=self.headers, params={"limit": 1})
            r.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            if r.status_code == 403:
                return False
            raise

    def search_statuses(self, keyword, limit=5):
        url = f"{self.base}/api/v1/timelines/tag/{keyword}"
        r = requests.get(url, headers=self.headers, params={"limit": limit})
        r.raise_for_status()
        return r.json()[:limit]

    def reply(self, status_id, text):
        r = requests.post(
            f"{self.base}/api/v1/statuses", headers=self.headers, json={"status": text, "in_reply_to_id": status_id}
        )
        r.raise_for_status()
        return r.json()


# ============================================================
# MAIN APP
# ============================================================

def main():
    notion = NotionClient()
    docs = notion.get_all_documents()
    generator = SocialMediaGenerator()
    mastodon = MastodonClient()

    while True:
        print("\n1. New post\n2. New post (topic)\n3. Reply to posts\n4. Exit")
        choice = input("> ").strip()
        if choice == "4":
            break

        context = "\n\n".join(random.sample(docs, k=min(2, len(docs))))

        if choice in {"1", "2"}:
            topic = input("Topic: ").strip() if choice == "2" else None
            post = generator.generate_post(context, topic)
            print("\nPREVIEW:\n", post)
            if input("\nPost? (y/n): ").lower() == "y":
                mastodon.post_status(post)
                print("✓ Posted")

        elif choice == "3":
            keyword = input("Keyword (without #): ").strip()
            if mastodon.can_access_hashtag(keyword):
                statuses = mastodon.search_statuses(keyword)
                if not statuses:
                    print(f"⚠️ No posts found for #{keyword}.")
                    continue

                replies = generator.generate_replies(context, statuses)["replies"]
                for r in replies:
                    print("\nREPLY PREVIEW:\n", r["reply_text"])
                    if input("Post reply? (y/n): ").lower() == "y":
                        mastodon.reply(r["status_id"], r["reply_text"])
                        print("✓ Reply posted")
            else:
                print(f"⚠️ This Mastodon instance does not allow hashtag timelines. Replies skipped.")


if __name__ == "__main__":
    main()
