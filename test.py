import requests
from openai import OpenAI
import os
from dotenv import load_dotenv
# Load env variables
load_dotenv()
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME =os.getenv("CHANNEL_USERNAME")  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(OPENAI_API_KEY)

Base_URL = "https://openrouter.ai/api/v1"
client = OpenAI(
  base_url= Base_URL,
  api_key = OPENAI_API_KEY
) 
def generate_post():
    prompt = """ তুমি একজন motivational content creator। তুমি “Hey You” নামের ফেসবুক পেজের জন্য শর্ট, স্টাইলিশ, বাংলা motivational quote লিখবে। প্রতিটি কোটস ১–৩ লাইন হবে, সহজ, সরল এবং সহজেই relatable।

থিম হতে পারে: life lesson, self-improvement, positive thinking, perseverance, success, mindset ইত্যাদি।

প্রতিটি কোটসে ২–৪টি ইমোজি ব্যবহার করতে হবে।

প্রতিবার শুধু একটি নতুন কোটস দেবে।

কোটসটি পড়ার পর মানুষ যেন প্রেরণা বা positive energy অনুভব করে।

কোটস যেন লাইক বা শেয়ার করার মতো catchy এবং স্টাইলিশ হয়।

শেষে ৩–৫টি ভাইরাল হ্যাশট্যাগ দাও, যেখানে অবশ্যই #hyeyou থাকবে।

❌ শর্ত: আগের দেওয়া কোটসের সাথে কোনোভাবেই মিল থাকবে না (শব্দ, ইমোজি, স্টাইল সব আলাদা হতে হবে)।


⚠️ Only return the post content."""
    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "sajim.com", 
        "X-Title": "Sajim",
    },
    extra_body={},
    model="deepseek/deepseek-chat-v3.1:free",
    messages=[
        {
        "role": "user",
        "content": prompt
        }
    ]
    )
    message = completion.choices[0].message.content
    return message

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    payload = {"message": message, "access_token": FB_ACCESS_TOKEN}
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        print("🚀 Generating new SQA post...")
        message = generate_post()
        print("✅ Post generated successfully!")
        result = post_to_facebook(message)
        print(f"✅ Post published! Post ID: {result.get('id')}")

    except Exception as e:
        print(f"❌ Error: {e}")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_USERNAME,
            "text": message
        }
        response = requests.post(url, data=payload)
