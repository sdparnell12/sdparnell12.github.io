from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(
    title="DIGGIT API",
    version="0.2.0",
    description="Decision-support API starter. Outputs are screening estimates, not field authorization."
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to deployed frontend origin before production.
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class HorticultureInput(BaseModel):
    ph: float = Field(6.5, ge=0, le=14)
    ec_ds_m: float = Field(1.0, ge=0)
    organic_matter_pct: float = Field(3.0, ge=0, le=100)
    water_holding_capacity_pct: float = Field(35, ge=0, le=100)
    bulk_density_g_cm3: float = Field(1.25, gt=0)
    baseline_germination_pct: float = Field(80, ge=0, le=100)
    contaminant_status: Literal["unknown", "detected", "screened"] = "unknown"
    plant_function: Literal["native", "wetland", "woody"] = "native"

class SculptureInput(BaseModel):
    co2_feed_g_day: float = Field(100, ge=0)
    capture_efficiency_pct: float = Field(70, ge=0, le=100)

@app.get("/health")
def health():
    return {"status": "ok", "service": "diggit-api", "version": "0.2.0"}

@app.post("/api/v1/horticulture/screen")
def horticulture_screen(x: HorticultureInput):
    clamp = lambda v: max(0.0, min(1.0, v))
    ph = clamp(1 - abs(x.ph - 6.5) / 4.5)
    ec = clamp(1 - x.ec_ds_m / 8)
    om = clamp(x.organic_matter_pct / 5)
    water = clamp(1 - abs(x.water_holding_capacity_pct - 40) / 60)
    density = clamp(1 - max(0, x.bulk_density_g_cm3 - 1.0) / 1.2)
    score = 100 * (0.25*ph + 0.20*ec + 0.15*om + 0.20*water + 0.20*density)
    warnings = [
        "Provisional heuristic only; not calibrated to a plant species or sediment type.",
        "Plant establishment does not demonstrate contaminant remediation.",
        "Measure contaminant bioavailability, leachate and plant-tissue uptake."
    ]
    if x.contaminant_status == "unknown":
        warnings.append("Contaminants are uncharacterized; no planting suitability conclusion is supported.")
    elif x.contaminant_status == "detected":
        warnings.append("Contaminants are reported detected; assess exposure pathways before planting.")
    return {
        "screening_index_0_100": round(score, 1),
        "germination_weighted_index_not_rate": round(score*x.baseline_germination_pct/100, 1),
        "plant_function_selected": x.plant_function,
        "contaminant_status": x.contaminant_status,
        "warnings": warnings,
        "model_version": "heuristic-0.1",
        "evidence_status": "illustrative; requires calibration and validation"
    }

@app.post("/api/v1/sculpture/carbonate-estimate")
def carbonate_estimate(x: SculptureInput):
    captured = x.co2_feed_g_day * x.capture_efficiency_pct / 100
    return {
        "captured_co2_g_day_estimate": round(captured, 2),
        "theoretical_caco3_g_day": round(captured * 100.0869 / 44.0095, 2),
        "caoh2_stoichiometric_equivalent_g_day": round(captured * 74.0927 / 44.0095, 2),
        "assumption": "100% conversion of captured CO2 to CaCO3; theoretical upper bound",
        "warnings": [
            "Particulate carbon (soot/black carbon) is not converted to carbonate by this calculation.",
            "Verify mineral phase, carbon balance, gas-transfer efficiency and dissolved chemistry.",
            "Contained laboratory concept only; do not discharge process water without characterization."
        ],
        "model_version": "stoichiometric-0.1"
    }
