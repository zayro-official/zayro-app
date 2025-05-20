review_data = []
    for review in reviews:
        # フィルター解除（original_language を無視）
        reply = None

        if AUTO_REPLY_MODE:
            try:
                prompt = f"お客様からのレビュー:\n{review['text']}\n\nこのレビューに対して、感謝の気持ちを伝える丁寧で自然な返信文を日本語で作成してください。"
                res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "あなたは一流の寿司店の丁寧な店長です。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                )
                reply = res.choices[0].message.content.strip()
            except Exception as e:
                reply = f"(AI返信エラー: {e})"

        review_data.append({
            "author_name": review.get("author_name"),
            "rating": review.get("rating"),
            "text": review.get("text"),
            "reply": reply,
        })
