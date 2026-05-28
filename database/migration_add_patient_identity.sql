-- Migration: Add patient identification fields
-- Run this to update existing patients table

USE disease_detection;

-- Add new columns to patients table
ALTER TABLE patients 
ADD COLUMN patient_name VARCHAR(255) AFTER user_id,
ADD COLUMN patient_id_number VARCHAR(100) UNIQUE AFTER patient_name,
ADD COLUMN date_of_birth DATE AFTER patient_id_number,
ADD COLUMN phone VARCHAR(20) AFTER gender,
ADD COLUMN email VARCHAR(255) AFTER phone,
ADD COLUMN address TEXT AFTER email,
ADD COLUMN emergency_contact_name VARCHAR(255) AFTER medical_history,
ADD COLUMN emergency_contact_phone VARCHAR(20) AFTER emergency_contact_name;

-- Add indexes
CREATE INDEX idx_patient_id ON patients(patient_id_number);
CREATE INDEX idx_name ON patients(patient_name);

-- Update existing records with placeholder data (optional - can be updated by users)
UPDATE patients 
SET patient_name = CONCAT('Patient ', id),
    patient_id_number = CONCAT('P', LPAD(id, 6, '0'))
WHERE patient_name IS NULL;

SELECT 'Migration completed successfully!' as status;
