import os
import json
import re
import time
from wordle import check_guess
from drawer import draw_game_state

STATE_FILE = "state.json"
README_FILE = "README.md"
TEMPLATE_FILE = "README.template"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"answer": "SMART", "guesses": [], "status": "playing"}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def update_readme_from_template():
    if not os.path.exists(TEMPLATE_FILE):
        print("錯誤：找不到樣板檔")
        return

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_content = f.read()

    timestamp = int(time.time())

    repo_url = "https://raw.githubusercontent.com/wulukewu/readme-wordle/main/wordle_status.png"
    image_markdown = f"![Wordle Status]({repo_url}?v={timestamp})"

    new_content = template_content.replace("{{WORDLE_STATUS}}", image_markdown)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"README 已根據樣板更新 (使用 Raw URL)，時間戳記: {timestamp}")

def main():
    issue_title = os.environ.get("ISSUE_TITLE", "")
    match = re.search(r"guess:\s*([a-zA-Z]{5})", issue_title, re.IGNORECASE)
    
    if not match:
        print("未偵測到有效猜測，僅重繪圖片並更新 README。")
        state = load_state()
        draw_game_state(state)
        update_readme_from_template()
        return

    guess_word = match.group(1).upper()
    state = load_state()
    target_word = state["answer"]

    if state["status"] != "playing":
        draw_game_state(state)
        update_readme_from_template()
        return

    result = check_guess(guess_word, target_word)
    
    state["guesses"].append({
        "word": guess_word,
        "result": result
    })

    if guess_word == target_word:
        state["status"] = "won"
    elif len(state["guesses"]) >= 6:
        state["status"] = "lost"

    save_state(state)
    draw_game_state(state)
    
    update_readme_from_template()

if __name__ == "__main__":
    main()