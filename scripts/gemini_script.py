#!/usr/bin/env python3
"""
gemini_script.py — generates video script
Uses pre-written scripts for testing. Replace with API call when ready.
Output: ./temp/script.json
"""

import sys
import os
import json
import random

# ── Pre-written scripts (7 days worth) ───────────────────────────────────────

SCRIPTS = [
    {
        "script": "Did you know most people waste over 500 dollars a month without realizing it? Here are 3 simple ways to stop the bleeding. First, cancel subscriptions you forgot about. Check your bank statement right now — most people find at least 2 they don't use. Second, cook one extra meal at home per week. That alone saves 50 dollars a month. Third, use the 24-hour rule before any purchase over 30 dollars. Wait a day. You'll skip it half the time. Small changes, massive results. Follow for more money tips every day.",
        "title": "3 Ways to Stop Wasting Money Every Month",
        "description": "Most people waste hundreds of dollars every month without knowing it. In this video we reveal 3 simple habits that can save you over 500 dollars a month. Start with your subscriptions, cooking at home, and the 24-hour spending rule. These small changes add up fast. Subscribe for daily personal finance tips that actually work.",
        "hashtags": ["moneytips","savemoney","personalfinance","budgeting","financialtips","moneyhacks","savingsgoals","frugalliving","moneyadvice","wealthbuilding"],
        "tiktok_caption": "Stop wasting $500/month without knowing it 💸 3 simple fixes #moneytips #savemoney #personalfinance",
        "hook": "You're wasting $500 a month and don't even know it."
    },
    {
        "script": "The reason most people stay broke is not their income — it's their habits. Here's what rich people do differently. They pay themselves first. Before any bill, they move 10 percent of every paycheck into savings automatically. They track every dollar. Not to restrict themselves, but to stay aware. And they invest early, even small amounts. A hundred dollars a month invested at 20 years old becomes over 500,000 by retirement. The gap between rich and poor is habits, not luck. Start today.",
        "title": "Why Most People Stay Broke — And How to Fix It",
        "description": "The difference between wealthy and broke people isn't income — it's habits. Learn the 3 core money habits that separate the rich from everyone else. Pay yourself first, track your spending, and start investing early no matter how small. These habits compound over time and build real wealth. Subscribe for daily financial tips.",
        "hashtags": ["richhabits","personalfinance","moneymindset","investing","wealthbuilding","financialfreedom","moneyadvice","budgeting","savemoney","growyourwealth"],
        "tiktok_caption": "Rich people aren't lucky — they just do this differently 💰 #richhabits #personalfinance #moneymindset",
        "hook": "Rich people aren't lucky — they just have different habits."
    },
    {
        "script": "If you have no savings right now, here is your 30-day plan to change that. Week one: track every single expense. Just awareness. Week two: find one bill to cut — phone plan, streaming, insurance. Week three: sell something you own but don't use. Most people have 200 dollars sitting in their house. Week four: open a separate savings account and move whatever you saved into it. By day 30 you will have your first emergency fund started. Progress over perfection. Let's go.",
        "title": "30-Day Savings Plan for Beginners With Zero Savings",
        "description": "Starting from zero savings feels impossible but it's not. This 30-day plan breaks it into simple weekly steps anyone can follow. Track expenses, cut one bill, sell unused items, and open a dedicated savings account. By the end of the month you'll have momentum and real savings. Follow for more beginner-friendly money tips.",
        "hashtags": ["savingmoney","beginnerfinance","30daychallenge","personalfinance","emergencyfund","moneytips","budgeting","financialgoals","savingsplan","zerosavings"],
        "tiktok_caption": "Zero savings? Here's your 30-day fix 📅 #savingmoney #30daychallenge #personalfinance",
        "hook": "Zero savings? Here's your exact 30-day plan to change that."
    },
    {
        "script": "Inflation is silently stealing your money right now. Here's how to fight back. First, buy in bulk for items you use every week — rice, pasta, soap. You save 20 to 30 percent instantly. Second, switch to store brands. The product is often identical, made in the same factory. Third, time your purchases. Electronics drop 30 percent after new models launch. Clothes are cheapest end of season. Fighting inflation isn't about earning more — it's about spending smarter. Share this with someone who needs it.",
        "title": "How Inflation Is Stealing Your Money and How to Stop It",
        "description": "Inflation is reducing your purchasing power every single day. But there are smart strategies to fight back. Buying in bulk, switching to store brands, and timing your purchases strategically can save you hundreds every month. These aren't sacrifices — they're upgrades to how you shop. Subscribe for more money-saving strategies.",
        "hashtags": ["inflation","savemoney","smartshopping","personalfinance","moneyhacks","budgeting","costoflliving","financialtips","moneysaving","frugal"],
        "tiktok_caption": "Inflation is robbing you daily — here's how to fight back 💪 #inflation #savemoney #smartshopping",
        "hook": "Inflation is silently stealing your money right now."
    },
    {
        "script": "Most people think investing is only for rich people. It's not. Here's how to start with just 10 dollars. Open a free account on any major investing app. Buy one share of an index fund — it tracks the whole stock market so you're instantly diversified. Set up automatic investing of even 10 dollars a week. That's it. Over 10 years, that 10 dollars a week becomes over 7,000 dollars. Over 30 years, over 60,000 dollars. The best time to start was yesterday. The second best time is right now.",
        "title": "How to Start Investing With Just $10 — Beginner Guide",
        "description": "You don't need thousands of dollars to start investing. With just 10 dollars you can open an account, buy an index fund, and start building wealth today. Automatic weekly investing is the secret weapon of everyday millionaires. Learn how compound interest turns small amounts into life-changing money over time. Subscribe for more investing tips.",
        "hashtags": ["investing","beginnerinvesting","indexfunds","personalfinance","wealthbuilding","stockmarket","financialfreedom","moneytips","invest10dollars","compoundinterest"],
        "tiktok_caption": "Start investing with just $10 today 📈 No excuses! #investing #beginnerinvesting #personalfinance",
        "hook": "You can start investing today with just $10."
    },
    {
        "script": "Your credit score is costing you thousands of dollars. Here's how to fix it fast. Number one: pay every bill on time. Set up autopay for minimums so you never miss. Number two: keep your credit card balance below 30 percent of the limit. This alone can raise your score 50 points. Number three: don't close old cards even if you don't use them. Length of history matters. A good credit score means lower interest rates on everything — cars, homes, loans. That's worth tens of thousands over your lifetime.",
        "title": "Fix Your Credit Score Fast — 3 Steps That Actually Work",
        "description": "A bad credit score costs you thousands in higher interest rates on loans, cars, and mortgages. These 3 steps can significantly improve your credit score in 90 days or less. Pay on time, lower your utilization rate, and keep old accounts open. Your credit score is one of the most valuable financial tools you have. Subscribe for more credit and finance tips.",
        "hashtags": ["creditscore","fixcredit","personalfinance","creditrepair","moneytips","financialtips","creditbuilding","goodcredit","creditadvice","financialhealth"],
        "tiktok_caption": "Your credit score is costing you thousands 😤 Fix it with these 3 steps #creditscore #fixcredit #personalfinance",
        "hook": "Your credit score is costing you thousands of dollars."
    },
    {
        "script": "Side hustles are not just for extra cash — they can replace your income. Here are 3 that work in 2026. First, freelance writing. Companies pay 50 to 300 dollars per article. Start on Upwork or Fiverr with no experience needed. Second, reselling. Buy items on sale locally and sell online for profit. People make 2,000 dollars a month doing this part time. Third, digital products. Create one template, guide, or preset and sell it forever with no extra work. The best side hustle is the one you start today. Which one will you try?",
        "title": "3 Side Hustles That Can Replace Your Income in 2026",
        "description": "Side hustles have never been more accessible. Freelance writing, reselling, and digital products are three proven ways to earn extra income in 2026 with minimal startup costs. Many people turn these into full-time income streams. Start small, stay consistent, and scale what works. Subscribe for more side hustle and money-making strategies.",
        "hashtags": ["sidehustle","makemoneyonline","extraincome","personalfinance","freelancing","digitalproducts","reselling","incomeideas","workfromhome","financialfreedom"],
        "tiktok_caption": "3 side hustles that can replace your 9-5 in 2026 🔥 #sidehustle #makemoneyonline #extraincome",
        "hook": "These 3 side hustles can replace your full-time income."
    }
]

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Pick a random script each run
    script_data = random.choice(SCRIPTS)

    os.makedirs("./temp", exist_ok=True)
    with open("./temp/script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)

    print(f"Script saved to ./temp/script.json")
    print(f"Title: {script_data['title']}")
    print(f"Hook:  {script_data['hook']}")


if __name__ == "__main__":
    main()
