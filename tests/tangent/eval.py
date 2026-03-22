"""
Tangent Skill Evaluation Suite

Runs /tangent against a set of topics, collects outputs, scores them on
novelty, coherence, actionability, and consistency. Compares against
vanilla baseline (same topic, no skill).

Usage:
    uv run eval.py --topics topics.json --runs 5
    uv run eval.py --topics topics.json --runs 5 --score-only  # skip generation, just score existing results
"""

import anthropic
import json
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

RESULTS_DIR = Path(__file__).parent / "results"
SKILL_PROMPT = Path(__file__).parent.parent.parent / ".claude" / "skills" / "tangent" / "SKILL.md"

SCORER_SYSTEM = """You are an evaluator scoring creative AI output. Score ONLY with numbers 1-5 for each metric. Be harsh.

Return valid JSON only, no other text:
{
  "novelty": <1-5>,
  "novelty_reason": "<one sentence>",
  "coherence": <1-5>,
  "coherence_reason": "<one sentence>",
  "actionability": <1-5>,
  "actionability_reason": "<one sentence>"
}

Scoring guide:
NOVELTY - Would a human have thought of this unprompted?
  1: Obvious, first-thing-anyone-would-say
  2: Slightly unexpected angle but common
  3: Genuinely surprising connection
  4: Cross-domain leap that makes you pause
  5: Something you've never seen connected before

COHERENCE - Is the reasoning defensible?
  1: Nonsense, no logical thread
  2: Vague hand-waving
  3: Followable but has gaps
  4: Clear reasoning with minor leaps
  5: Airtight, you could explain this to someone else

ACTIONABILITY - Can you DO something with the distillation bullets?
  1: Pure abstraction, no next step
  2: Interesting but impractical
  3: At least one bullet is directly usable
  4: Multiple bullets you'd actually try
  5: You'd change your approach based on this"""

MODEL = "claude-sonnet-4-6"


def load_topics(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)


def load_skill_prompt() -> str:
    with open(SKILL_PROMPT) as f:
        content = f.read()
    parts = content.split("---", 2)
    if len(parts) >= 3:
        return parts[2].strip()
    return content


def run_tangent(client: anthropic.Anthropic, topic: str, skill_prompt: str) -> str:
    prompt = skill_prompt.replace("$ARGUMENTS", topic)
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def run_baseline(client: anthropic.Anthropic, topic: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"Give me creative ideas and unexpected angles on this topic: {topic}",
            }
        ],
    )
    return response.content[0].text


def score_output(client: anthropic.Anthropic, topic: str, output: str, retries: int = 3) -> dict:
    for attempt in range(retries):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=512,
                system=SCORER_SYSTEM,
                messages=[
                    {
                        "role": "user",
                        "content": f"Topic: {topic}\n\nOutput to score:\n{output}",
                    }
                ],
            )
            text = response.content[0].text.strip()
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                text = text[start:end]
            return json.loads(text)
        except (json.JSONDecodeError, Exception):
            if attempt == retries - 1:
                print(f"    WARNING: scoring failed after {retries} attempts, using defaults")
                return {"novelty": 0, "novelty_reason": "parse error", "coherence": 0, "coherence_reason": "parse error", "actionability": 0, "actionability_reason": "parse error"}


def measure_consistency(outputs: list[str]) -> float:
    """How different are N runs on the same topic? Higher = more diverse = better."""
    if len(outputs) < 2:
        return 0.0
    distillations = []
    for output in outputs:
        lower = output.lower()
        idx = lower.find("distillation")
        if idx != -1:
            distillations.append(output[idx:])
        else:
            distillations.append(output[-500:])

    hashes = set()
    for d in distillations:
        normalized = " ".join(d.split())[:200]
        hashes.add(hashlib.md5(normalized.encode()).hexdigest())

    return len(hashes) / len(outputs)


def run_experiment(topics_path: str, num_runs: int, score_only: bool = False):
    client = anthropic.Anthropic()
    topics = load_topics(topics_path)
    skill_prompt = load_skill_prompt()
    RESULTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_dir = RESULTS_DIR / timestamp
    experiment_dir.mkdir(exist_ok=True)

    all_results = []

    for topic_entry in topics:
        topic = topic_entry["topic"]
        category = topic_entry.get("category", "general")
        print(f"\n{'='*60}")
        print(f"Topic: {topic} [{category}]")
        print(f"{'='*60}")

        topic_results = {
            "topic": topic,
            "category": category,
            "tangent_runs": [],
            "baseline": None,
            "scores": {"tangent": [], "baseline": None},
            "consistency": None,
        }

        if not score_only:
            tangent_outputs = []
            for i in range(num_runs):
                print(f"  Tangent run {i+1}/{num_runs}...")
                output = run_tangent(client, topic, skill_prompt)
                tangent_outputs.append(output)
                topic_results["tangent_runs"].append(output)

            print(f"  Baseline run...")
            baseline = run_baseline(client, topic)
            topic_results["baseline"] = baseline

            topic_results["consistency"] = measure_consistency(tangent_outputs)
            print(f"  Consistency (diversity): {topic_results['consistency']:.2f}")

        print(f"  Scoring tangent outputs...")
        for i, output in enumerate(topic_results["tangent_runs"]):
            score = score_output(client, topic, output)
            topic_results["scores"]["tangent"].append(score)
            print(
                f"    Run {i+1}: N={score['novelty']} C={score['coherence']} A={score['actionability']}"
            )

        print(f"  Scoring baseline...")
        baseline_score = score_output(client, topic, topic_results["baseline"])
        topic_results["scores"]["baseline"] = baseline_score
        print(
            f"    Baseline: N={baseline_score['novelty']} C={baseline_score['coherence']} A={baseline_score['actionability']}"
        )

        all_results.append(topic_results)

    # Save raw results
    with open(experiment_dir / "results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    # Print summary
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    for r in all_results:
        tangent_scores = r["scores"]["tangent"]
        baseline = r["scores"]["baseline"]

        avg_n = sum(s["novelty"] for s in tangent_scores) / len(tangent_scores)
        avg_c = sum(s["coherence"] for s in tangent_scores) / len(tangent_scores)
        avg_a = sum(s["actionability"] for s in tangent_scores) / len(tangent_scores)

        print(f"\n{r['topic']} [{r['category']}]")
        print(
            f"  Tangent avg:  N={avg_n:.1f}  C={avg_c:.1f}  A={avg_a:.1f}  Diversity={r['consistency']:.2f}"
        )
        print(
            f"  Baseline:     N={baseline['novelty']}    C={baseline['coherence']}    A={baseline['actionability']}"
        )
        print(
            f"  Delta:        N={avg_n - baseline['novelty']:+.1f}  C={avg_c - baseline['coherence']:+.1f}  A={avg_a - baseline['actionability']:+.1f}"
        )

    # Save summary
    with open(experiment_dir / "summary.txt", "w") as f:
        f.write(f"Experiment: {timestamp}\n")
        f.write(f"Model: {MODEL}\n")
        f.write(f"Runs per topic: {num_runs}\n")
        f.write(f"Topics: {len(topics)}\n\n")
        for r in all_results:
            tangent_scores = r["scores"]["tangent"]
            baseline = r["scores"]["baseline"]
            avg_n = sum(s["novelty"] for s in tangent_scores) / len(tangent_scores)
            avg_c = sum(s["coherence"] for s in tangent_scores) / len(tangent_scores)
            avg_a = sum(s["actionability"] for s in tangent_scores) / len(tangent_scores)
            f.write(f"{r['topic']} [{r['category']}]\n")
            f.write(f"  Tangent: N={avg_n:.1f} C={avg_c:.1f} A={avg_a:.1f} D={r['consistency']:.2f}\n")
            f.write(f"  Base:    N={baseline['novelty']} C={baseline['coherence']} A={baseline['actionability']}\n")
            f.write(f"  Delta:   N={avg_n - baseline['novelty']:+.1f} C={avg_c - baseline['coherence']:+.1f} A={avg_a - baseline['actionability']:+.1f}\n\n")

    print(f"\nResults saved to {experiment_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", default="topics.json")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--score-only", action="store_true")
    args = parser.parse_args()
    run_experiment(args.topics, args.runs, args.score_only)
