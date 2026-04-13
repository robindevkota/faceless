#!/usr/bin/env python3
"""
gemini_script.py — generates video script
Uses pre-written scripts (30 days worth). Replace with API call when ready.
Output: ./temp/script.json
"""

import os
import json
import random

# ── 30 Pre-written scripts ────────────────────────────────────────────────────

SCRIPTS = [
    {
        "script": "Did you know most people waste over 500 dollars a month without realizing it? Here are 3 simple ways to stop the bleeding. First, cancel subscriptions you forgot about. Check your bank statement right now — most people find at least 2 they don't use. Second, cook one extra meal at home per week. That alone saves 50 dollars a month. Third, use the 24-hour rule before any purchase over 30 dollars. Wait a day. You'll skip it half the time. Small changes, massive results. Follow for more money tips every day.",
        "title": "3 Ways to Stop Wasting Money Every Month",
        "description": "Most people waste hundreds of dollars every month without knowing it. In this video we reveal 3 simple habits that can save you over 500 dollars a month. Start with your subscriptions, cooking at home, and the 24-hour spending rule. These small changes add up fast. Subscribe for daily personal finance tips.",
        "hashtags": ["moneytips","savemoney","personalfinance","budgeting","financialtips","moneyhacks","savingsgoals","frugalliving","moneyadvice","wealthbuilding"],
        "tiktok_caption": "Stop wasting $500/month without knowing it 💸 3 simple fixes #moneytips #savemoney #personalfinance",
        "hook": "You're wasting $500 a month and don't even know it."
    },
    {
        "script": "The reason most people stay broke is not their income — it's their habits. Here's what rich people do differently. They pay themselves first. Before any bill, they move 10 percent of every paycheck into savings automatically. They track every dollar. Not to restrict themselves, but to stay aware. And they invest early, even small amounts. A hundred dollars a month invested at 20 years old becomes over 500,000 by retirement. The gap between rich and poor is habits, not luck. Start today.",
        "title": "Why Most People Stay Broke — And How to Fix It",
        "description": "The difference between wealthy and broke people isn't income — it's habits. Learn the 3 core money habits that separate the rich from everyone else. Pay yourself first, track your spending, and start investing early. These habits compound over time and build real wealth. Subscribe for daily financial tips.",
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
        "description": "Inflation is reducing your purchasing power every single day. But there are smart strategies to fight back. Buying in bulk, switching to store brands, and timing your purchases strategically can save you hundreds every month. Subscribe for more money-saving strategies.",
        "hashtags": ["inflation","savemoney","smartshopping","personalfinance","moneyhacks","budgeting","costofliving","financialtips","moneysaving","frugal"],
        "tiktok_caption": "Inflation is robbing you daily — here's how to fight back 💪 #inflation #savemoney #smartshopping",
        "hook": "Inflation is silently stealing your money right now."
    },
    {
        "script": "Most people think investing is only for rich people. It's not. Here's how to start with just 10 dollars. Open a free account on any major investing app. Buy one share of an index fund — it tracks the whole stock market so you're instantly diversified. Set up automatic investing of even 10 dollars a week. That's it. Over 10 years, that 10 dollars a week becomes over 7,000 dollars. Over 30 years, over 60,000 dollars. The best time to start was yesterday. The second best time is right now.",
        "title": "How to Start Investing With Just $10 — Beginner Guide",
        "description": "You don't need thousands of dollars to start investing. With just 10 dollars you can open an account, buy an index fund, and start building wealth today. Automatic weekly investing is the secret weapon of everyday millionaires. Subscribe for more investing tips.",
        "hashtags": ["investing","beginnerinvesting","indexfunds","personalfinance","wealthbuilding","stockmarket","financialfreedom","moneytips","compoundinterest","invest"],
        "tiktok_caption": "Start investing with just $10 today 📈 No excuses! #investing #beginnerinvesting #personalfinance",
        "hook": "You can start investing today with just $10."
    },
    {
        "script": "Your credit score is costing you thousands of dollars. Here's how to fix it fast. Number one: pay every bill on time. Set up autopay for minimums so you never miss. Number two: keep your credit card balance below 30 percent of the limit. This alone can raise your score 50 points. Number three: don't close old cards even if you don't use them. Length of history matters. A good credit score means lower interest rates on everything — cars, homes, loans. That's worth tens of thousands over your lifetime.",
        "title": "Fix Your Credit Score Fast — 3 Steps That Actually Work",
        "description": "A bad credit score costs you thousands in higher interest rates on loans, cars, and mortgages. These 3 steps can significantly improve your credit score in 90 days or less. Pay on time, lower your utilization rate, and keep old accounts open. Subscribe for more credit and finance tips.",
        "hashtags": ["creditscore","fixcredit","personalfinance","creditrepair","moneytips","financialtips","creditbuilding","goodcredit","creditadvice","financialhealth"],
        "tiktok_caption": "Your credit score is costing you thousands 😤 Fix it with these 3 steps #creditscore #fixcredit #personalfinance",
        "hook": "Your credit score is costing you thousands of dollars."
    },
    {
        "script": "Side hustles are not just for extra cash — they can replace your income. Here are 3 that work in 2026. First, freelance writing. Companies pay 50 to 300 dollars per article. Start on Upwork or Fiverr with no experience needed. Second, reselling. Buy items on sale locally and sell online for profit. People make 2,000 dollars a month doing this part time. Third, digital products. Create one template, guide, or preset and sell it forever with no extra work. The best side hustle is the one you start today. Which one will you try?",
        "title": "3 Side Hustles That Can Replace Your Income in 2026",
        "description": "Side hustles have never been more accessible. Freelance writing, reselling, and digital products are three proven ways to earn extra income in 2026 with minimal startup costs. Many people turn these into full-time income streams. Start small, stay consistent, and scale what works. Subscribe for more side hustle strategies.",
        "hashtags": ["sidehustle","makemoneyonline","extraincome","personalfinance","freelancing","digitalproducts","reselling","incomeideas","workfromhome","financialfreedom"],
        "tiktok_caption": "3 side hustles that can replace your 9-5 in 2026 🔥 #sidehustle #makemoneyonline #extraincome",
        "hook": "These 3 side hustles can replace your full-time income."
    },
    {
        "script": "The 50-30-20 budget rule changed my financial life. Here's how it works. 50 percent of your income goes to needs — rent, food, transport. 30 percent goes to wants — entertainment, dining out, hobbies. 20 percent goes straight to savings and debt. That's it. No complicated spreadsheets. No tracking every coffee. Just three numbers. If you earn 3,000 a month, that's 1,500 for needs, 900 for fun, and 600 saved. Try this for 90 days and watch your finances transform.",
        "title": "The 50-30-20 Budget Rule That Will Change Your Finances",
        "description": "The 50-30-20 rule is the simplest budgeting method that actually works for beginners. Split your income into needs, wants, and savings with no complicated tracking required. This rule works on any income level and helps you save consistently while still enjoying life. Subscribe for more practical money tips.",
        "hashtags": ["budgeting","503020rule","personalfinance","moneytips","savemoney","budgetingforbeginners","financialtips","moneymanagement","savingsgoals","financialplanning"],
        "tiktok_caption": "The 50-30-20 rule will fix your finances 💡 So simple! #budgeting #503020rule #personalfinance",
        "hook": "This one rule will completely fix your budget."
    },
    {
        "script": "What if I told you that your daily coffee habit isn't the reason you're broke? The real budget killers are the big three — housing, transport, and food. Most people spend 70 percent of their income on just these three things. Here's how to cut each one. Negotiate your rent or get a roommate. Buy a reliable used car instead of financing a new one. Meal prep on Sundays. Cutting each by just 10 percent frees up hundreds every month. Focus on the big wins, not the small sacrifices.",
        "title": "The 3 Real Reasons You're Always Broke (It's Not Coffee)",
        "description": "Cutting your daily coffee won't make you rich. The real money drains are housing, transportation, and food — the big three that eat up most people's budgets. Learn how to reduce each one by 10 percent and free up hundreds of dollars every month. Subscribe for honest money advice that makes a real difference.",
        "hashtags": ["budgeting","personalfinance","moneytips","savemoney","financialadvice","moneymanagement","broketo rich","financialfreedom","moneyhacks","realadvice"],
        "tiktok_caption": "Your coffee isn't why you're broke 😂 This is the real reason #budgeting #personalfinance #moneytips",
        "hook": "Your daily coffee isn't why you're broke. This is."
    },
    {
        "script": "Compound interest is the most powerful force in personal finance. Here's a simple example. You invest 1,000 dollars at age 25. At 10 percent return per year, by age 65 that single investment becomes 45,000 dollars. But if you wait until 35 to invest that same 1,000, it only becomes 17,000. Waiting 10 years cut your result by more than half. Time is the ingredient that makes compound interest work. Every year you wait is money you're leaving behind. Start now.",
        "title": "Why Compound Interest Is the Secret to Getting Rich",
        "description": "Compound interest is the eighth wonder of the world and the foundation of all wealth building. The earlier you start investing, the more time your money has to grow exponentially. Even small amounts invested early can grow into life-changing wealth. Subscribe to learn how to make compound interest work for you.",
        "hashtags": ["compoundinterest","investing","wealthbuilding","personalfinance","financialfreedom","moneytips","investearly","retirementplanning","passiveincome","richhabits"],
        "tiktok_caption": "Why waiting to invest is costing you EVERYTHING 😱 #compoundinterest #investing #wealthbuilding",
        "hook": "Waiting 10 years to invest cuts your wealth in half."
    },
    {
        "script": "An emergency fund is not optional — it's the foundation of financial security. Without one, any unexpected expense sends you into debt. Here's how to build one fast. Step one: open a separate high-yield savings account. Keep it away from your main account so you don't touch it. Step two: automate a fixed transfer every payday — even 50 dollars. Step three: throw any windfalls in — tax refunds, bonuses, gifts. Your goal is 3 months of expenses. Start with 1,000 as your first milestone.",
        "title": "How to Build an Emergency Fund From Scratch",
        "description": "An emergency fund is the most important financial safety net you can have. Without one, any car repair, medical bill, or job loss sends you spiraling into debt. Learn how to build a 3-month emergency fund step by step even on a tight budget. Subscribe for more foundational money tips.",
        "hashtags": ["emergencyfund","personalfinance","savemoney","financialsecurity","moneytips","savingsgoals","budgeting","financialplanning","moneyhacks","savingsaccount"],
        "tiktok_caption": "No emergency fund = one bad day away from debt 😰 Here's how to build one #emergencyfund #personalfinance #savemoney",
        "hook": "Without an emergency fund, you're one bad day away from debt."
    },
    {
        "script": "Debt is a trap and here's how to escape it faster than you think. Use the debt avalanche method. List all your debts from highest interest rate to lowest. Pay minimums on everything. Then throw every extra dollar at the highest interest debt first. Once it's gone, roll that payment into the next one. This saves the most money in interest over time. The average person using this method pays off all debt 2 years faster. Your income is your most powerful wealth-building tool — stop giving it to banks.",
        "title": "Pay Off All Your Debt 2 Years Faster With This Method",
        "description": "The debt avalanche method is mathematically the fastest way to become debt free. By targeting high-interest debt first and rolling payments forward, you save thousands in interest and pay off everything years sooner. Stop letting banks profit from your debt. Subscribe for more debt freedom strategies.",
        "hashtags": ["debtfree","debtpayoff","personalfinance","debtavalanche","moneytips","financialfreedom","payoffdebt","debtfreecommunity","moneyadvice","creditcarddebt"],
        "tiktok_caption": "Pay off all debt 2 YEARS faster with this method 🔥 #debtfree #debtpayoff #personalfinance",
        "hook": "You can pay off all your debt 2 years faster with this one method."
    },
    {
        "script": "Most people don't know that negotiating your salary is one of the highest ROI activities you can do. A 5,000 dollar raise compounded over a 30-year career is worth over 400,000 dollars. Here's how to do it. Research market rate on Glassdoor or LinkedIn Salary. Ask for 10 to 15 percent above your target. Never give the first number. Say: I'm looking for something in the range of X based on my research and experience. Silence after your ask is your friend. Most people leave hundreds of thousands on the table by never asking.",
        "title": "How Negotiating Your Salary Can Make You $400K More",
        "description": "Salary negotiation is the highest return on investment activity most people never do. A single successful negotiation can be worth hundreds of thousands over your career. Learn the exact script to ask for more money with confidence. Subscribe for career and money tips that change your financial future.",
        "hashtags": ["salarynegotiation","careertips","personalfinance","makemoremoney","negotiation","moneytips","careergrowth","wealthbuilding","jobadvice","financialtips"],
        "tiktok_caption": "Never negotiating your salary costs you $400K 😳 Here's the script #salarynegotiation #careertips #personalfinance",
        "hook": "Never negotiating your salary costs you $400,000 over your career."
    },
    {
        "script": "Passive income sounds like a dream but it's very real. Here are 3 ways to earn money while you sleep. First, dividend stocks. Buy shares in companies that pay quarterly dividends. Even 10,000 dollars in dividend stocks can pay 300 to 500 dollars a year in passive income. Second, rental income. Even renting a spare room on Airbnb earns 500 to 1,500 per month. Third, digital products. Create an ebook, template, or course once and sell it forever. Passive income takes work upfront. But the payoff is freedom.",
        "title": "3 Real Ways to Earn Passive Income in 2026",
        "description": "Passive income is not a myth — it's a strategy. Dividend stocks, rental income, and digital products are three proven passive income streams anyone can start. Learn how to build income that works while you sleep and start your journey to financial freedom. Subscribe for more passive income strategies.",
        "hashtags": ["passiveincome","makemoneyonline","financialfreedom","dividends","rentalincome","digitalproducts","wealthbuilding","personalfinance","incomeideas","sidehustle"],
        "tiktok_caption": "3 ways to earn money while you sleep 😴💰 #passiveincome #makemoneyonline #financialfreedom",
        "hook": "3 real ways to earn money while you sleep."
    },
    {
        "script": "Your 20s are the most important decade for your finances. Here's what to do before you turn 30. One: build your emergency fund — 3 months of expenses minimum. Two: invest in your employer's retirement plan and get the full company match — that's free money. Three: build your credit score to above 700. Four: learn one high-income skill — coding, sales, writing, design. Five: avoid lifestyle inflation when you get raises. The decisions you make in your 20s will define your financial life for decades. Make them count.",
        "title": "5 Money Moves to Make Before You Turn 30",
        "description": "Your 20s are the most powerful decade for building wealth. The financial decisions you make now will compound for decades. Build your emergency fund, invest early, build credit, learn a high-income skill, and avoid lifestyle inflation. These 5 moves will set you up for life. Subscribe for more money advice for young adults.",
        "hashtags": ["moneyin20s","personalfinance","youngadults","financialtips","investing","wealthbuilding","moneymoves","financialfreedom","adulting","moneyadvice"],
        "tiktok_caption": "Do these 5 money moves before 30 or you'll regret it 😬 #moneyin20s #personalfinance #youngadults",
        "hook": "5 money moves you must make before turning 30."
    },
    {
        "script": "Most people are overpaying for car insurance by hundreds of dollars every year. Here's how to fix it in 10 minutes. Call your insurance company and ask for a loyalty discount. Most give 5 to 10 percent just for asking. Then go to a comparison site and get 3 competing quotes. Call your insurer back with the lowest quote and ask them to match it. If they won't, switch. Also, increasing your deductible from 500 to 1,000 dollars can reduce your premium by 15 percent. One phone call. Hundreds saved.",
        "title": "Stop Overpaying for Car Insurance — Save $300 This Year",
        "description": "Millions of people overpay for car insurance every single year. With one phone call and 10 minutes of your time you can save hundreds of dollars annually. Learn how to negotiate your premium, use competing quotes, and adjust your deductible to cut costs without losing coverage. Subscribe for more money-saving hacks.",
        "hashtags": ["carinsurance","savemoney","moneyhacks","personalfinance","insurancetips","moneysaving","financialtips","budgeting","adulting","moneytips"],
        "tiktok_caption": "You're overpaying for car insurance — fix it in 10 mins 🚗💸 #carinsurance #savemoney #moneyhacks",
        "hook": "You're overpaying for car insurance by hundreds every year."
    },
    {
        "script": "The stock market seems scary but it doesn't have to be. Here's the simplest investing strategy that beats most professional fund managers. Buy an S&P 500 index fund every month no matter what the market is doing. This strategy is called dollar cost averaging. You buy more shares when prices are low and fewer when prices are high. Over any 20-year period in history, the S&P 500 has never lost money. You don't need to pick stocks. You don't need to time the market. Just keep buying.",
        "title": "The Simplest Investment Strategy That Beats Most Experts",
        "description": "Dollar cost averaging into an S&P 500 index fund is the simplest and most effective investment strategy for most people. No stock picking, no market timing, no financial advisor needed. This strategy has beaten the majority of professional fund managers over long periods. Subscribe for more beginner investing tips.",
        "hashtags": ["investing","indexfunds","sp500","dollarcostAveraging","personalfinance","stockmarket","wealthbuilding","beginnerinvesting","moneytips","financialfreedom"],
        "tiktok_caption": "This simple strategy beats most expert investors 📊 #investing #indexfunds #sp500",
        "hook": "This simple strategy beats most professional investors."
    },
    {
        "script": "You're probably leaving free money on the table right now. Here are 5 types of free money most people never claim. One: employer 401k match — contribute enough to get the full match. Two: cash back credit cards — use them for regular purchases and pay in full. Three: bank account bonuses — banks pay 200 to 500 dollars to open a new account. Four: rebate apps like Rakuten — earn cash back on online shopping. Five: tax deductions — most people miss the home office, student loan interest, and charity deductions. Free money is everywhere.",
        "title": "5 Types of Free Money You're Probably Not Claiming",
        "description": "Free money exists everywhere if you know where to look. Employer matches, cashback cards, bank bonuses, rebate apps, and overlooked tax deductions are leaving thousands on the table for most people. Learn how to claim every dollar you're owed. Subscribe for more money hacks and tips.",
        "hashtags": ["freemoney","moneyhacks","personalfinance","cashback","moneytips","financialtips","savemoney","401k","taxdeductions","wealthbuilding"],
        "tiktok_caption": "5 types of FREE money you're missing out on 🤑 #freemoney #moneyhacks #personalfinance",
        "hook": "You're leaving free money on the table right now."
    },
    {
        "script": "Renting versus buying a home — which is actually better? The truth is it depends on your situation. Buying builds equity over time but comes with hidden costs — property tax, maintenance, insurance, HOA fees. These can add 2 to 3 percent of the home value per year. Renting gives you flexibility and keeps capital free to invest. If you invest the down payment instead of buying, historically you end up in a similar financial position. The best home is the one that fits your life, not just your finances.",
        "title": "Renting vs Buying a Home — The Truth Nobody Tells You",
        "description": "The rent vs buy debate is more nuanced than most people think. Buying isn't always better — hidden costs, opportunity cost of the down payment, and reduced flexibility can make renting the smarter financial choice in many situations. Learn how to make the right decision for your specific situation. Subscribe for more financial truth.",
        "hashtags": ["rentingvsbuying","personalfinance","homebuying","realestate","moneytips","financialadvice","firsttimehomebuyer","rentvsbuy","housingmarket","financialplanning"],
        "tiktok_caption": "Renting vs buying — the truth nobody tells you 🏠 #rentingvsbuying #personalfinance #homebuying",
        "hook": "Buying a home is not always the smartest financial decision."
    },
    {
        "script": "If you got a 1,000 dollar windfall today — tax refund, bonus, gift — here's exactly how to use it. First 500: pay off the highest interest debt you have. If no debt, add to your emergency fund. Next 300: invest in an index fund. Open an account today if you don't have one. Last 200: spend on something that brings you joy — guilt free. The key is having a plan before the money arrives. Without a plan, windfalls disappear within 30 days. With a plan, they build wealth.",
        "title": "What to Do With a $1,000 Windfall — The Smart Way",
        "description": "Most people waste unexpected money within a month because they have no plan for it. Whether it's a tax refund, bonus, or gift, having a framework for windfalls turns them into wealth-building tools. Learn the exact split that maximizes your financial progress while still enjoying the money. Subscribe for more smart money strategies.",
        "hashtags": ["windfall","moneytips","personalfinance","taxrefund","savemoney","investing","debtpayoff","smartmoney","financialplanning","moneyhacks"],
        "tiktok_caption": "Got a $1000 windfall? Here's EXACTLY what to do with it 💰 #windfall #moneytips #personalfinance",
        "hook": "Got $1,000 unexpectedly? Here's exactly what to do with it."
    },
    {
        "script": "Most people think they need a financial advisor to invest. You don't. Here's a complete beginner portfolio you can set up in 30 minutes. Put 60 percent in a total US stock market index fund. Put 30 percent in an international stock index fund. Put 10 percent in a bond index fund. Rebalance once a year. That's it. This three-fund portfolio has outperformed most actively managed funds over 20 years. Low fees. Low effort. High returns. You don't need Wall Street to build wealth.",
        "title": "The 3-Fund Portfolio — All You Need to Build Wealth",
        "description": "The three-fund portfolio is the simplest and most effective investment strategy for long-term wealth building. US stocks, international stocks, and bonds in the right proportions beat most managed funds over time. Set it up in 30 minutes and review once a year. No advisor needed. Subscribe for more DIY investing tips.",
        "hashtags": ["threefundportfolio","investing","indexfunds","personalfinance","wealthbuilding","diyinvesting","stockmarket","financialfreedom","beginnerinvesting","moneytips"],
        "tiktok_caption": "The only investment portfolio you'll ever need 📈 #threefundportfolio #investing #indexfunds",
        "hook": "You only need 3 funds to build real wealth."
    },
    {
        "script": "Lifestyle inflation is silently destroying your wealth. Here's how it works. You get a raise. Instead of saving the extra, you upgrade your car, move to a nicer apartment, eat out more. Your expenses rise to meet your income. You feel richer but your savings rate stays the same. The fix: every time you get a raise, save at least half of it before you touch it. Automate the transfer so you never see it. Live like you didn't get the raise. Do this consistently and you will retire wealthy even on an average income.",
        "title": "Lifestyle Inflation Is Secretly Keeping You Broke",
        "description": "Lifestyle inflation — spending more every time you earn more — is the silent wealth killer. Most people get raise after raise but never build real wealth because expenses always catch up with income. Learn how to break the cycle and actually benefit from earning more. Subscribe for more wealth-building strategies.",
        "hashtags": ["lifestyleinflation","personalfinance","wealthbuilding","moneytips","savemoney","financialfreedom","moneyhabits","richhabits","budgeting","financialmindset"],
        "tiktok_caption": "Getting raises but still broke? This is why 😩 #lifestyleinflation #personalfinance #wealthbuilding",
        "hook": "Getting raises but still broke? This is why."
    },
    {
        "script": "Here's something schools never taught you about taxes. You can legally reduce how much you pay. Contribute to a 401k or IRA — every dollar you put in reduces your taxable income. Use an HSA if you have a high-deductible health plan — triple tax advantage. Claim every deduction you qualify for — home office, student loan interest, charitable donations. If you're self-employed, you can deduct a phone, internet, and business expenses. The average person overpays taxes by thousands every year just from lack of knowledge.",
        "title": "Legal Ways to Pay Less Tax That Schools Never Taught You",
        "description": "Most people overpay taxes every year because they don't know about legal deductions and tax-advantaged accounts. 401k contributions, HSA accounts, and proper deductions can save you thousands annually. This isn't tax evasion — it's using the system the way it was designed. Subscribe for more tax and money tips.",
        "hashtags": ["taxes","taxhacks","personalfinance","moneytips","taxdeductions","401k","HSA","savemoney","financialtips","legaladvice"],
        "tiktok_caption": "Legal ways to pay way less in taxes 💡 Schools never taught this #taxes #taxhacks #personalfinance",
        "hook": "You're legally allowed to pay less in taxes — here's how."
    },
    {
        "script": "The number one financial mistake young people make is waiting. Waiting to invest. Waiting to save. Waiting until they earn more. Here's the math that should scare you into action. If you invest 200 dollars a month starting at 25, at a 10 percent return you'll have 1.3 million at 65. If you start at 35, same amount, same return — only 456,000. That 10-year delay cost you nearly a million dollars. Time in the market always beats timing the market. Start today. Even 50 dollars a month. Just start.",
        "title": "Starting to Invest at 25 vs 35 — The $1 Million Difference",
        "description": "The cost of waiting to invest is staggering. Starting just 10 years earlier can result in nearly a million dollars more at retirement due to compound interest. Every month you delay investing is compounding working against you instead of for you. Subscribe for motivation and tips to start investing today.",
        "hashtags": ["investing","compoundinterest","personalfinance","moneytips","startinvesting","wealthbuilding","financialfreedom","beginnerinvesting","retirementplanning","youngadults"],
        "tiktok_caption": "Waiting 10 years to invest costs you $1 MILLION 😱 #investing #compoundinterest #personalfinance",
        "hook": "Waiting 10 years to invest costs you nearly $1 million."
    },
    {
        "script": "Most people think budgeting means cutting out everything fun. It doesn't. Here's the anti-budget method. First, pay yourself — move your savings goal to a separate account the day you get paid. Then pay all your fixed bills. Whatever is left — spend freely on whatever you want. No tracking. No guilt. The key is saving first, not last. Most people save what's left after spending. Wealthy people spend what's left after saving. Flip the order and everything changes.",
        "title": "The Anti-Budget Method — Save Money Without Tracking",
        "description": "Traditional budgeting feels restrictive and most people quit within weeks. The anti-budget method flips the script — save first, then spend the rest however you want with zero guilt and zero tracking. This simple mindset shift is how millions of people build wealth without feeling deprived. Subscribe for more effortless money tips.",
        "hashtags": ["antibudget","budgeting","personalfinance","savemoney","moneytips","financialtips","payourselffirst","moneyhacks","savingsgoals","financialfreedom"],
        "tiktok_caption": "Budget without tracking every dollar 🙌 The anti-budget method #antibudget #budgeting #personalfinance",
        "hook": "Save money every month without tracking a single dollar."
    },
    {
        "script": "Financial freedom doesn't mean being rich. It means having enough passive income to cover your expenses. Here's how to calculate your freedom number. Add up all your monthly expenses. Multiply by 12 to get your annual expenses. Multiply that by 25. That's your financial freedom number — the amount you need invested to live off returns forever. If you spend 2,000 a month, your freedom number is 600,000. It sounds like a lot. But invested at 10 percent a year, 600,000 generates 60,000 dollars annually. Freedom is a math problem.",
        "title": "Calculate Your Financial Freedom Number in 60 Seconds",
        "description": "Financial freedom is not about being a millionaire — it's about having enough invested to cover your expenses from returns alone. Learn how to calculate your personal freedom number and build a plan to reach it. The math is simpler than you think. Subscribe for more financial independence strategies.",
        "hashtags": ["financialfreedom","FIRE","personalfinance","financialindependence","moneytips","wealthbuilding","passiveincome","retirementplanning","freedomnumber","investing"],
        "tiktok_caption": "Calculate your financial freedom number in 60 seconds ⏱️ #financialfreedom #FIRE #personalfinance",
        "hook": "Financial freedom is a math problem — here's how to solve it."
    },
    {
        "script": "Here's why keeping all your money in a savings account is actually losing you money. Inflation runs at 3 percent per year on average. A regular savings account pays 0.1 percent. That means your money is losing 2.9 percent of its value every single year. A high-yield savings account pays 4 to 5 percent — beating inflation. And investing in index funds historically returns 10 percent per year. Keeping cash under the mattress or in a regular savings account is a choice to get poorer slowly. Move your money where it works.",
        "title": "Why Keeping Money in a Savings Account Is Making You Poor",
        "description": "A regular savings account is silently destroying your wealth through inflation. When your savings earn less than inflation, you're getting poorer every year. High-yield savings accounts and index fund investing are two ways to make your money actually grow. Subscribe for more tips on making your money work harder.",
        "hashtags": ["savingsaccount","inflation","personalfinance","moneytips","hysa","investing","wealthbuilding","financialtips","makeyourmoneywork","financialfreedom"],
        "tiktok_caption": "Your savings account is making you POORER 😳 Here's why #savingsaccount #inflation #personalfinance",
        "hook": "Your savings account is making you poorer every year."
    },
    {
        "script": "Here are 5 money habits to start this week that will change your finances in 90 days. One: check your bank balance every morning — awareness is everything. Two: pack lunch 3 days a week — saves 150 dollars a month. Three: unsubscribe from retail emails — out of sight out of mind. Four: set a spending alarm — most banking apps let you set alerts. Five: automate a 50-dollar weekly savings transfer. None of these are hard. All of them work. The only question is will you start today or keep waiting.",
        "title": "5 Money Habits That Will Change Your Finances in 90 Days",
        "description": "Small daily habits compound into massive financial results over time. These 5 money habits are simple enough to start this week and powerful enough to transform your finances within 90 days. Consistency beats intensity in personal finance every time. Subscribe for more actionable money habits.",
        "hashtags": ["moneyhabits","personalfinance","moneytips","financialhabits","savemoney","budgeting","financialfreedom","wealthbuilding","moneymindset","dailyhabits"],
        "tiktok_caption": "5 money habits that change everything in 90 days ✅ #moneyhabits #personalfinance #moneytips",
        "hook": "5 money habits to start this week that will transform your finances."
    },
    {
        "script": "Most people don't realize that your biggest wealth-building asset is not your investments — it's your income. And the fastest way to increase income is to become more valuable. Here's how. Learn one skill that companies desperately need — data analysis, digital marketing, copywriting, or coding. You can learn any of these free on YouTube in 6 months. Then freelance on the side to build a portfolio. Then either go full-time freelance or use the skill to negotiate a higher salary. Invest the increase. Repeat. This is the wealth formula.",
        "title": "The Real Wealth Formula Nobody Talks About",
        "description": "Building wealth starts with increasing your income, not just cutting expenses. Learning high-demand skills, freelancing to build a portfolio, and investing the extra income is the most reliable path to financial freedom. Subscribe for more career and money strategies that actually work.",
        "hashtags": ["wealthformula","personalfinance","highincomereskills","freelancing","moneytips","wealthbuilding","financialfreedom","investing","careergrowth","makemoremoney"],
        "tiktok_caption": "The real wealth formula nobody talks about 💡 #wealthformula #personalfinance #highincomereskills",
        "hook": "Your biggest wealth-building asset isn't your investments — it's your income."
    },
    {
        "script": "Here's the truth about credit cards. Used wrong, they're a debt trap. Used right, they're free money. Here's how to use them right. Only spend what you already have in your bank account. Pay the full balance every month — never just the minimum. Use a cashback card for all regular purchases — groceries, gas, bills. That's 1 to 5 percent back on money you were spending anyway. A family spending 2,000 a month on a 2 percent cashback card earns 480 dollars a year for free. Credit cards are tools. Master the tool.",
        "title": "How to Use Credit Cards to Make Money Instead of Lose It",
        "description": "Credit cards are either your best financial tool or your worst enemy — it all depends on how you use them. Learn the simple rules that turn credit cards into a cashback machine while building your credit score. Pay in full, use rewards wisely, and never pay interest. Subscribe for more smart money strategies.",
        "hashtags": ["creditcards","cashback","personalfinance","moneytips","creditcardhacks","smartmoney","financialtips","creditbuilding","moneyhacks","rewardscards"],
        "tiktok_caption": "How to make money with credit cards (legally) 💳💰 #creditcards #cashback #personalfinance",
        "hook": "Credit cards can make you money — if you use them right."
    },
    {
        "script": "Retirement feels far away but the math makes it urgent. Here's what you need to save to retire comfortably. To replace 50,000 dollars a year in retirement you need 1.25 million invested. That sounds impossible but here's the math. Invest 500 dollars a month for 30 years at 10 percent return and you end up with 1.13 million. That's 16 dollars a day. Skip one restaurant meal and one coffee a day and you're there. Retirement is not a dream. It's a daily decision. Make the right one.",
        "title": "How Much You Need to Retire — And How to Get There",
        "description": "Retirement planning feels overwhelming but the math is surprisingly achievable. To retire comfortably you need roughly 25 times your annual expenses invested. Learn how much to save monthly based on your timeline and how to make it automatic. Subscribe for more retirement planning tips made simple.",
        "hashtags": ["retirement","retirementplanning","personalfinance","moneytips","investing","401k","financialfreedom","retireearly","wealthbuilding","financialplanning"],
        "tiktok_caption": "Here's exactly how much you need to retire 🧮 #retirement #retirementplanning #personalfinance",
        "hook": "Here's exactly how much money you need to retire comfortably."
    },
]

# ── Main ──────────────────────────────────────────────────────────────────────

USED_INDEX_FILE = "./temp/used_scripts.json"

def load_used():
    os.makedirs("./temp", exist_ok=True)
    if os.path.exists(USED_INDEX_FILE):
        with open(USED_INDEX_FILE) as f:
            return json.load(f)
    return []

def save_used(used):
    with open(USED_INDEX_FILE, "w") as f:
        json.dump(used, f)

def main():
    used = load_used()
    all_indices = list(range(len(SCRIPTS)))

    # Find unused scripts
    unused = [i for i in all_indices if i not in used]

    # If all used, reset and start over
    if not unused:
        print("All 30 scripts used — resetting cycle.")
        used = []
        unused = all_indices

    # Pick a random unused script
    index = random.choice(unused)
    script_data = SCRIPTS[index]

    # Mark as used
    used.append(index)
    save_used(used)

    os.makedirs("./temp", exist_ok=True)
    with open("./temp/script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)

    print(f"Script {index + 1}/30 saved to ./temp/script.json")
    print(f"Scripts used this cycle: {len(used)}/30")
    print(f"Title: {script_data['title']}")
    print(f"Hook:  {script_data['hook']}")


if __name__ == "__main__":
    main()
