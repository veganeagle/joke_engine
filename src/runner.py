import json, urllib.request, urllib.error
from datetime import datetime
import config

def load_prompts():
    with open(config.PROMPTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def call_ollama(model, prompt, options=None):
    payload = {"model": model,  "prompt": prompt, "stream": False}
    if options:
        payload["options"] = options

    req = urllib.request.Request(
        config.OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=config.TIMEOUT) as resp:
        body = json.loads(resp.read().decode("utf-8"))
        return body["response"].strip()


def parse_jokes(text):
    jokes = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("JOKE_1:") or line.startswith("JOKE_2:") or line.startswith("JOKE_3:"):
            jokes.append(line.split(":", 1)[1].strip())
    if len(jokes) != 3:
        raise ValueError(f"Expected 3 jokes, got {len(jokes)}:\n{text}")
    return jokes

def parse_best_index(text):
    text = text.strip()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("BEST_INDEX:"):
            n = int(line.split(":", 1)[1].strip())
            if n not in (1, 2, 3):
                raise ValueError(f"Invalid BEST_INDEX value: {n}")
            return n
    raise ValueError(f"No BEST_INDEX found in response:\n{text}")


def append_jsonl(path, obj):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main():
    prompts = load_prompts()
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = config.LOG_DIR / f"run_{run_id}.jsonl"
    append_jsonl(log_path, {
        "event": "run_started",
        "run_id": run_id,
        "seed_joke": config.SEED_JOKE,
        "num_iterations": config.ITERATIONS
    })

    generator_prompt = prompts["generator_iteration"].replace("<<CURRENT_BEST>>", config.SEED_JOKE)
    current_best = config.SEED_JOKE
    all_jokes =[]
    best_jokes = []

    for i in range(config.ITERATIONS):
        generator_response = call_ollama(config.GENERATOR, generator_prompt, config.GENERATOR_OPTIONS)
        print(repr(generator_response))
        jokes = parse_jokes(generator_response)
        append_jsonl(log_path, {
            "event": "generated_jokes",
            "iteration": i,
            "model": config.GENERATOR,
            "prompt_sent": generator_prompt,
            "response": generator_response,
            "jokes": jokes
        })

        best_joke_prompt = prompts["coach_best"]
        best_joke_prompt = best_joke_prompt.replace("<<CURRENT_BEST>>", current_best)
        for j in range(3):            
            best_joke_prompt = best_joke_prompt.replace(f"<<JOKE_{j+1}>>", jokes[j])
            all_jokes.append(jokes[j])

        coach_eval_response = call_ollama(config.COACH, best_joke_prompt, config.COACH_OPTIONS)
        print (coach_eval_response)
        best_index = parse_best_index(coach_eval_response)
        current_best = jokes[best_index - 1]    
        best_jokes.append(current_best)
        generator_prompt = prompts["generator_iteration"].replace("<<CURRENT_BEST>>", current_best)
        append_jsonl(log_path, {
            "event": "coach_selected_best",
            "iteration": i,
            "model": config.COACH,
            "prompt_sent": best_joke_prompt,
            "response": coach_eval_response,
            "best_joke": current_best,
            "next_generator_prompt": generator_prompt
        })

    append_jsonl(log_path, { "event": "run_finished",
        "run_id": run_id,  "final_best_joke": current_best})
    print(f"Run complete. Final best joke:\n{current_best}")
    for i in range(len(all_jokes)):
        print (f"{i+1}: {all_jokes[i]}")

if __name__ == "__main__":
    main()