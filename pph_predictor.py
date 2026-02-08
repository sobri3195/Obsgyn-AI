"""Simple multimodal AI-style predictor for postpartum hemorrhage (PPH).

This module provides a deterministic baseline model combining:
- Vital signs + anesthesia data
- Lab values
- Camera-based estimated blood loss (EBL)

It is designed as starter code for prototyping, not as a clinical device.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Dict, List, Optional


@dataclass
class PatientSnapshot:
    """Single timepoint of multimodal data."""

    minutes_from_delivery: int
    systolic_bp: float
    heart_rate: float
    spo2: float
    uterotonic_dose_count: int
    hemoglobin: float
    fibrinogen: float
    lactate: float
    camera_ebl_ml: float


@dataclass
class PredictionResult:
    """Prediction output at a single timepoint."""

    risk_score: float
    risk_level: str
    alert: bool
    recommendations: List[str]


class PPHMultimodalPredictor:
    """Rule-guided logistic model for early PPH prediction."""

    def __init__(self, alert_threshold: float = 0.65) -> None:
        self.alert_threshold = alert_threshold

    @staticmethod
    def _sigmoid(x: float) -> float:
        return 1 / (1 + exp(-x))

    @staticmethod
    def _clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def _feature_vector(
        self, current: PatientSnapshot, previous: Optional[PatientSnapshot]
    ) -> Dict[str, float]:
        # Vital signs
        shock_index = current.heart_rate / max(current.systolic_bp, 1.0)
        f_shock_index = self._clamp01((shock_index - 0.7) / 0.6)
        f_spo2_low = self._clamp01((95.0 - current.spo2) / 10.0)

        # Labs
        f_hb_low = self._clamp01((10.0 - current.hemoglobin) / 4.0)
        f_fibrinogen_low = self._clamp01((250.0 - current.fibrinogen) / 200.0)
        f_lactate_high = self._clamp01((current.lactate - 2.0) / 4.0)

        # Blood loss (video)
        f_ebl_absolute = self._clamp01((current.camera_ebl_ml - 500.0) / 1200.0)

        ebl_trend = 0.0
        if previous is not None:
            delta_ml = current.camera_ebl_ml - previous.camera_ebl_ml
            delta_t = max(1, current.minutes_from_delivery - previous.minutes_from_delivery)
            ebl_rate = delta_ml / delta_t  # ml/min
            ebl_trend = self._clamp01((ebl_rate - 20.0) / 80.0)

        # Treatment escalation proxy
        f_uterotonic_escalation = self._clamp01(current.uterotonic_dose_count / 5.0)

        return {
            "shock_index": f_shock_index,
            "spo2_low": f_spo2_low,
            "hb_low": f_hb_low,
            "fibrinogen_low": f_fibrinogen_low,
            "lactate_high": f_lactate_high,
            "ebl_absolute": f_ebl_absolute,
            "ebl_trend": ebl_trend,
            "uterotonic_escalation": f_uterotonic_escalation,
        }

    def predict(
        self, current: PatientSnapshot, previous: Optional[PatientSnapshot] = None
    ) -> PredictionResult:
        features = self._feature_vector(current, previous)

        # Weighted linear score + intercept (heuristic baseline)
        linear = (
            -2.2
            + 1.6 * features["shock_index"]
            + 0.5 * features["spo2_low"]
            + 1.0 * features["hb_low"]
            + 1.0 * features["fibrinogen_low"]
            + 0.8 * features["lactate_high"]
            + 1.8 * features["ebl_absolute"]
            + 2.0 * features["ebl_trend"]
            + 0.4 * features["uterotonic_escalation"]
        )

        risk = self._sigmoid(linear)
        level = "low" if risk < 0.35 else "moderate" if risk < self.alert_threshold else "high"
        alert = risk >= self.alert_threshold

        recs = ["Lanjutkan monitoring ketat q5-10 menit"]
        if risk >= 0.35:
            recs.append("Evaluasi sumber perdarahan dan respons uterotonik")
        if alert:
            recs.extend(
                [
                    "Aktifkan protokol PPH / massive hemorrhage sesuai RS",
                    "Siapkan produk darah dan pertimbangkan transfusi dini",
                    "Pertimbangkan intervensi lanjutan: balloon tamponade / tindakan bedah",
                ]
            )
        if current.camera_ebl_ml >= 1000:
            recs.append("Kriteria PPH terpenuhi berdasarkan estimasi blood loss")

        return PredictionResult(risk_score=round(risk, 4), risk_level=level, alert=alert, recommendations=recs)
