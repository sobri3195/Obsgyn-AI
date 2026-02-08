"""Demo runner for PPH multimodal predictor."""

from pph_predictor import PPHMultimodalPredictor, PatientSnapshot


def main() -> None:
    predictor = PPHMultimodalPredictor(alert_threshold=0.65)

    t0 = PatientSnapshot(
        minutes_from_delivery=5,
        systolic_bp=110,
        heart_rate=96,
        spo2=98,
        uterotonic_dose_count=1,
        hemoglobin=10.8,
        fibrinogen=280,
        lactate=1.9,
        camera_ebl_ml=350,
    )

    t1 = PatientSnapshot(
        minutes_from_delivery=15,
        systolic_bp=95,
        heart_rate=124,
        spo2=95,
        uterotonic_dose_count=3,
        hemoglobin=9.1,
        fibrinogen=210,
        lactate=3.6,
        camera_ebl_ml=980,
    )

    t2 = PatientSnapshot(
        minutes_from_delivery=25,
        systolic_bp=88,
        heart_rate=132,
        spo2=93,
        uterotonic_dose_count=4,
        hemoglobin=8.5,
        fibrinogen=170,
        lactate=4.4,
        camera_ebl_ml=1320,
    )

    for prev, curr in [(None, t0), (t0, t1), (t1, t2)]:
        result = predictor.predict(curr, prev)
        print(f"t={curr.minutes_from_delivery}m | risk={result.risk_score} | level={result.risk_level} | alert={result.alert}")
        for rec in result.recommendations:
            print(f"- {rec}")
        print("-" * 50)


if __name__ == "__main__":
    main()
