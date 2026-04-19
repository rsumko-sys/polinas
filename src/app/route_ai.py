from typing import Tuple, Optional
import os
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# ... (попередній код залишається) ...

def analyze_route(distance_km: float, elevation_m: float, api_key: Optional[str] = None) -> Tuple[str, str]:
    """Аналізує маршрут за допомогою ШІ.
    Повертає Tuple[Складність, Коментар]
    """
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key or not OpenAI:
        # Fallback якщо ключ не задано
        score = (distance_km * 1.5) + ((elevation_m / 10) * 2)
        if score < 15:
            return "ЛЕГКИЙ", "Ідеально для розслаблюючого галопу. Насолоджуйтесь природою."
        elif score < 40:
            return "СЕРЕДНІЙ", "Хороше тренування для коня. Слідкуйте за диханням на підйомах."
        else:
            return "СКЛАДНИЙ", "Виклик для витривалості! Ретельно розраховуйте сили і не забувайте про крокові репризи."
            
    client = OpenAI(api_key=key)
    prompt = f"""
    Ти досвідчений тренер з кінного спорту. 
    Оціни маршрут для тренування:
    Довжина: {distance_km:.1f} км.
    Набір висоти: {elevation_m:.0f} м.
    
    Відповідь має бути рівно у 2 рядки:
    Рядок 1: Складність (одне слово: ЛЕГКИЙ, СЕРЕДНІЙ або СКЛАДНИЙ)
    Рядок 2: Короткий готично-містичний або професійний коментар (до 2 речень)
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        text = response.choices[0].message.content.strip().split('\n')
        diff = text[0].replace('Складність:', '').strip().upper()
        if 'СЕРЕД' in diff:
            diff = "СЕРЕДНІЙ"
        elif 'ЛЕГ' in diff:
            diff = "ЛЕГКИЙ"
        else:
            diff = "СКЛАДНИЙ"
        return diff, text[1] if len(text) > 1 else ""
    except Exception:
        return "СЕРЕДНІЙ", "ШІ втомився, але маршрут виглядає збалансовано."
