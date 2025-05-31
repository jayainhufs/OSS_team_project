from flask import Flask, request, jsonify, render_template
import os, glob, json, random

# backend/templates 기준으로 자동 인식됨
app = Flask(
    __name__,
    static_url_path="/images",                 # URL 경로
    static_folder="static/images"              # 실제 경로
)

DATA_DIR = os.path.join("data")  # backend/data 폴더

@app.route("/")
def index():
    return "✅ 패션 마법사 서버가 실행 중입니다!"

@app.route("/recommend_page")
def recommend_page():
    return render_template("recommend.html")

@app.route("/recommend", methods=["GET"])
def recommend():
    gender = request.args.get("gender")
    age = request.args.get("age")
    style = request.args.get("style")
    occasion = request.args.get("occasion")

    gender_map = {"남성": "M", "여성": "W"}
    age_map = {"20대": 1, "30대": 2, "40대": 3, "50대": 4}
    occasion_map = {"출근": 1, "일상": 5}

    g = gender_map.get(gender)
    a = age_map.get(age)
    o = occasion_map.get(occasion)

    matched_files = []

    for path in glob.glob(os.path.join(DATA_DIR, "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            try:
                item = json.load(f)
                user = item["user"]
                survey = item["item"]["survey"]

                if (user["r_gender"] == (1 if gender == "남성" else 2) and
                    user["age"] == a and
                    item["item"]["style"] == style and
                    survey["Q3"] == o):
                    matched_files.append(item)
            except Exception as e:
                print(f"Error in {path}: {e}")
                continue

    if not matched_files:
        return jsonify({"message": "조건에 맞는 추천 결과가 없습니다."})

    selected = random.choice(matched_files)
    img_name = selected["item"]["imgName"]
    era = selected["item"]["era"]
    s = selected["item"]["style"]

    def generate_description(style, era, occasion_code):
        kor_style = {
            "ivy": "아이비룩",
            "punk": "펑크룩",
            "feminine": "페미닌룩"
        }.get(style, style)

        kor_occ = {
            1: "출근룩",
            5: "일상 캐주얼룩"
        }.get(occasion_code, "다목적 스타일")

        return f"{era}년대의 {kor_style}은 {kor_occ}으로 활용하기 좋은 스타일입니다."

    description = generate_description(s, era, o)

    return jsonify({
        "recommendations": [
            {
                "imgName": img_name,
                "imageUrl": f"/images/{img_name}",
                "style": s,
                "era": era,
                "description": description
            }
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)