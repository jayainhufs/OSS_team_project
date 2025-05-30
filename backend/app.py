from flask import Flask, request, jsonify
import json
import random
import os

app = Flask(__name__)

# 안전하게 JSON 데이터 로드
DATA_PATH = "sample_fashion_data.json"
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []  # 예외 처리

@app.route("/")
def index():
    return "✅ 패션 마법사 서버가 실행 중입니다!"

@app.route("/recommend", methods=["GET"])
def recommend():
    gender = request.args.get("gender")
    age = request.args.get("age")
    style = request.args.get("style")
    occasion = request.args.get("occasion")

    # 매핑값 (실제 survey 값과 일치시킴)
    gender_map = {"남성": 1, "여성": 2}
    age_map = {"20대": 1, "30대": 2, "40대": 3, "50대": 4}
    occasion_map = {"출근": 1, "일상": 5}

    gender_val = gender_map.get(gender)
    age_val = age_map.get(age)
    occasion_val = occasion_map.get(occasion)

    # 필터링
    matched = [
        item for item in data
        if item["user"]["r_gender"] == gender_val
        and item["user"]["age"] == age_val
        and item["item"]["style"] == style
        and item["item"]["survey"]["Q3"] == occasion_val
    ]

    if not matched:
        return jsonify({"message": "조건에 맞는 결과가 없습니다."})

    results = random.sample(matched, min(2, len(matched)))

    return jsonify({
        "recommendations": [
            {
                "imgName": item["item"]["imgName"],
                "style": item["item"]["style"],
                "era": item["item"]["era"],
                "description": "AI가 추천한 스타일입니다!"
            }
            for item in results
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)