import json
import os

HIGHSCORES_FILE = os.path.join(os.path.dirname(__file__), "..", "highscores.json")


def load_highscores():
    """Return list of dicts: [{'name': str, 'score': int}, ...]"""
    try:
        with open(HIGHSCORES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                # ensure dict shape
                res = []
                for item in data:
                    if isinstance(item, dict) and 'score' in item:
                        name = str(item.get('name', '---'))
                        try:
                            score = int(item.get('score', 0))
                        except Exception:
                            score = 0
                        res.append({'name': name, 'score': score})
                return res
    except Exception:
        pass
    return []


def save_highscores(entries, top_n=5):
    """entries: list of dicts with keys name, score"""
    try:
        # Normalize and keep highest score per name (case-insensitive)
        best_by_name = {}
        for e in entries:
            if not isinstance(e, dict):
                continue
            name = str(e.get('name', ''))
            score = int(e.get('score', 0) or 0)
            key = name.strip().lower()
            if key == '':
                continue
            if key not in best_by_name or score > best_by_name[key]['score']:
                best_by_name[key] = {'name': name, 'score': score}

        combined_list = list(best_by_name.values())
        combined = sorted(combined_list, key=lambda e: e.get('score', 0), reverse=True)[:top_n]
        with open(HIGHSCORES_FILE, "w", encoding="utf-8") as f:
            json.dump(combined, f, ensure_ascii=False, indent=2)
        return combined
    except Exception:
        return entries


def add_score_with_name(name, score, top_n=5):
    entries = load_highscores()
    entries.append({'name': str(name), 'score': int(score)})
    return save_highscores(entries, top_n=top_n)


def clear_highscores():
    try:
        with open(HIGHSCORES_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    except Exception:
        pass
