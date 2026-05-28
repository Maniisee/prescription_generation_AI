-- AI Disease Detection System Database Schema
-- MySQL Database Setup

CREATE DATABASE IF NOT EXISTS disease_detection;
USE disease_detection;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    patient_name VARCHAR(255) NOT NULL,
    patient_id_number VARCHAR(100) UNIQUE,
    date_of_birth DATE,
    age INT NOT NULL,
    gender ENUM('male', 'female', 'other') NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    blood_pressure_systolic INT,
    blood_pressure_diastolic INT,
    temperature DECIMAL(4,1),
    pulse INT,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    symptoms TEXT,
    medical_history TEXT,
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_patient_id (patient_id_number),
    INDEX idx_name (patient_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Diagnoses table
CREATE TABLE IF NOT EXISTS diagnoses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    disease VARCHAR(255) NOT NULL,
    confidence DECIMAL(5,2) NOT NULL,
    symptoms JSON NOT NULL,
    vitals JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    INDEX idx_patient (patient_id),
    INDEX idx_disease (disease)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    diagnosis_id INT NOT NULL,
    medications JSON NOT NULL,
    dosage TEXT,
    instructions TEXT,
    precautions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (diagnosis_id) REFERENCES diagnoses(id) ON DELETE CASCADE,
    INDEX idx_diagnosis (diagnosis_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Disease information table (for reference)
CREATE TABLE IF NOT EXISTS diseases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    symptoms TEXT,
    treatment TEXT,
    severity ENUM('low', 'medium', 'high', 'critical'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample diseases
INSERT INTO diseases (name, description, symptoms, severity) VALUES
('Common Cold', 'Viral infection of upper respiratory tract', 'Runny nose, sore throat, cough, sneezing', 'low'),
('Flu', 'Influenza viral infection', 'Fever, body aches, fatigue, cough', 'medium'),
('Diabetes', 'High blood sugar levels', 'Increased thirst, frequent urination, fatigue', 'high'),
('Hypertension', 'High blood pressure', 'Headache, dizziness, chest pain', 'high'),
('Asthma', 'Respiratory condition', 'Shortness of breath, wheezing, coughing', 'medium'),
('Migraine', 'Severe headache disorder', 'Intense headache, nausea, light sensitivity', 'medium'),
('Gastritis', 'Stomach inflammation', 'Stomach pain, nausea, bloating', 'medium'),
('Pneumonia', 'Lung infection', 'Chest pain, cough with phlegm, fever, difficulty breathing', 'high'),
('Allergic Rhinitis', 'Nasal allergies', 'Sneezing, itchy nose, congestion', 'low'),
('Bronchitis', 'Bronchial tube inflammation', 'Cough, mucus production, fatigue', 'medium')
ON DUPLICATE KEY UPDATE name=name;
