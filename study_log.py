import os
import json
from datetime import datetime

def update_study_log(action, correct=False, incorrect=False, session_time=None):
    """
    action: "study" | "register" | "delete"
    correct: True/False (정답 여부, 공부할 때만 사용)
    incorrect: True/False (오답 여부, 공부할 때만 사용)
    session_time: (start, end) 튜플 ("10:05", "10:45") - 공부할 때만 사용
    """
    log_path = "data/study_log.json"
    today = datetime.now().strftime("%Y-%m-%d")

    # 기존 로그 불러오기
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    else:
        log_data = {}

    # 오늘 날짜 데이터 초기화
    if today not in log_data:
        log_data[today] = {
            "studied_word_count": 0,
            "registered_word_count": 0,
            "deleted_word_count": 0,
            "correct_count": 0,
            "incorrect_count": 0,
            "study_minutes": 0,
            "study_sessions": []
        }

    # 카운트 업데이트
    if action == "study":
        log_data[today]["studied_word_count"] += 1
        if correct:
            log_data[today]["correct_count"] += 1
        if incorrect:
            log_data[today]["incorrect_count"] += 1
        if session_time:
            start, end = session_time
            log_data[today]["study_sessions"].append({"start": start, "end": end})
            # 선택: study_minutes는 직접 계산해서 더하기 (예: 40분)
    elif action == "register":
        log_data[today]["registered_word_count"] += 1
    elif action == "delete":
        log_data[today]["deleted_word_count"] += 1

    # 저장
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def minutes_between(start, end):
    """
    두 시간 문자열("HH:MM") 사이의 분 단위 차이를 반환
    """
    fmt = "%H:%M"
    delta = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
    return delta.seconds // 60