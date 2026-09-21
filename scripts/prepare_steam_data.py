from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR
    / "data"
    / "steamdb_chart_578080.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "steam_players.csv"
)


def prepare_data():
    df = pd.read_csv(INPUT_PATH)

    df["DateTime"] = pd.to_datetime(
        df["DateTime"],
        errors="coerce",
    )

    df["Players"] = pd.to_numeric(
        df["Players"],
        errors="coerce",
    )

    df = df.dropna(
        subset=["DateTime", "Players"]
    )

    latest_datetime = df["DateTime"].max()
    current_day = latest_datetime.normalize()

    daily = (
        df
        .set_index("DateTime")["Players"]
        .resample("D")
        .max()
        .dropna()
    )

    # 아직 끝나지 않은 최신 날짜는 제외
    daily = daily[
        daily.index < current_day
    ]

    # 가장 최근 완료된 365일만 사용
    daily = daily.tail(365)

    result = daily.reset_index()

    result.columns = [
        "date",
        "value",
    ]

    result["date"] = (
        result["date"]
        .dt.strftime("%Y-%m-%d")
    )

    result["value"] = (
        result["value"]
        .round()
        .astype(int)
    )

    result["memo"] = (
        "PUBG daily peak players"
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print(
        f"원본 데이터: {len(df)}개"
    )

    print(
        f"정제 데이터: {len(result)}개"
    )

    print(
        f"기간: "
        f"{result.iloc[0]['date']} "
        f"~ "
        f"{result.iloc[-1]['date']}"
    )

    print(
        f"저장 위치: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    prepare_data()