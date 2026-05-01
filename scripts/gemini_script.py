#!/usr/bin/env python3
"""
gemini_script.py — picks a random unused psychology/mind fact script
Output: ./temp/script.json
"""

import os
import json
import random

SCRIPTS = [
    {
        "script": "Your brain makes 35,000 decisions every single day — and most of them happen without you even knowing it. Scientists call this the unconscious mind, and it controls about 95 percent of everything you do. Your posture, your tone of voice, the route you take to work — all automatic. Here's what's wild: the conscious part of your brain, the part you think is in charge, is really just the tip of the iceberg. The real power is underneath. Understanding your unconscious is the first step to changing your habits, your reactions, and your life.",
        "title": "Your Brain Makes 35000 Decisions a Day Without You",
        "description": "The unconscious mind controls 95% of your behavior. Learn how your brain makes thousands of automatic decisions daily and how understanding this can help you change habits and improve your life.",
        "hashtags": ["psychology","mindfacts","brain","unconsciousmind","mentalhealth","mindpower","brainfacts","selfdevelopment","mindset","neuroscience"],
        "tiktok_caption": "Your brain is making 35,000 decisions without you #psychology #mindfacts #brain",
        "hook": "Your brain makes 35,000 decisions every day — without your permission."
    },
    {
        "script": "Did you know that loneliness is as physically dangerous as smoking 15 cigarettes a day? Research from Brigham Young University found that social isolation increases the risk of early death by 26 percent. Your brain literally treats social rejection the same way it treats physical pain — the same neural pathways light up. This is why a breakup or being left out can feel so physically awful. Humans are wired for connection. It's not a luxury — it's a biological need. Make time for real relationships. Your life literally depends on it.",
        "title": "Loneliness Is as Deadly as Smoking 15 Cigarettes a Day",
        "description": "Science shows chronic loneliness is as harmful as smoking. Your brain treats social rejection like physical pain. Learn why human connection is a biological necessity, not a luxury.",
        "hashtags": ["psychology","loneliness","mentalhealth","brainfacts","socialconnection","mindfacts","wellbeing","humanconnection","neuroscience","mindhealth"],
        "tiktok_caption": "Loneliness is as deadly as smoking — science says so #psychology #loneliness #mentalhealth",
        "hook": "Loneliness is as dangerous as smoking 15 cigarettes a day."
    },
    {
        "script": "Here's a mind trick that can completely change how you see yourself. It's called cognitive reframing, and therapists use it to treat anxiety and depression. Instead of saying I failed, say I learned what doesn't work. Instead of I'm terrible at this, say I'm getting better at this. Your brain believes what you tell it. The words you use to describe your experiences physically shape the neural pathways in your mind. Positive reframing isn't toxic positivity — it's neuroscience. The story you tell yourself becomes the life you live.",
        "title": "The Mind Trick Therapists Use to Rewire Your Brain",
        "description": "Cognitive reframing is a proven therapy technique that changes how your brain interprets experiences. Learn how to shift your self-talk to literally rewire neural pathways and improve your mental outlook.",
        "hashtags": ["psychology","cognitivereframing","mentalhealth","mindfacts","brainhacks","therapy","mindset","selftalk","brainscience","mindpower"],
        "tiktok_caption": "This mind trick rewires your brain — therapists use it daily #psychology #cognitivereframing #mentalhealth",
        "hook": "This one mind trick can completely change how you see yourself."
    },
    {
        "script": "The average person has between 60,000 and 80,000 thoughts per day. About 80 percent of those thoughts are negative, and 95 percent are the exact same thoughts you had yesterday. Your mind is stuck in a loop. This negativity bias evolved to keep our ancestors alive — always scanning for threats. But in modern life, it works against us. The fix? Mindfulness. When you notice a thought, you break the automatic loop. You become the observer, not the prisoner. Awareness is the first step to freedom.",
        "title": "80 Percent of Your Daily Thoughts Are Negative Here Is the Fix",
        "description": "Research shows most daily thoughts are negative and repetitive. This negativity bias is ancient evolution working against modern life. Learn how mindfulness breaks the cycle and gives you back control.",
        "hashtags": ["psychology","negativitybias","mindfulness","mindfacts","brainfacts","mentalhealth","thoughts","mindpower","awareness","neuroscience"],
        "tiktok_caption": "80% of your thoughts are negative — here's how to fix that #psychology #negativitybias #mindfulness",
        "hook": "80 percent of your daily thoughts are negative — and most repeat every single day."
    },
    {
        "script": "There's a psychological phenomenon called the Dunning-Kruger effect that explains why the least competent people are often the most confident. When you know very little about a subject, you don't know enough to know what you don't know. So you feel confident. As you learn more, you realize how complex it is and your confidence drops. Then, as you master it, confidence climbs again — but now it's real expertise. The most dangerous people in any room are often the ones who've read one article on a topic. True wisdom begins with knowing what you don't know.",
        "title": "Why the Least Competent People Are Always the Most Confident",
        "description": "The Dunning-Kruger effect explains why beginners overestimate their abilities while experts underestimate theirs. Understanding this helps you spot overconfidence in yourself and others.",
        "hashtags": ["psychology","dunningkruger","mindfacts","brainfacts","cognitivebias","selfdevelopment","criticalthinking","mindset","awareness","psychology101"],
        "tiktok_caption": "Why incompetent people are always so confident — the Dunning-Kruger effect #psychology #dunningkruger #mindfacts",
        "hook": "The least skilled people are usually the most confident — here's the psychology."
    },
    {
        "script": "Your gut has its own nervous system with over 100 million neurons — more than your spinal cord. Scientists call it the second brain. It communicates directly with your actual brain through the vagus nerve, and 90 percent of the signals travel upward from gut to brain, not the other way around. This is why stress gives you stomach problems, and why your gut feelings are often right. The connection between digestive health and mental health is so strong that scientists believe poor gut health may contribute to depression and anxiety. Feed your gut well — you're feeding your mind.",
        "title": "Your Gut Has 100 Million Neurons It Is Your Second Brain",
        "description": "With 100 million neurons and a direct line to your brain, your gut influences mood, mental health, and decision-making in ways science is just beginning to understand.",
        "hashtags": ["psychology","gutbrain","secondbrain","mindfacts","brainfacts","mentalhealth","guthealth","neuroscience","brainscience","mindpower"],
        "tiktok_caption": "Your gut has 100 million neurons — it's literally your second brain #psychology #gutbrain #mindfacts",
        "hook": "Your gut has its own brain with 100 million neurons."
    },
    {
        "script": "Mirror neurons are one of the most fascinating discoveries in neuroscience. When you watch someone get hurt, the same neurons fire in your brain as if you were hurt yourself. When you watch someone smile, your mirror neurons activate a smile response in your own brain. This is the biological basis of empathy. It's also why yawning is contagious, why you flinch watching action movies, and why spending time with positive people literally changes your brain chemistry. You absorb the emotions of the people around you. Choose your circle wisely.",
        "title": "Mirror Neurons Why You Feel What Others Feel",
        "description": "Mirror neurons fire when you watch others experience something, creating the physical basis of empathy. This explains contagious yawning, emotional contagion, and why your social circle directly shapes your brain chemistry.",
        "hashtags": ["psychology","mirrorneurons","empathy","mindfacts","neuroscience","brainfacts","emotionalintelligence","brainscience","mindpower","psychology101"],
        "tiktok_caption": "Mirror neurons explain why you feel what others feel #psychology #mirrorneurons #empathy",
        "hook": "When you watch someone get hurt, your brain responds as if it happened to you."
    },
    {
        "script": "The Placebo Effect is one of the most powerful forces in medicine — and it works even when you know it's a placebo. Studies at Harvard showed that patients who were told they were taking sugar pills still experienced significant improvements in their symptoms. Your mind has the power to change your body's chemistry based purely on belief. Pain relief, immune response, even blood pressure — all influenced by belief alone. The flip side is the nocebo effect: negative expectations cause real harm. What you believe about your health literally shapes your biology.",
        "title": "The Placebo Effect Works Even When You Know It Is Fake",
        "description": "Harvard studies proved the placebo effect works even when patients know they're taking sugar pills. Your beliefs physically alter your body chemistry and health outcomes.",
        "hashtags": ["psychology","placeboeffect","mindfacts","brainfacts","mindbody","mentalhealth","neuroscience","mindpower","healthpsychology","brainscience"],
        "tiktok_caption": "The placebo effect works even when you know it's fake #psychology #placeboeffect #mindfacts",
        "hook": "The Placebo Effect works even when you know you're taking a sugar pill."
    },
    {
        "script": "The Baader-Meinhof phenomenon explains why once you notice something for the first time, you suddenly see it everywhere. You buy a red car and suddenly red cars are everywhere. You learn a new word and hear it three times that week. Your brain didn't create new things — it just started filtering for them. This is your reticular activating system at work. It filters the 11 million bits of information hitting your senses every second down to the 40 you can consciously process. What you focus on is what you see. Set your mental filter to what you want to attract.",
        "title": "Why You See Something Everywhere After Learning About It",
        "description": "The Baader-Meinhof phenomenon and your reticular activating system explain why new knowledge seems to appear everywhere. Your brain filters 11 million bits of data per second — and focus determines what you notice.",
        "hashtags": ["psychology","baadermeinhof","mindfacts","brainfacts","reticularsystem","cognitivebias","brainscience","awareness","mindpower","psychology101"],
        "tiktok_caption": "Once you notice something, you see it EVERYWHERE — here's why #psychology #baadermeinhof #mindfacts",
        "hook": "Ever notice something new and then see it everywhere? Your brain is doing this on purpose."
    },
    {
        "script": "Studies show that writing down your goals makes you 42 percent more likely to achieve them. When you write by hand, your brain engages both hemispheres — the logical left and the creative right. Writing activates your encoding process, which moves information from short-term to long-term memory. And when you describe your goal as if it's already happened, you trigger the same brain regions as when you actually experience something. Your brain doesn't distinguish much between vivid imagination and reality. Write your future into existence.",
        "title": "Writing Your Goals Makes You 42 Percent More Likely to Achieve Them",
        "description": "Handwriting goals engages both brain hemispheres and activates memory encoding. When written as already achieved, your brain treats them as real experiences.",
        "hashtags": ["psychology","goalwriting","mindfacts","brainfacts","neuroscience","productivity","mindpower","journaling","brainscience","motivation"],
        "tiktok_caption": "Write your goals down — it makes you 42% more likely to achieve them #psychology #goalwriting #mindfacts",
        "hook": "Writing your goals down makes you 42 percent more likely to achieve them."
    },
    {
        "script": "Decision fatigue is real and it's why you make worse choices later in the day. Judges in Israel were studied and found to approve paroles 65 percent of the time in morning sessions — dropping to nearly zero by end of day. Your brain uses glucose to make decisions, and it runs low over time. This is why Mark Zuckerberg wears the same clothes every day — to eliminate one decision. The fix: make your most important decisions in the morning, automate small daily choices, and eat before big decisions. Guard your mental energy.",
        "title": "Why You Make Worse Decisions as the Day Goes On",
        "description": "Decision fatigue is proven by research — your brain burns glucose making choices, and performance deteriorates by end of day. Learn how to protect your mental energy.",
        "hashtags": ["psychology","decisionfatigue","mindfacts","brainfacts","productivity","neuroscience","mentalenergy","brainscience","mindpower","psychology101"],
        "tiktok_caption": "Why you make BAD decisions by evening — decision fatigue explained #psychology #decisionfatigue #mindfacts",
        "hook": "Your brain makes worse decisions the more choices it makes — here's the science."
    },
    {
        "script": "The human brain physically changes shape based on what you repeatedly think and do. This is called neuroplasticity. London taxi drivers, who memorize thousands of routes, have a measurably larger hippocampus than average. Musicians who practice intensively develop thicker motor cortex regions. Meditators show structural changes in their prefrontal cortex after just 8 weeks. Your brain is not fixed — it's constantly being sculpted by your habits, thoughts, and experiences. Every repetition, every practice session, every chosen thought is literally reshaping your mind.",
        "title": "Your Brain Physically Changes Shape Based on Your Habits",
        "description": "Neuroplasticity proves the brain rewires and reshapes itself throughout life. Taxi drivers, musicians, and meditators all show measurable brain structural changes from repeated practice.",
        "hashtags": ["psychology","neuroplasticity","mindfacts","brainfacts","brainhacks","neuroscience","brainscience","habits","mindpower","psychology101"],
        "tiktok_caption": "Your brain literally changes shape based on your habits #psychology #neuroplasticity #mindfacts",
        "hook": "Your brain is physically being reshaped right now by your habits."
    },
    {
        "script": "Color psychology is one of the most powerful and least talked about influences on human behavior. Red raises your heart rate and creates urgency — that's why sales signs are red. Blue creates trust and calm — why banks and hospitals use it. Yellow triggers anxiety in large amounts. Green reduces stress and is easiest on the eyes. Fast food chains use red and yellow together because they increase appetite and create urgency to eat quickly and leave. You are being emotionally manipulated by color every single day. Now you see it.",
        "title": "How Colors Secretly Control Your Emotions and Behavior",
        "description": "Color psychology shows that colors directly affect heart rate, appetite, trust, and anxiety. Marketers use this science to influence behavior without your knowledge.",
        "hashtags": ["psychology","colorpsychology","mindfacts","brainfacts","behavioralpsychology","mindpower","marketing","brainscience","perception","psychology101"],
        "tiktok_caption": "Colors are secretly controlling your emotions #psychology #colorpsychology #mindfacts",
        "hook": "The colors around you are controlling your emotions without your knowledge."
    },
    {
        "script": "Studies from Harvard show that people spend 46.9 percent of their waking hours thinking about something other than what they're doing — and this mind-wandering makes them unhappy. The research found that how present you are in an activity is a stronger predictor of happiness than what activity you're doing. Washing dishes while focused on washing dishes makes people happier than washing dishes while thinking about something better. The present moment is the only place where life actually happens. Your ability to stay here, in this moment, is one of the most powerful skills you can develop.",
        "title": "Harvard Study Being Present Is the Real Key to Happiness",
        "description": "Harvard researchers found people spend 47% of waking hours mind-wandering, and it makes them unhappy. Presence in any activity predicts happiness more than the activity itself.",
        "hashtags": ["psychology","mindfulness","happiness","mindfacts","presentmoment","brainfacts","wellbeing","awareness","psychology101","harvardresearch"],
        "tiktok_caption": "Being present is the REAL key to happiness — Harvard proved it #psychology #mindfulness #happiness",
        "hook": "Harvard found that people are unhappy 47% of the time — here's the single reason why."
    },
    {
        "script": "There's a psychological phenomenon called the Spotlight Effect — the tendency to overestimate how much others notice us. When you trip in public, you think everyone saw and judged you. In reality, most people barely registered it because they're too busy worrying about themselves. Research at Cornell showed people consistently overestimate how much attention others pay to their appearance, mistakes, and behaviors. The audience in your head is almost entirely fictional. Most people are the main character in their own story — and barely an extra in yours. Stop performing for a crowd that isn't watching.",
        "title": "The Spotlight Effect Nobody Is Actually Watching You",
        "description": "The Spotlight Effect is our tendency to overestimate how much others notice us. Cornell research proves we dramatically overestimate our own visibility. Most people are too focused on themselves to notice your mistakes.",
        "hashtags": ["psychology","spotlighteffect","mindfacts","socialpsychology","cognitivebias","selfdevelopment","anxiety","brainfacts","mindpower","psychology101"],
        "tiktok_caption": "Nobody is watching you as much as you think — the Spotlight Effect #psychology #spotlighteffect #mindfacts",
        "hook": "The Spotlight Effect: nobody is watching you nearly as much as you think."
    },
    {
        "script": "Sleep is not just rest — it's a cognitive superpower. During sleep your brain activates the glymphatic system, which clears toxic waste proteins from your neural tissue — including proteins linked to Alzheimer's disease. Your brain also replays memories during sleep, moving them from short-term to long-term storage. Just one night of poor sleep reduces your cognitive performance by 40 percent. Chronic sleep deprivation has been linked to anxiety, depression, weight gain, and impaired immune function. Sleep is not laziness. It's the most productive thing you can do for your brain.",
        "title": "What Your Brain Does While You Sleep Will Surprise You",
        "description": "Sleep activates the glymphatic system that clears brain toxins, consolidates memories, and restores cognitive function. One poor night drops performance by 40%.",
        "hashtags": ["psychology","sleep","brainfacts","mindfacts","neuroscience","brainhealth","sleepscience","mentalhealth","memory","brainpower"],
        "tiktok_caption": "What your brain does while you sleep will shock you #psychology #sleep #brainfacts",
        "hook": "Your brain is doing something incredible while you sleep."
    },
    {
        "script": "Confirmation bias is the brain's tendency to seek out information that confirms what we already believe — and ignore everything that contradicts it. Once you form an opinion, your brain actively filters reality to protect it. This is why two people can watch the same news and walk away with completely opposite conclusions. It's also why people stay in bad relationships, bad jobs, and bad beliefs long after the evidence says to leave. The only antidote is deliberately seeking out opposing viewpoints. The most intelligent thing you can do is actively try to prove yourself wrong.",
        "title": "Why Your Brain Only Sees What It Already Believes",
        "description": "Confirmation bias causes your brain to filter reality to match existing beliefs. Understanding this cognitive bias is essential for better decision-making and healthier relationships.",
        "hashtags": ["psychology","confirmationbias","mindfacts","cognitivebias","brainfacts","criticalthinking","awareness","mindpower","decisionmaking","psychology101"],
        "tiktok_caption": "Your brain only sees what it already believes #psychology #confirmationbias #mindfacts",
        "hook": "Your brain is filtering reality to protect your existing beliefs."
    },
    {
        "script": "Oxytocin, often called the love hormone, is released during hugging, eye contact, and acts of generosity. But here's what most people don't know: oxytocin also increases in-group bias. It makes you more loving toward your group while making you more suspicious toward outsiders. This is the neurochemistry behind tribalism. The same chemical that makes you hug your loved ones also makes you distrust strangers. Understanding this helps explain prejudice and group conflicts — not as moral failures alone, but as biological programming that requires conscious override.",
        "title": "The Love Hormone Oxytocin Has a Dark Side Nobody Talks About",
        "description": "Oxytocin increases love within groups but also amplifies distrust of outsiders. This neurochemical is the biological root of tribalism and in-group bias.",
        "hashtags": ["psychology","oxytocin","mindfacts","neuroscience","brainfacts","tribalism","lovehormone","brainscience","socialpsychology","psychology101"],
        "tiktok_caption": "Oxytocin — the love hormone — has a dark side nobody talks about #psychology #oxytocin #mindfacts",
        "hook": "The love hormone has a dark side that explains tribalism and prejudice."
    },
    {
        "script": "The mere exposure effect is one of the most powerful forces in human attraction. The more you're exposed to something — or someone — the more you tend to like it. This is why songs grow on you after repeated plays. It's why you become attracted to people you see regularly. Advertisers use this to make you like their brand before you even buy it. In relationships, proximity and familiarity breed affection in ways that have nothing to do with objective qualities. You often fall for people simply because you see them often. Your preferences aren't entirely your own — exposure shapes them.",
        "title": "Why You Like Things More the More You Are Exposed to Them",
        "description": "The mere exposure effect shows repeated exposure increases liking for music, people, and products. This explains attraction, brand loyalty, and why familiarity breeds affection.",
        "hashtags": ["psychology","mereexposure","mindfacts","attraction","socialpsychology","brainfacts","cognitivebias","relationships","mindpower","psychology101"],
        "tiktok_caption": "You like things more just from seeing them repeatedly — here's why #psychology #mereexposure #mindfacts",
        "hook": "You become attracted to people simply by seeing them often — here's the science."
    },
    {
        "script": "The human brain is the most energy-hungry organ in the body. It represents only 2 percent of your body weight but consumes 20 percent of your total energy. And it runs almost entirely on glucose. This is why mental work makes you feel physically tired, why you crave sugar after intense focus sessions, and why your willpower fades as the day goes on. What you eat directly affects how your brain performs — within hours. A meal high in refined sugar causes a cognitive crash. Complex carbohydrates and healthy fats provide steady brain fuel. You are literally what you eat — from the neck up.",
        "title": "Your Brain Uses 20 Percent of Your Body Energy Here Is What That Means",
        "description": "The brain consumes 20% of the body's energy. Glucose powers thinking, decision-making, and willpower. Learn how diet directly affects cognitive performance within hours.",
        "hashtags": ["psychology","brainfacts","mindfacts","neuroscience","brainhealth","nutrition","brainpower","mentalperformance","mindpower","cognitivefuel"],
        "tiktok_caption": "Your brain uses 20% of your body's energy — here's what that means #psychology #brainfacts #mindfacts",
        "hook": "Your brain is a 2 percent organ that demands 20 percent of your energy."
    },
    {
        "script": "The Zeigarnik effect explains why unfinished tasks haunt you. Russian psychologist Bluma Zeigarnik noticed that waiters remembered the details of unpaid orders perfectly — but forgot them the moment the bill was settled. Your brain keeps unfinished tasks in an active mental loop, consuming cognitive resources until they're resolved. This is why you can't stop thinking about an argument you didn't resolve, or a project you didn't finish. The solution: write down every open loop in your head. Once your brain knows it's recorded, it releases the mental hold. Getting things out of your head is the first productivity superpower.",
        "title": "Why Unfinished Tasks Haunt Your Mind The Zeigarnik Effect",
        "description": "The Zeigarnik Effect explains why incomplete tasks dominate your thoughts. Writing things down closes those mental loops and frees cognitive resources.",
        "hashtags": ["psychology","zeigarnikeffect","mindfacts","brainfacts","productivity","mentalhealth","brainscience","mindpower","focus","psychology101"],
        "tiktok_caption": "Unfinished tasks live rent-free in your head — here's the psychology #psychology #zeigarnikeffect #mindfacts",
        "hook": "Unfinished tasks haunt your mind until they're done — and here's why."
    },
    {
        "script": "Studies show that exercise is one of the most powerful antidepressants ever studied — and it has zero side effects. A 2018 study in Lancet Psychiatry analyzed 1.2 million people and found those who exercised regularly had 43 percent fewer days of poor mental health. Exercise releases BDNF — brain-derived neurotrophic factor — which acts like fertilizer for neurons, helping them grow and connect. It also floods your brain with serotonin, dopamine, and endorphins. Moving your body is the most evidence-based mental health intervention that exists.",
        "title": "Exercise Is One of the Most Powerful Antidepressants Ever Studied",
        "description": "A study of 1.2 million people found exercisers had 43% fewer poor mental health days. Exercise releases BDNF, serotonin, and dopamine comparable to antidepressant medication.",
        "hashtags": ["psychology","exercise","mentalhealth","mindfacts","brainfacts","depression","neuroscience","mindBody","brainhealth","BDNF"],
        "tiktok_caption": "Exercise is more powerful than antidepressants — science confirms it #psychology #exercise #mentalhealth",
        "hook": "Exercise is one of the most powerful antidepressants ever studied — and it's free."
    },
    {
        "script": "Your brain has a hard limit on how many close relationships it can maintain — and the number is 150. British anthropologist Robin Dunbar discovered this after studying social group sizes in primates. He found humans consistently maintain about 150 stable social relationships — now called Dunbar's Number. Within that, you have concentric circles: 5 intimate friends, 15 close friends, 50 good friends. Beyond 150, the brain simply can't track trust, history, and relationship dynamics. This is why armies, companies, and villages throughout history have clustered around 150 people.",
        "title": "Why Your Brain Can Only Handle 150 Friends Dunbars Number",
        "description": "Robin Dunbar discovered humans can maintain only 150 stable social relationships — a limit set by brain size. This explains why ancient villages, military units, and effective companies all cluster near 150 people.",
        "hashtags": ["psychology","dunbarsnumber","mindfacts","socialpsychology","brainfacts","anthropology","relationships","brainscience","humanconnection","psychology101"],
        "tiktok_caption": "Your brain can only handle 150 friends — it's science #psychology #dunbarsnumber #mindfacts",
        "hook": "Your brain has a hard limit of 150 relationships — and here's why."
    },
    {
        "script": "The Pygmalion effect proves that expectations shape reality. In a landmark study, researchers told teachers that certain students had scored high on an intelligence test and were expected to bloom academically — even though the students were chosen at random. By the end of the year, those students actually performed significantly better. The teachers' higher expectations changed how they interacted with the students — more encouragement, more challenging work, more belief. The students internalized those expectations and rose to meet them. What you expect from people — and from yourself — shapes what actually happens.",
        "title": "The Pygmalion Effect Why Your Expectations Become Reality",
        "description": "The Pygmalion Effect shows that high expectations literally cause higher performance. In a famous study, students performed better simply because teachers expected them to.",
        "hashtags": ["psychology","pygmalioneffect","mindfacts","expectations","socialpsychology","selffulfilling","brainfacts","mindpower","motivation","psychology101"],
        "tiktok_caption": "Your expectations literally shape reality — the Pygmalion Effect #psychology #pygmalioneffect #mindfacts",
        "hook": "Your expectations about people shape what they actually become — here's the science."
    },
    {
        "script": "Fear and excitement are the same physiological state. Same elevated heart rate. Same adrenaline. Same heightened senses. The only difference is the story your brain tells about the sensation. Research at Harvard shows that telling yourself I am excited before a stressful event leads to significantly better performance than trying to calm down. Instead of fighting the feeling, re-label it. The anxiety before a presentation isn't dread — it's your body preparing for peak performance. Reinterpreting your arousal state is called cognitive appraisal — and it's one of the most effective mental performance tools that exists.",
        "title": "Fear and Excitement Are the Same Your Brain Just Picks the Story",
        "description": "Fear and excitement share identical physiological signatures. Harvard research shows relabeling anxiety as excitement improves performance more than trying to calm down.",
        "hashtags": ["psychology","anxietyhacks","mindfacts","fear","excitement","performancepsychology","brainfacts","cognitiveappraisal","mindpower","psychology101"],
        "tiktok_caption": "Fear and excitement are literally the SAME thing #psychology #anxietyhacks #mindfacts",
        "hook": "Fear and excitement are physiologically identical — your brain just picks the story."
    },
    {
        "script": "The Ben Franklin effect is one of the strangest findings in social psychology. When Benjamin Franklin wanted to win over a political rival, he asked to borrow one of the man's rare books. The man who was hostile toward him lent the book — and afterward became a friend. The psychology: doing a favor for someone makes you like them more, not less. Your brain reasons backward: I helped him, so I must like him. Asking people for small favors actually increases their liking of you. It feels counterintuitive, but the act of helping rewires the helper's feelings toward you.",
        "title": "The Ben Franklin Effect Ask for a Favor to Make Someone Like You",
        "description": "The Ben Franklin Effect shows that doing a favor for someone makes you like them more. When people help you, their brain concludes they must like you.",
        "hashtags": ["psychology","benfranklineffect","mindfacts","socialpsychology","relationships","brainfacts","influence","persuasion","mindpower","psychology101"],
        "tiktok_caption": "Ask for a favor to make someone like you more — the Ben Franklin Effect #psychology #benfranklineffect #mindfacts",
        "hook": "Asking for a favor makes people like you more — not less."
    },
    {
        "script": "Studies show that gratitude physically alters the brain. When you regularly practice gratitude, it increases activity in the hypothalamus — which controls stress — and releases dopamine and serotonin. Research from UC Berkeley found that people who wrote gratitude letters showed significantly better mental health for weeks afterward, even if they never sent the letters. Writing gratitude activates neural pathways associated with positive emotion. After 21 days of daily gratitude practice, your brain starts scanning for positives by default. Gratitude isn't just a nice sentiment — it's a neurological rewiring tool.",
        "title": "How Gratitude Physically Changes Your Brain in 21 Days",
        "description": "Gratitude practice triggers dopamine and serotonin release and reduces stress hormones. UC Berkeley research showed gratitude writing improved mental health for weeks. Twenty-one days rewires your brain to default to positivity.",
        "hashtags": ["psychology","gratitude","mindfacts","brainfacts","mentalhealth","neuroscience","happiness","brainscience","mindpower","positivepsychology"],
        "tiktok_caption": "Gratitude physically changes your brain in 21 days #psychology #gratitude #mindfacts",
        "hook": "Gratitude physically rewires your brain — and it takes only 21 days."
    },
    {
        "script": "The sunk cost fallacy is why people stay in bad relationships, bad movies, and bad investments long after they should have left. It's the irrational tendency to continue something because of resources you've already spent — time, money, or emotion — even when continuing will only cost you more. Five years in this relationship is not a reason to continue a toxic one. Your brain mistakes past investment for future value. The rational truth: past costs are gone regardless of your choice. The only question is what's the best path forward from here. Let sunk costs sink.",
        "title": "The Sunk Cost Fallacy Why You Stay in Bad Situations Too Long",
        "description": "The sunk cost fallacy causes people to continue bad decisions because of past investments. Understanding this cognitive bias is essential for making clearer decisions in relationships, careers, and finances.",
        "hashtags": ["psychology","sunkcostfallacy","mindfacts","cognitivebias","brainfacts","decisionmaking","relationships","criticalthinking","mindpower","psychology101"],
        "tiktok_caption": "Why you stay in bad situations too long — the sunk cost fallacy #psychology #sunkcostfallacy #mindfacts",
        "hook": "The Sunk Cost Fallacy explains why people stay in bad situations way too long."
    },
    {
        "script": "There's a science to first impressions — and most of the judgment happens in 0.1 seconds. Research by Princeton psychologists found that people form assessments of trustworthiness and attractiveness from a glance lasting a tenth of a second. And more time looking doesn't dramatically change those initial judgments. The first 7 seconds of a meeting are 55 percent body language, 38 percent tone of voice, and only 7 percent the actual words. Your brain makes social snap judgments as a survival mechanism. Understanding this lets you be more intentional — and more forgiving.",
        "title": "First Impressions Form in 0.1 Seconds and They Stick",
        "description": "Princeton research shows character judgments form in 0.1 seconds and barely change with more time. First impressions are mostly body language and tone, not words.",
        "hashtags": ["psychology","firstimpressions","mindfacts","socialpsychology","brainfacts","bodylanguage","communication","mindpower","perception","psychology101"],
        "tiktok_caption": "First impressions form in 0.1 seconds and they're almost impossible to change #psychology #firstimpressions #mindfacts",
        "hook": "First impressions form in 0.1 seconds — and they almost never change."
    },
    {
        "script": "Dopamine is not the pleasure chemical — it's the anticipation chemical. Your brain releases dopamine in the lead-up to a reward, not during it. This is why the pursuit of something often feels better than getting it. The chase releases dopamine. Achievement releases less. This is the neurological engine behind addiction, gambling, and endless social media scrolling — the next post might be the one. Understanding that you're chasing dopamine, not actual satisfaction, is the first step to breaking compulsive patterns. Create goals with milestones. Each milestone triggers a dopamine hit to keep you moving.",
        "title": "Dopamine Is Not the Pleasure Chemical Here Is What It Really Does",
        "description": "Dopamine is the anticipation chemical, not pleasure itself. Your brain releases it during the chase, not the achievement. This explains addiction, gambling, and social media compulsion.",
        "hashtags": ["psychology","dopamine","mindfacts","brainfacts","neuroscience","addiction","motivation","brainscience","mindpower","psychology101"],
        "tiktok_caption": "Dopamine isn't what you think — this will change how you see motivation #psychology #dopamine #mindfacts",
        "hook": "Dopamine isn't about pleasure — it's about the chase. And this changes everything."
    },
    {
        "script": "Imposter syndrome affects an estimated 70 percent of people at some point in their lives — including Nobel Prize winners, CEOs, and world-renowned artists. It's the persistent feeling that you're a fraud who will be found out, despite clear evidence of success. Here's what's fascinating: experiencing imposter syndrome is actually associated with higher competence. Less competent people rarely feel like frauds. If you feel like an imposter, it might mean you're more capable than you think.",
        "title": "70 Percent of People Feel Like Frauds Including CEOs and Nobel Winners",
        "description": "Imposter syndrome affects 70% of people including elite achievers. Feeling like a fraud is associated with higher competence — less skilled people rarely question themselves.",
        "hashtags": ["psychology","impostersyndrome","mindfacts","mentalhealth","selfdevelopment","brainfacts","confidence","mindpower","selfworth","psychology101"],
        "tiktok_caption": "70% of people feel like frauds — even CEOs and Nobel winners #psychology #impostersyndrome #mindfacts",
        "hook": "70 percent of people feel like frauds — including the most successful people alive."
    },
    {
        "script": "Your memory is not a recording — it's a reconstruction. Every time you remember something, you partially rewrite it. Research shows that memories are rebuilt from fragments each time you recall them, and they're influenced by your current mood, beliefs, and the questions you're asked. This is why two siblings remember the same childhood differently. It's why eyewitness testimony is unreliable. And it's why you remember past relationships as better than they were when you're lonely, or worse when you're angry. Your memories are stories your brain tells you — revised at every telling.",
        "title": "Your Memory Is Not a Recording Your Brain Rewrites It Every Time",
        "description": "Memory is reconstructive, not reproductive. Every time you recall something, your brain partially rewrites it influenced by current mood. This explains false memories and why the past isn't what you think.",
        "hashtags": ["psychology","memory","mindfacts","brainfacts","neuroscience","falsememory","brainscience","cognitivescience","mindpower","psychology101"],
        "tiktok_caption": "Your memories are being rewritten every time you remember them #psychology #memory #mindfacts",
        "hook": "Your brain rewrites your memories every single time you recall them."
    },
    {
        "script": "Chronic stress shrinks your brain. Research shows that prolonged elevated cortisol — the stress hormone — actually causes the hippocampus, your memory and learning center, to physically shrink. It also weakens the prefrontal cortex, the seat of rational decision-making, and strengthens the amygdala — your fear response center. This explains why people under chronic stress struggle to learn, make good decisions, and feel emotionally reactive. But the damage is largely reversible. Sleep, exercise, mindfulness, and social connection restore the hippocampus. Managing stress isn't optional — it's brain maintenance.",
        "title": "Chronic Stress Literally Shrinks Your Brain Here Is the Science",
        "description": "Prolonged stress elevates cortisol, which physically shrinks the hippocampus and weakens rational decision-making. The damage is largely reversible with sleep, exercise, and mindfulness.",
        "hashtags": ["psychology","stress","brainfacts","mindfacts","cortisol","mentalhealth","neuroscience","brainhealth","mindpower","stressmanagement"],
        "tiktok_caption": "Chronic stress literally shrinks your brain — here's the science #psychology #stress #brainfacts",
        "hook": "Chronic stress is physically shrinking your brain right now."
    },
    {
        "script": "There's a reason you can remember lyrics to a song you haven't heard in 20 years but forget where you put your keys. Music is processed in multiple brain regions simultaneously — emotional, linguistic, motor, and memory centers all light up together. This multi-region encoding creates much stronger memory traces than ordinary experiences. Advertisers know this — hence jingles. Teachers are discovering it too — lessons set to music are remembered significantly better. If you want to memorize anything, set it to a rhythm or song. Your ancient brain evolved with music long before language.",
        "title": "Why You Remember Song Lyrics but Forget Where You Left Your Keys",
        "description": "Music activates emotional, linguistic, motor, and memory brain regions simultaneously, creating stronger memory traces than ordinary experience.",
        "hashtags": ["psychology","musicandmemory","mindfacts","brainfacts","neuroscience","memory","brainscience","musicpsychology","mindpower","learning"],
        "tiktok_caption": "Why you remember song lyrics but forget your keys #psychology #musicandmemory #mindfacts",
        "hook": "You remember lyrics from 20 years ago but forgot where your keys are — here's the psychology."
    },
    {
        "script": "The Hawthorne Effect explains why people behave differently when they know they're being observed. Factory workers in the 1920s became dramatically more productive when researchers simply started measuring their output — regardless of any other changes. Just being watched improved performance. This is why fitness trackers increase exercise, why journaling improves self-awareness, and why having an accountability partner boosts success rates dramatically. Observation changes behavior. If you want to improve any habit, start tracking it. The act of measurement itself is a performance enhancer.",
        "title": "Why Being Observed Makes You Perform Better The Hawthorne Effect",
        "description": "The Hawthorne Effect shows people improve performance simply when they know they're being measured. This explains why fitness trackers, journaling, and accountability partners work.",
        "hashtags": ["psychology","hawthorneeffect","mindfacts","behavioralpsychology","brainfacts","accountability","habits","productivity","mindpower","psychology101"],
        "tiktok_caption": "Being observed literally makes you perform better #psychology #hawthorneeffect #mindfacts",
        "hook": "Being watched makes you perform better — and here's the science behind why."
    },
    {
        "script": "Your emotional state right now affects what memories you recall. This is called mood-congruent memory, and it creates a feedback loop that can trap you. When you're sad, your brain preferentially recalls sad memories, which makes you sadder, which recalls more sad memories. When you're happy, you remember happy times more easily. This is why forcing yourself to move your body can actually change your emotional trajectory — you shift the memory access pattern. To break a negative thought spiral, change your physical state first — walk, dance, exercise — then your memories will follow.",
        "title": "Why Your Mood Determines What Memories You Can Access",
        "description": "Mood-congruent memory means your emotional state filters which memories you recall, creating reinforcing loops. Changing your physical state breaks this cycle.",
        "hashtags": ["psychology","moodmemory","mindfacts","brainfacts","emotion","mentalhealth","brainscience","mindpower","emotionalintelligence","psychology101"],
        "tiktok_caption": "Your mood controls which memories your brain can access #psychology #moodmemory #mindfacts",
        "hook": "Your current mood is controlling which memories your brain can access."
    },
    {
        "script": "There's a psychological concept called learned helplessness — and it might be quietly running your life. Psychologist Martin Seligman discovered it by studying dogs who received random shocks. After a while, even when given a chance to escape, the dogs would lie down and accept the pain. They had learned that their actions had no effect. Humans develop the same pattern. After enough failure, rejection, or trauma, the brain concludes: nothing I do matters. This blocks action even when options exist. The antidote is small wins — intentional actions followed by real results — that rebuild the belief that you have agency.",
        "title": "Learned Helplessness Why People Stop Trying Even When They Can Succeed",
        "description": "Learned helplessness occurs when repeated failures train the brain to stop trying, even when success is possible. Small intentional wins rebuild the neural belief in personal agency.",
        "hashtags": ["psychology","learnedhelplessness","mindfacts","brainfacts","mentalhealth","motivation","resilience","mindpower","martinSeligman","psychology101"],
        "tiktok_caption": "Learned helplessness is silently stopping you from trying #psychology #learnedhelplessness #mindfacts",
        "hook": "Learned helplessness might be why you've stopped trying — even when you could succeed."
    },
    {
        "script": "The recency bias makes your brain give disproportionate weight to recent events. A great employee who has a bad month seems worse than a mediocre employee who had a good month. Your last experience at a restaurant matters more than your previous ten. Your most recent argument with a partner colors how you see the whole relationship. Investors sell after crashes because recent losses feel permanent. This bias evolved for survival — recent information is often most relevant. But in modern contexts, it distorts judgment. When evaluating anything important, deliberately consider the full history, not just what just happened.",
        "title": "Recency Bias Why Your Brain Overweights What Just Happened",
        "description": "Recency bias causes your brain to give disproportionate weight to recent events, distorting judgment in relationships, performance evaluation, and investing.",
        "hashtags": ["psychology","recencybias","mindfacts","cognitivebias","brainfacts","decisionmaking","criticalthinking","mindpower","awareness","psychology101"],
        "tiktok_caption": "Your brain overweights recent events — and it's distorting your reality #psychology #recencybias #mindfacts",
        "hook": "Recency bias is causing you to judge people and situations unfairly — here's how."
    },
    {
        "script": "Flow state is arguably the peak human experience. Described by psychologist Mihaly Csikszentmihalyi after studying thousands of artists, athletes, and musicians, flow is the mental state where you're fully absorbed, time disappears, and performance peaks. Your brain in flow shows reduced activity in the prefrontal cortex — the inner critic quiets. EEG studies show flow produces theta brain waves associated with deep meditation. To enter flow: eliminate distractions, match task difficulty slightly above your skill level, and work in blocks of 90 minutes. Flow is not luck — it's architecture.",
        "title": "The Science of Flow State Why Time Disappears When You Are at Your Best",
        "description": "Flow state is a peak performance mental state where the inner critic quiets and output soars. Csikszentmihalyi's decades of research reveal conditions for flow — and how to engineer it deliberately.",
        "hashtags": ["psychology","flowstate","mindfacts","brainfacts","peakperformance","neuroscience","productivity","mindpower","brainscience","csikszentmihalyi"],
        "tiktok_caption": "Flow state is the peak human experience — here's how to get there #psychology #flowstate #mindfacts",
        "hook": "Flow state is the peak of human experience — and you can engineer it deliberately."
    },
    {
        "script": "Laughter is one of the most powerful and underused cognitive tools we have. When you laugh, your brain releases endorphins, dopamine, and oxytocin simultaneously — a chemical trifecta. Studies show laughter reduces cortisol and adrenaline, lowering stress response within seconds. It also boosts immune function, reduces pain perception, and increases creativity by relaxing prefrontal cortex constraints. Research found that people laugh 30 times more in social settings than when alone — confirming laughter's deep social function. The phrase laughter is the best medicine is actually neuroscience. Laugh more. It's maintenance.",
        "title": "Laughter Releases 3 Feel Good Chemicals at Once It Is Brain Medicine",
        "description": "Laughter triggers simultaneous release of endorphins, dopamine, and oxytocin while reducing cortisol. Research shows it boosts immunity, reduces pain, and increases creativity.",
        "hashtags": ["psychology","laughter","mindfacts","brainfacts","endorphins","mentalhealth","neuroscience","happiness","brainscience","wellbeing"],
        "tiktok_caption": "Laughter releases 3 feel-good chemicals at once — it's literally brain medicine #psychology #laughter #mindfacts",
        "hook": "Laughter releases three feel-good chemicals simultaneously — it's one of the best things for your brain."
    },
    {
        "script": "The social comparison trap is wired into your biology. Humans have evolved to constantly gauge status relative to others — because in ancestral environments, relative status determined access to food, mates, and safety. Today, social media has weaponized this instinct. Every scroll is a highlight reel comparison that triggers the same neural threat response as falling behind in the tribe. Studies show Instagram use is directly correlated with increased depression and lower self-esteem. Knowing the mechanism doesn't make you immune, but it gives you a chance to override it. Your worth is not a comparison.",
        "title": "Why Social Media Makes You Feel Bad The Social Comparison Trap",
        "description": "Social comparison is an ancient survival instinct weaponized by social media. Research directly links Instagram use to depression and lower self-esteem. Understanding the evolutionary mechanism helps you consciously override it.",
        "hashtags": ["psychology","socialcomparison","mindfacts","socialmedia","mentalhealth","brainfacts","selfworth","mindpower","awareness","psychology101"],
        "tiktok_caption": "Social media is exploiting your ancient comparison instinct #psychology #socialcomparison #mindfacts",
        "hook": "Social media is exploiting an ancient brain circuit to make you feel inferior."
    },
    {
        "script": "The body keeps the score — that's the title of one of the most important psychology books ever written. Bessel van der Kolk's decades of research show that trauma is not just stored in your memories — it's stored in your body. Unprocessed trauma lives in muscle tension, altered breathing patterns, gut responses, and hypervigilance. The body literally holds the experience. This is why traditional talk therapy alone sometimes doesn't resolve trauma — the body needs to be part of healing through movement, breathwork, somatic therapy, or even yoga. Healing is not just mental. It is physical.",
        "title": "Trauma Is Stored in Your Body Not Just Your Mind",
        "description": "Bessel van der Kolk's research shows trauma is stored in the body as physical tension and altered responses — not just in memories. Healing must address the body.",
        "hashtags": ["psychology","trauma","mindfacts","bodykeepsthescore","mentalhealth","somatictherapy","brainfacts","healing","mindbody","psychology101"],
        "tiktok_caption": "Trauma is stored in your BODY — not just your mind #psychology #trauma #mindfacts",
        "hook": "Trauma isn't just in your memories — it's physically stored in your body."
    },
    {
        "script": "Sleep deprivation does something terrifying to your emotional regulation. Research shows that after just one night of poor sleep, the amygdala — your brain's threat detector — becomes 60 percent more reactive. The connection between the amygdala and prefrontal cortex weakens, meaning your rational brain can't calm down your emotional brain. This explains road rage, disproportionate anger, crying over small things, and catastrophic thinking after a bad night. You're not more emotional — you're less regulated. Before attributing an emotional reaction to a personality flaw, ask yourself: when did I last sleep well?",
        "title": "One Bad Night of Sleep Makes Your Brain 60 Percent More Emotional",
        "description": "Sleep deprivation causes the amygdala to become 60% more reactive while weakening rational control from the prefrontal cortex. Many emotional problems are actually sleep problems in disguise.",
        "hashtags": ["psychology","sleep","emotionalregulation","mindfacts","brainfacts","amygdala","mentalhealth","neuroscience","sleepscience","mindpower"],
        "tiktok_caption": "One bad sleep makes your brain 60% more emotional — not a personality flaw #psychology #sleep #mindfacts",
        "hook": "One bad night of sleep makes your brain 60 percent more emotionally reactive."
    },
    {
        "script": "The peak-end rule reveals something profound about how memory works. Psychologist Daniel Kahneman discovered that people judge an experience almost entirely by two things: the peak emotional moment and the final moment — not the overall average. In a study, patients undergoing a painful procedure who had a less painful ending rated the entire procedure as less bad — even though it lasted longer. This is why how you end conversations, relationships, and experiences matters enormously. People remember peaks and endings. Make yours memorable. The last impression becomes the lasting impression.",
        "title": "Why How Things End Matters More Than How They Go The Peak End Rule",
        "description": "Daniel Kahneman's Peak-End Rule shows people judge experiences by their emotional peak and final moment — not the average. Endings carry disproportionate weight in memory.",
        "hashtags": ["psychology","peakendrule","mindfacts","kahneman","brainfacts","memory","relationships","mindpower","behavioraleconomics","psychology101"],
        "tiktok_caption": "How things end matters MORE than how they go — the Peak-End Rule #psychology #peakendrule #mindfacts",
        "hook": "People judge your relationship not by the whole — but by the peak and the end."
    },
    {
        "script": "Your brain is essentially an energy-saving machine, and it achieves this through automaticity — turning repeated behaviors into automatic habits to conserve cognitive resources. This is why driving a familiar route requires almost no conscious attention. Habits live in the basal ganglia, separate from the conscious decision-making prefrontal cortex. Once formed, habits never fully disappear — they're just overwritten by new ones. This is the basis of habit loops: cue, routine, reward. Every habit you have was once a conscious choice repeated until it went automatic. You can use this deliberately to design the person you want to become.",
        "title": "How Your Brain Converts Choices Into Automatic Habits",
        "description": "The brain converts repeated behaviors into automatic habits stored in the basal ganglia, freeing cognitive resources. Understanding the habit loop lets you deliberately design new automatic behaviors.",
        "hashtags": ["psychology","habits","mindfacts","brainfacts","automaticity","habitloop","neuroscience","basalganglia","mindpower","psychology101"],
        "tiktok_caption": "Your brain turns repeated choices into automatic habits — here's how to use that #psychology #habits #mindfacts",
        "hook": "Every habit you have was once a conscious choice — until your brain made it automatic."
    },
    {
        "script": "Nature deprivation is a real and growing mental health crisis. Research from Stanford shows that a 90-minute walk in a natural setting significantly reduces activity in the brain region associated with rumination and negative self-focused thought. Urban dwellers who rarely access nature show higher rates of depression and anxiety than rural populations. Even 20 minutes in a green space reduces cortisol levels measurably. Our brains evolved over millions of years in natural environments — modern urban living is a mismatch. Going outside isn't escaping — it's returning to where your brain thrives.",
        "title": "Nature Deprivation Is a Real Mental Health Crisis Go Outside",
        "description": "Stanford research shows nature walks reduce brain activity linked to depression and rumination. Twenty minutes in green space lowers cortisol. Urban environments create a fundamental mismatch with the brain's evolutionary habitat.",
        "hashtags": ["psychology","nature","mentalhealth","mindfacts","brainfacts","neuroscience","outdoors","stressrelief","mindpower","biophilia"],
        "tiktok_caption": "You need nature for your brain — science proves it #psychology #nature #mentalhealth",
        "hook": "Your brain evolved in nature — and being deprived of it is making you mentally ill."
    },
    {
        "script": "The actor-observer bias is why relationships are so difficult. When you do something wrong, you explain it by circumstances: I was stressed, I was tired, I had a bad day. When someone else does the same thing, you explain it by their character: they're selfish, they don't care, that's just who they are. You're the actor seeing your circumstances. You're the observer judging their character. This asymmetry causes resentment and broken relationships. The fix: apply the same charitable interpretation to others as you do to yourself. Extend the grace you give yourself.",
        "title": "Why You Forgive Yourself but Judge Others The Actor Observer Bias",
        "description": "The actor-observer bias causes people to attribute their own bad behavior to circumstances while attributing others' bad behavior to character. This asymmetry is a major source of relationship conflict.",
        "hashtags": ["psychology","actorobserver","mindfacts","socialpsychology","relationships","brainfacts","cognitivebias","empathy","mindpower","psychology101"],
        "tiktok_caption": "Why you forgive yourself but judge others — the actor-observer bias #psychology #actorobserver #mindfacts",
        "hook": "You forgive yourself for circumstances but judge others for their character — here's the bias."
    },
    {
        "script": "Vulnerability is not weakness — it's the birthplace of creativity, belonging, and love. Researcher Brene Brown spent a decade studying human connection and found that the people with the strongest sense of belonging had one thing in common: they had the courage to be vulnerable. They were willing to say I don't know, I was wrong, I love you first. The armor people use to protect themselves from vulnerability also blocks connection, creativity, and joy. The walls that keep pain out also keep love out. Courage is not the absence of fear — it's showing up fully when the outcome is uncertain.",
        "title": "Vulnerability Is Not Weakness It Is the Source of Human Connection",
        "description": "Brene Brown's decade of research found that people with the strongest sense of belonging shared one trait: courage to be vulnerable. Emotional armor blocks both pain and connection.",
        "hashtags": ["psychology","vulnerability","mindfacts","brenebrown","connection","mentalhealth","empathy","courage","wellbeing","psychology101"],
        "tiktok_caption": "Vulnerability is not weakness — it's where connection is born #psychology #vulnerability #mindfacts",
        "hook": "Vulnerability is not weakness — it's the only path to genuine human connection."
    },
    {
        "script": "The availability heuristic makes people think events are more common than they are, based on how easily examples come to mind. Plane crashes feel more dangerous than car accidents because they're dramatic and widely covered. Shark attacks feel more common than lightning strikes because sharks are scarier in our imagination. Your risk assessment is calibrated by media coverage and emotional salience, not actual statistics. This bias distorts everything from fear to policy decisions. Before concluding something is common or rare, check the data. Your instincts are measuring memorability, not probability.",
        "title": "Why You Fear the Wrong Things The Availability Heuristic",
        "description": "The availability heuristic makes dramatic memorable events seem more probable than they are. Media coverage and emotional salience distort our risk assessment.",
        "hashtags": ["psychology","availabilityheuristic","mindfacts","cognitivebias","brainfacts","fear","risk","criticalthinking","mindpower","psychology101"],
        "tiktok_caption": "Your brain is terrible at measuring real risk — the availability heuristic #psychology #availabilityheuristic #mindfacts",
        "hook": "Your brain measures risk by how scary something sounds, not how likely it actually is."
    },
    {
        "script": "Breathing is the only autonomic function you can consciously control — and that makes it a direct gateway to your nervous system. When you're stressed, your sympathetic nervous system activates. But slow, deep breathing — particularly exhale-longer-than-inhale patterns — directly activates the parasympathetic system, your rest and digest response. Box breathing: 4 counts in, 4 hold, 4 out, 4 hold. Used by Navy SEALs to perform under fire. The 4-7-8 breathing pattern can induce calm in 60 seconds. You have a biological override switch for stress built into every breath.",
        "title": "Breathing Is Your Biological Override Switch for Stress",
        "description": "Breathing is the only autonomic function under conscious control, making it a direct gateway to the nervous system. Slow exhalation activates parasympathetic response. Box breathing reduces stress in under 60 seconds.",
        "hashtags": ["psychology","breathing","mindfacts","stressrelief","nervoussystem","breathwork","neuroscience","mentalhealth","mindpower","anxiety"],
        "tiktok_caption": "Breathing is your biological override switch for stress #psychology #breathing #mindfacts",
        "hook": "You have a biological override switch for stress — and it's in every single breath."
    },
    {
        "script": "The science of procrastination reveals it's not a time management problem — it's an emotion management problem. Research shows people procrastinate not because they're lazy, but because the task triggers negative emotions — anxiety, self-doubt, boredom, or resentment. Avoidance temporarily relieves those emotions, which reinforces procrastination as a coping strategy. The fix is not discipline — it's identifying and reducing the emotional charge around the task. Break it into a 2-minute start. Change the environment. Pair it with something pleasant. Make starting feel safe, and the doing will follow.",
        "title": "Procrastination Is an Emotion Problem Not a Time Problem",
        "description": "Research shows procrastination is emotional avoidance of tasks that trigger anxiety or self-doubt, not laziness or poor time management. Reducing the emotional charge around starting is the only reliable fix.",
        "hashtags": ["psychology","procrastination","mindfacts","emotionalregulation","brainfacts","productivity","mentalhealth","mindpower","habits","psychology101"],
        "tiktok_caption": "Procrastination is an emotion problem — not laziness #psychology #procrastination #mindfacts",
        "hook": "Procrastination has nothing to do with time management — it's emotional avoidance."
    },
    {
        "script": "Your sense of smell is the only sense with a direct neural pathway to the amygdala and hippocampus — your emotion and memory centers. This is why a smell can instantly transport you to a specific memory with all its emotional intensity intact. Scent bypasses the thalamus, which filters all other senses. This is why aromatherapy has real neurological effects — lavender genuinely reduces cortisol. The scent of a loved one lowers stress hormones. Your nose is the most direct route to your emotional brain. The memories tied to smell are among the most vivid and emotionally powerful you have.",
        "title": "Why Smell Instantly Triggers Memories The Neuroscience of Scent",
        "description": "Smell has a direct neural pathway to the amygdala and hippocampus, bypassing the thalamus that filters other senses. This explains why scents trigger vivid emotional memories instantly.",
        "hashtags": ["psychology","smell","memory","mindfacts","brainfacts","neuroscience","senses","brainscience","mindpower","emotion"],
        "tiktok_caption": "Smell bypasses every filter to hit your emotional brain directly #psychology #smell #mindfacts",
        "hook": "Smell is the only sense with a direct line to your emotional brain — here's why."
    },
    {
        "script": "Anger is a secondary emotion — it almost always masks a primary emotion underneath. When someone feels hurt, they often express anger. When someone feels scared, they often show rage. When someone feels ashamed, they often become hostile. Anger feels more powerful than hurt or fear, which is why the brain uses it as a shield. But because the anger addresses none of the underlying emotions, it never resolves anything. The next time you feel angry, pause and ask: what emotion am I actually protecting? The answer almost always leads to the real conversation — and real resolution.",
        "title": "Anger Is Almost Always Masking a Deeper Emotion Here Is What",
        "description": "Anger is typically a secondary emotion masking hurt, fear, or shame. Because anger feels more powerful, the brain deploys it as emotional armor. True resolution requires identifying the primary emotion underneath.",
        "hashtags": ["psychology","anger","emotionalintelligence","mindfacts","brainfacts","mentalhealth","emotions","relationships","mindpower","psychology101"],
        "tiktok_caption": "Anger is almost never the real emotion — here's what's actually underneath #psychology #anger #mindfacts",
        "hook": "Anger is almost always masking a deeper emotion — and here's how to find it."
    },
    {
        "script": "The bystander effect explains why people fail to help in emergencies when others are present. When Kitty Genovese was attacked outside her New York apartment, dozens of witnesses reportedly watched and did nothing. The psychology: in a group, individuals feel less personal responsibility — someone else will help. And social proof makes inaction seem acceptable because no one else is acting. To overcome the bystander effect, make it personal: make direct eye contact with one specific person and say: you, please call 911. Specificity breaks diffusion of responsibility.",
        "title": "The Bystander Effect Why People Do Nothing in Emergencies",
        "description": "The bystander effect causes individuals to feel less personal responsibility in groups, leading to inaction in emergencies. Understanding this phenomenon — and how to override it — can save lives.",
        "hashtags": ["psychology","bystandereffect","mindfacts","socialpsychology","brainfacts","emergencies","diffusionofresponsibility","mindpower","socialbehavior","psychology101"],
        "tiktok_caption": "Why people do nothing in emergencies — the bystander effect #psychology #bystandereffect #mindfacts",
        "hook": "The Bystander Effect explains why crowds watch emergencies unfold — and no one helps."
    },
    {
        "script": "Your brain literally cannot multitask. What you experience as multitasking is actually rapid task-switching — and it comes at a significant cognitive cost. Every time you switch tasks, your brain needs time to reload the context of the new task. This switching cost reduces productivity by up to 40 percent. It also increases error rates and mental fatigue. The people who think they're best at multitasking are, according to Stanford research, actually the worst at it — they're more distracted, less able to filter irrelevance, and worse at switching. Single-task. Sequentially. Deeply.",
        "title": "Your Brain Cannot Multitask Here Is What Is Actually Happening",
        "description": "Multitasking is a myth — your brain rapidly switches tasks, costing up to 40% productivity and increasing errors. Stanford found self-described multitaskers are actually the worst at it.",
        "hashtags": ["psychology","multitasking","mindfacts","productivity","brainfacts","focus","neuroscience","attentionpsychology","mindpower","psychology101"],
        "tiktok_caption": "Your brain literally cannot multitask — here's what's really happening #psychology #multitasking #mindfacts",
        "hook": "Multitasking is a myth — and believing in it is costing you 40 percent of your productivity."
    },
    {
        "script": "Physical touch is not a luxury — it's a biological necessity. Research shows that premature babies who are held and touched regularly gain weight 47 percent faster than those in standard care. Touch triggers oxytocin release, lowers blood pressure, and reduces cortisol. Studies from UC Berkeley show that NBA teams with more physical contact — high-fives, chest bumps, team huddles — perform significantly better over the season. Touch communicates trust, cooperation, and safety faster than words. In an increasingly touchless world, the deprivation of physical contact has measurable mental and physical health consequences.",
        "title": "Physical Touch Is a Biological Necessity Not a Luxury",
        "description": "Touch triggers oxytocin, reduces cortisol, and is essential for development and health. Research shows premature babies who are touched regularly grow 47% faster. Touch deprivation has measurable health consequences.",
        "hashtags": ["psychology","touch","mindfacts","oxytocin","brainfacts","mentalhealth","neuroscience","connection","wellbeing","psychology101"],
        "tiktok_caption": "Physical touch is a biological need — not a luxury #psychology #touch #mindfacts",
        "hook": "Physical touch is as essential as food and water — and science proves it."
    },
    {
        "script": "Growth mindset versus fixed mindset — the research by Carol Dweck at Stanford is some of the most important in modern psychology. People with a fixed mindset believe intelligence and talent are innate and unchangeable. When they fail, it threatens their identity. So they avoid challenges. People with a growth mindset believe abilities develop through effort and learning. Failure is data. Criticism is useful. Challenges are interesting. The remarkable finding: teaching children that the brain grows through effort changed their academic trajectories within weeks. The belief about the nature of ability determines whether you use it.",
        "title": "Growth Mindset vs Fixed Mindset The Stanford Research That Changes Everything",
        "description": "Carol Dweck's Stanford research shows that beliefs about intelligence shape behavior, resilience, and achievement. Teaching that the brain grows through effort changes academic outcomes within weeks.",
        "hashtags": ["psychology","growthmindset","fixedmindset","mindfacts","carolDweck","brainfacts","education","selfdevelopment","mindpower","psychology101"],
        "tiktok_caption": "Growth mindset vs fixed mindset — the Stanford research that changes everything #psychology #growthmindset #mindfacts",
        "hook": "Your belief about whether you can grow determines whether you actually grow."
    },
    {
        "script": "Studies show that people who have a strong sense of purpose live longer, get sick less often, and recover from illness faster. Research published in Psychological Science tracked 6,000 people and found that having purpose reduced all-cause mortality by 15 percent — regardless of age, income, or health status. The Japanese concept of Ikigai — your reason for being — has been linked to exceptional longevity in Okinawa, which has one of the highest concentrations of centenarians in the world. Purpose is not something you find — it's something you build through contribution, craft, and connection. It's also medicine.",
        "title": "Having a Strong Sense of Purpose Makes You Live Longer Science Confirms",
        "description": "Research shows purpose reduces all-cause mortality by 15%. The Japanese concept of Ikigai has been linked to exceptional longevity. Purpose improves immune function and extends lifespan.",
        "hashtags": ["psychology","purpose","ikigai","mindfacts","brainfacts","longevity","mentalhealth","wellbeing","mindpower","psychology101"],
        "tiktok_caption": "Having purpose makes you live longer — science confirms it #psychology #purpose #ikigai",
        "hook": "People with a strong sense of purpose live longer — and here's the science."
    },
    {
        "script": "The psychological immune system is one of the most fascinating features of the human mind. Research by Daniel Gilbert at Harvard shows that humans are remarkably poor predictors of how long negative events will affect them. People consistently overestimate how bad losing a job, a relationship, or even a limb will feel one year later. The psychological immune system — a combination of rationalization, perspective-shifting, and meaning-making — automatically activates to help you adapt. You are more resilient than you think. The worst-case scenarios you fear will hurt less and heal faster than your predictions.",
        "title": "You Are More Resilient Than You Think The Psychological Immune System",
        "description": "Harvard's Daniel Gilbert found people consistently overestimate how long and how badly negative events will affect them. The psychological immune system automatically activates resilience through rationalization and meaning-making.",
        "hashtags": ["psychology","resilience","mindfacts","danielgilbert","brainfacts","mentalhealth","adaptation","wellbeing","mindpower","psychology101"],
        "tiktok_caption": "You're far more resilient than you think — the psychological immune system #psychology #resilience #mindfacts",
        "hook": "You are far more resilient than you believe — and Harvard science proves it."
    },
    {
        "script": "The self-serving bias is one of the most pervasive in human psychology. When good things happen, we attribute them to our own skill and effort. When bad things happen, we blame external circumstances. You got the job because you're talented. You didn't get it because the interviewer was biased. This bias protects self-esteem — which is useful. But it also blocks learning from failure and damages relationships, because others around you don't see things the same way. After a failure, ask: what role did I play? After a success, ask: what helped me that I didn't control? Humility and growth live in the gap.",
        "title": "The Self Serving Bias Why You Take Credit but Avoid Blame",
        "description": "The self-serving bias causes people to attribute successes to themselves and failures to external factors. While it protects self-esteem, it blocks learning and damages relationships.",
        "hashtags": ["psychology","selfservingbias","mindfacts","cognitivebias","brainfacts","selfawareness","accountability","mindpower","criticalthinking","psychology101"],
        "tiktok_caption": "You take credit for wins and blame others for losses — everyone does this #psychology #selfservingbias #mindfacts",
        "hook": "You take credit for your successes and blame circumstances for failures — without realizing it."
    },
    {
        "script": "Humans are the only animals that can feel embarrassed — and it's because of a brain region called the medial prefrontal cortex, which is responsible for self-awareness and imagining how others see you. This same region is overactive in people with social anxiety. But here's the fascinating part: people with damage to this brain area literally cannot feel embarrassed, and they also lose the ability to empathize. Embarrassment and empathy share the same neural machinery. Being able to feel embarrassed means your brain is working as designed for social connection.",
        "title": "Why Humans Are the Only Animals That Feel Embarrassed",
        "description": "Embarrassment requires a brain region that enables self-awareness and social imagination. The same neural circuitry underlies empathy. Understanding the neuroscience of embarrassment reveals how deeply social our brains are.",
        "hashtags": ["psychology","embarrassment","mindfacts","brainfacts","socialpsychology","neuroscience","brainscience","empathy","psychology101","mindpower"],
        "tiktok_caption": "Humans are the only animals that feel embarrassed — here's why #psychology #mindfacts #brainfacts",
        "hook": "Humans are the only animals capable of feeling embarrassed — here's the neuroscience."
    },
    {
        "script": "Your brain's reticular activating system — or RAS — is the filter system that determines what your consciousness pays attention to out of the 11 million bits of sensory data hitting you per second. It prioritizes what you've deemed important. If you focus on problems, it filters for problems. If you focus on opportunities, it finds opportunities. You can deliberately program your RAS through intention-setting and journaling. Write down three things you want to notice today — opportunities, kindness, beauty. Your brain will start finding them everywhere. This is not mysticism — it's how filtering works.",
        "title": "Your Brain Has a Filter System That Determines What Reality You Experience",
        "description": "The reticular activating system filters 11 million bits of sensory data per second based on what you focus on. Deliberately programming it through intention-setting shapes which aspects of reality your consciousness accesses.",
        "hashtags": ["psychology","RAS","reticularsystem","mindfacts","brainfacts","neuroscience","attention","mindpower","brainscience","awareness"],
        "tiktok_caption": "Your brain's filter determines what reality you experience #psychology #RAS #mindfacts",
        "hook": "Your brain filters reality based on what you focus on — and you can deliberately reprogram it."
    },
    {
        "script": "Adrenaline and cortisol — your stress hormones — were designed for short-term crises. The fight-or-flight response evolved to handle a predator charging at you: 2 minutes of intense physical response, then resolution. In modern life, we activate the same response for emails, traffic, and social media comments — and it never fully resolves. Chronic low-level stress keeps cortisol elevated 24 hours a day. Over time this damages the immune system, cardiovascular system, digestive system, and brain. Your body doesn't know the difference between a predator and a difficult boss. But the physiological damage is identical.",
        "title": "Your Stress System Was Designed for 2 Minutes Not All Day",
        "description": "The fight-or-flight stress response evolved for short acute threats. Modern chronic stress keeps cortisol elevated permanently, damaging the immune system, heart, gut, and brain over time.",
        "hashtags": ["psychology","stress","cortisol","mindfacts","brainfacts","fightorflight","mentalhealth","neuroscience","stressmanagement","mindpower"],
        "tiktok_caption": "Your stress system was built for 2 minutes — not a 40-hour work week #psychology #stress #cortisol",
        "hook": "Your stress response was designed for 2 minutes — modern life runs it all day."
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

    unused = [i for i in all_indices if i not in used]

    if not unused:
        print(f"All {len(SCRIPTS)} scripts used — resetting cycle.")
        used = []
        unused = all_indices

    index = random.choice(unused)
    script_data = SCRIPTS[index]

    used.append(index)
    save_used(used)

    os.makedirs("./temp", exist_ok=True)
    with open("./temp/script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)

    total = len(SCRIPTS)
    print(f"Script {index + 1}/{total} saved to ./temp/script.json")
    print(f"Scripts used this cycle: {len(used)}/{total}")
    print(f"Title: {script_data['title']}")
    print(f"Hook:  {script_data['hook']}")


if __name__ == "__main__":
    main()
