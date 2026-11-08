CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS sites (
  site_id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  site_code TEXT UNIQUE,
  description TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS operable_units (
  ou_id BIGSERIAL PRIMARY KEY,
  site_id BIGINT NOT NULL REFERENCES sites(site_id) ON DELETE CASCADE,
  ou_code TEXT NOT NULL,
  description TEXT,
  UNIQUE(site_id, ou_code)
);

CREATE TABLE IF NOT EXISTS sampling_events (
  event_id BIGSERIAL PRIMARY KEY,
  site_id BIGINT NOT NULL REFERENCES sites(site_id),
  sample_code TEXT NOT NULL,
  sampled_at TIMESTAMPTZ,
  sample_matrix TEXT NOT NULL,
  depth_top_m NUMERIC,
  depth_bottom_m NUMERIC,
  location GEOMETRY(Point, 4326),
  source_document TEXT,
  UNIQUE(site_id, sample_code)
);
CREATE INDEX IF NOT EXISTS sampling_events_location_gix ON sampling_events USING GIST(location);

CREATE TABLE IF NOT EXISTS analytes (
  analyte_id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  casrn TEXT UNIQUE,
  analyte_group TEXT
);

CREATE TABLE IF NOT EXISTS analytical_results (
  result_id BIGSERIAL PRIMARY KEY,
  event_id BIGINT NOT NULL REFERENCES sampling_events(event_id) ON DELETE CASCADE,
  analyte_id BIGINT NOT NULL REFERENCES analytes(analyte_id),
  result_value NUMERIC,
  result_unit TEXT NOT NULL,
  qualifier TEXT,
  detection_limit NUMERIC,
  laboratory TEXT,
  method TEXT,
  reported_at TIMESTAMPTZ,
  source_reference TEXT NOT NULL,
  is_validated BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS geochemistry_results (
  geochem_id BIGSERIAL PRIMARY KEY,
  event_id BIGINT NOT NULL REFERENCES sampling_events(event_id) ON DELETE CASCADE,
  parameter TEXT NOT NULL,
  result_value NUMERIC NOT NULL,
  result_unit TEXT NOT NULL,
  method TEXT,
  source_reference TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS substrate_recipes (
  recipe_id BIGSERIAL PRIMARY KEY,
  site_id BIGINT REFERENCES sites(site_id),
  recipe_name TEXT NOT NULL,
  mineral_fraction JSONB NOT NULL DEFAULT '{}'::jsonb,
  organic_amendments JSONB NOT NULL DEFAULT '{}'::jsonb,
  water_regime JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS analysis_runs (
  run_id BIGSERIAL PRIMARY KEY,
  site_id BIGINT REFERENCES sites(site_id),
  run_type TEXT NOT NULL,
  model_name TEXT NOT NULL,
  model_version TEXT NOT NULL,
  input_snapshot JSONB NOT NULL,
  output_snapshot JSONB NOT NULL,
  uncertainty JSONB,
  evidence_status TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
