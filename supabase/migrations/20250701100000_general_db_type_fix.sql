-- Ensure non-nullable columns and use timestamptz for timestamps

-- Users
ALTER TABLE users
  ALTER COLUMN created_at SET NOT NULL;

-- Restrictions
ALTER TABLE restrictions
  ALTER COLUMN build_category SET NOT NULL,
  ALTER COLUMN name SET NOT NULL,
  ALTER COLUMN type SET NOT NULL;

-- Types
ALTER TABLE types
  ALTER COLUMN build_category SET NOT NULL,
  ALTER COLUMN name SET NOT NULL;

-- Verification codes
ALTER TABLE verification_codes
  ALTER COLUMN created TYPE TIMESTAMPTZ USING created AT TIME ZONE 'UTC',
  ALTER COLUMN expires TYPE TIMESTAMPTZ USING expires AT TIME ZONE 'UTC';

-- Builds
ALTER TABLE builds
  ALTER COLUMN submission_time TYPE TIMESTAMPTZ USING submission_time AT TIME ZONE 'UTC';
