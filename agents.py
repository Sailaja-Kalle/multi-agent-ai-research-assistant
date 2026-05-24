from groq import Groq
import os
from dotenv import load_dotenv
from tools import quick_answer, search_web, search_and_scrape, scrape_url

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def call_llm(prompt, system="You are a helpful AI assistant."):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    return response.choices[0].message.content

def research_agent(query):
    print(f"\n🔍 Research Agent: {query}")
    results = search_and_scrape(query, limit=3)
    all_content = ""
    for i, r in enumerate(results):
        all_content += f"\nSource {i+1}: {r['title']}\n"
        all_content += f"URL: {r['url']}\n"
        all_content += f"Content: {r['content']}\n"
        all_content += f"Scraped: {r['scraped'][:1000]}\n"
        all_content += "-"*50 + "\n"
    return all_content

def judge_agent(query, content):
    print("\n⚖️ Judge Agent checking quality...")
    prompt = f"""
You are a strict quality judge for research evidence.

Research Question: {query}

Evidence Collected:
{content[:3000]}

Evaluate this evidence and respond in EXACTLY this format:
SCORE: [number between 0.0 and 1.0]
DECISION: [GOOD or NEEDS_MORE]
REASON: [one sentence explanation]
MISSING: [list what information is still needed, or NONE]

Be strict. Score must be 0.85 or above to be GOOD.
"""
    result = call_llm(prompt, "You are a strict research quality judge.")
    print(f"⚖️ Judge result:\n{result}")
    return result

def parse_judge_result(judge_result):
    score = 0.0
    decision = "NEEDS_MORE"
    missing = []

    for line in judge_result.split("\n"):
        line = line.strip()
        if line.startswith("SCORE:"):
            try:
                score = float(line.replace("SCORE:", "").strip())
            except:
                score = 0.5
        elif line.startswith("DECISION:"):
            decision = line.replace("DECISION:", "").strip()
        elif line.startswith("MISSING:"):
            missing_text = line.replace("MISSING:", "").strip()
            if missing_text != "NONE":
                missing = [missing_text]

    return score, decision, missing

def writer_agent(query, all_content):
    print("\n✍️ Writer Agent creating report...")
    prompt = f"""
Write a professional research report for this question:
{query}

Based on this evidence:
{all_content[:5000]}

Structure the report with these sections:
1. Executive Summary
2. Key Findings
3. Context
4. Detailed Analysis
5. Implications
6. Sources

Write clearly and professionally.
Keep each section detailed and informative.
"""
    return call_llm(
        prompt,
        "You are an expert research analyst who writes professional reports."
    )

def manager_agent(query):
    print(f"\n🤖 Manager Agent starting: {query}")
    logs = []

    # Step 1 - Quick answer
    logs.append("⚡ Getting quick answer...")
    quick = quick_answer(query)
    logs.append(f"✅ Quick answer received")

    # Step 2 - Research
    logs.append("🔍 Research Agent searching web...")
    content = research_agent(query)
    logs.append("✅ Web search complete")

    # Step 3 - Judge
    logs.append("⚖️ Judge Agent checking quality...")
    judgment = judge_agent(query, content)
    score, decision, missing = parse_judge_result(judgment)
    logs.append(f"✅ Judge score: {score} — {decision}")

    # Step 4 - If needs more
    if decision == "NEEDS_MORE" or score < 0.85:
        logs.append("🔄 Getting more information...")
        extra_query = query
        if missing:
            extra_query = query + " " + " ".join(missing)
        extra_content = research_agent(extra_query)
        content = content + "\n\nADDITIONAL RESEARCH:\n" + extra_content

        # Judge again
        logs.append("⚖️ Judge Agent checking again...")
        judgment2 = judge_agent(query, content)
        score2, decision2, _ = parse_judge_result(judgment2)
        logs.append(f"✅ Judge score: {score2} — {decision2}")

        # Step 5 - If still weak, scrape top URLs
        if decision2 == "NEEDS_MORE" or score2 < 0.85:
            logs.append("🌐 Scraping top sources deeply...")
            results = search_web(query, limit=5)
            for r in results[:3]:
                scraped = scrape_url(r["url"])
                content += f"\nDeep scrape of {r['url']}:\n{scraped}\n"
            logs.append("✅ Deep scraping complete")

    # Step 6 - Write report
    logs.append("✍️ Writer Agent creating final report...")
    report = writer_agent(query, content)
    logs.append("✅ Report complete!")

    return report, logs