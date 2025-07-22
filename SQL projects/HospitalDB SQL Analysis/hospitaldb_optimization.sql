-- HospitalDB Optimization
-- Defines reusable views to simplify queries and improve readability
-- See README for context

USE hospitalDB;

GO
CREATE VIEW patdoctreat AS
SELECT 
	d.doctor_id,
	d.first_name as doctor_firstname,
	d.last_name as doctor_lastname,
	d.email as doctor_email,
	d.specialization,
	d.phone_number,
	d.years_experience,
	d.hospital_branch,
	t.*,
	p.*
FROM doctors d
JOIN appointments a ON d.doctor_id = a.doctor_id
JOIN treatments t ON t.appointment_id = a.appointment_id
JOIN billing b ON t.treatment_id = b.treatment_id
JOIN patients p ON b.patient_id = p.patient_id;

--Find the patients who had a treatment in February. Include the patient_id, patient full name, treatment type, treatement date, doctor id, doctor full name
GO
SELECT 
	patient_id, 
	concat(first_name,' ',last_name) as patient_full_name,
	treatment_type,
	treatment_date,
	doctor_id,
	concat(doctor_firstname,' ',doctor_lastname) as doctor_full_name
FROM patdoctreat
WHERE MONTH(treatment_date) = 2;

-- How many doctors and patients share the same first name?
GO
SELECT COUNT(*) AS num_of_shared_first_names
FROM patdoctreat
WHERE doctor_firstname = first_name;
