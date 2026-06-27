"""
Affiliate link database for all experiments.
Shared module used by multiple repos/experiments.
"""
import random

# Mood-based affiliate links (博客來 books + other products)
AFFILIATE_LINKS = {
    "inspirational": [
        ("📖 《被討厭的勇氣》— 阿德勒心理學經典",
         "https://www.books.com.tw/products/0010702204"),
        ("📖 《活出意義來》— 維克多·弗蘭克",
         "https://www.books.com.tw/products/0010433937"),
        ("📖 《原子習慣》— 細微改變帶來巨大成就",
         "https://www.books.com.tw/products/0010792915"),
        ("📖 《與神對話》— 影響千萬人的心靈經典",
         "https://www.books.com.tw/products/0010862519"),
        ("📖 《人生的智慧》— 叔本華處世哲學",
         "https://www.books.com.tw/products/0010613113"),
        ("📖 《心態致勝》— 史丹佛心理學家教你改變思維",
         "https://www.books.com.tw/products/0010816287"),
    ],
    "healing": [
        ("📖 《也許你該找人聊聊》— 心理師的療癒故事",
         "https://www.books.com.tw/products/0010896855"),
        ("📖 《脆弱的力量》— Brené Brown 自我接納",
         "https://www.books.com.tw/products/0010645061"),
        ("📖 《當你越活越好的時候》— 療癒系散文",
         "https://www.books.com.tw/products/0010935312"),
        ("📖 《雖然是精神病但沒關係》— 療癒繪本",
         "https://www.books.com.tw/products/0010893234"),
        ("📖 《蛤蟆先生去看心理師》— 心理諮商故事",
         "https://www.books.com.tw/products/0010905538"),
        ("📖 《自我關懷的力量》— Kristin Neff 經典",
         "https://www.books.com.tw/products/0010761252"),
    ],
}


def get_affiliate_block(mood: str, count: int = 2) -> str:
    """Generate markdown affiliate links block for a given mood."""
    links = AFFILIATE_LINKS.get(mood, AFFILIATE_LINKS["healing"])
    chosen = random.sample(links, min(count, len(links)))
    lines = ["\n📌 **你可能也會喜歡：**"]
    for name, url in chosen:
        lines.append(f"  {name}")
        lines.append(f"  → {url}")
    return "\n".join(lines)
