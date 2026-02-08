from pph_predictor import PPHMultimodalPredictor, PatientSnapshot


def test_risk_increases_with_worsening_state() -> None:
    model = PPHMultimodalPredictor(alert_threshold=0.65)

    baseline = PatientSnapshot(
        minutes_from_delivery=5,
        systolic_bp=118,
        heart_rate=88,
        spo2=99,
        uterotonic_dose_count=1,
        hemoglobin=11.2,
        fibrinogen=320,
        lactate=1.6,
        camera_ebl_ml=250,
    )

    severe = PatientSnapshot(
        minutes_from_delivery=20,
        systolic_bp=84,
        heart_rate=136,
        spo2=92,
        uterotonic_dose_count=4,
        hemoglobin=8.2,
        fibrinogen=150,
        lactate=4.8,
        camera_ebl_ml=1400,
    )

    low_result = model.predict(baseline)
    high_result = model.predict(severe, baseline)

    assert low_result.risk_score < high_result.risk_score
    assert high_result.alert is True
    assert high_result.risk_level == "high"


def test_low_risk_case_no_alert() -> None:
    model = PPHMultimodalPredictor(alert_threshold=0.65)
    sample = PatientSnapshot(
        minutes_from_delivery=10,
        systolic_bp=122,
        heart_rate=82,
        spo2=99,
        uterotonic_dose_count=0,
        hemoglobin=11.8,
        fibrinogen=350,
        lactate=1.4,
        camera_ebl_ml=180,
    )

    result = model.predict(sample)
    assert result.alert is False
    assert result.risk_level == "low"
