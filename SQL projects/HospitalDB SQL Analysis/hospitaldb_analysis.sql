-- Hospital Database Analysis
-- Advanced SQL using CTEs, window functions, and more
-- See README for project summary and key business questions

USE hospitalDB;

-- What is the average number of appointments per patient?

WITH avg_appointments AS (
    SELECT
        p.patient_id,
        COUNT(a.appointment_id) AS number_of_appointments
    FROM patients p
    JOIN appointments a
    ON p.patient_id = a.patient_id
    GROUP BY p.patient_id
)
SELECT AVG(number_of_appointments) AS avg_number_of_appointments
FROM avg_appointments;


-- Calculate summary statistics for number of appointments

WITH appointment_count AS (
    SELECT
        p.patient_id,
        COUNT(a.appointment_id) AS number_of_appointments
    FROM patients p
    JOIN appointments a
        ON p.patient_id = a.patient_id
    GROUP BY p.patient_id
),
mode_calculation AS (
    SELECT 
        number_of_appointments, 
        COUNT(*) AS frequency
    FROM appointment_count
    GROUP BY number_of_appointments
),
median_cte AS (
    SELECT *,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY number_of_appointments)
            OVER () AS median
    FROM appointment_count
),
summary_stats AS (
    SELECT 
        MAX(number_of_appointments) AS maximum,
        MIN(number_of_appointments) AS minimum,
        AVG(number_of_appointments) AS average,
        ROUND(STDEV(number_of_appointments), 4) AS std_deviation,
        MAX(median) AS median
    FROM median_cte
),
mode_value AS (
    SELECT TOP 1 number_of_appointments AS mode
    FROM mode_calculation
    ORDER BY frequency DESC
)
SELECT 
    s.maximum,
    s.minimum,
    s.average,
    s.std_deviation,
    s.median,
    m.mode
FROM summary_stats s
CROSS JOIN mode_value m;


-- What is the most common reason for visit?

WITH reason_count AS (
    SELECT 
        reason_for_visit, 
        COUNT(reason_for_visit) AS count_
    FROM appointments
    GROUP BY reason_for_visit
) 
SELECT TOP 1 reason_for_visit AS most_common_reason
FROM reason_count
ORDER BY count_ DESC;


-- Which day(s) of the week have the most appointments?

WITH date_cast AS (
    SELECT
        FORMAT(CAST(appointment_date AS DATE), 'dddd') AS day_of_week
    FROM appointments
),
weekday_count AS (
    SELECT
        day_of_week,
        COUNT(*) AS weekday_count
    FROM date_cast
    GROUP BY day_of_week
),
max_weekday_count AS (
    SELECT
        MAX(weekday_count) AS max_weekday
    FROM weekday_count
)
SELECT
    day_of_week,
    weekday_count AS appointment_count
FROM weekday_count
WHERE weekday_count = (SELECT max_weekday FROM max_weekday_count);


-- What is the average time between appointments per patient?

WITH appts AS (
    SELECT 
        p.patient_id, 
        CAST(a.appointment_date AS DATETIME) + CAST(a.appointment_time AS DATETIME) AS appointment
    FROM appointments a
    JOIN patients p
    ON p.patient_id = a.patient_id
),
prev_appts AS (
    SELECT
        patient_id,
        appointment,
        LAG(appointment, 1) OVER (PARTITION BY patient_id ORDER BY appointment) AS previous_appointment
    FROM appts
),
appts_diff AS (
    SELECT
        patient_id,
        DATEDIFF(SECOND, previous_appointment, appointment) AS avg_date_diff
    FROM prev_appts
    WHERE previous_appointment IS NOT NULL
)
SELECT
    patient_id,
    ROUND(AVG(avg_date_diff) / 86400.0, 2) AS avg_date_diff
FROM appts_diff
GROUP BY patient_id;


-- Average time between registration date and first treatment?

WITH first_treatment AS (
    SELECT p.patient_id, MIN(t.treatment_date) AS first_treatment_date
    FROM patients p
    JOIN billing b ON p.patient_id = b.patient_id
    JOIN treatments t ON t.treatment_id = b.treatment_id
    GROUP BY p.patient_id
) 
SELECT 
    AVG(DATEDIFF(DAY, p.registration_date, t.first_treatment_date)) AS avg_num_days_between_registration_and_treatment
FROM first_treatment t
JOIN patients p
ON t.patient_id = p.patient_id;


-- Which doctors have the longest average gaps between appointments (low utilization)?

WITH prev_appt AS (
    SELECT 
        d.doctor_id,
        CONCAT('Dr. ', d.first_name, ' ', d.last_name) AS doctor_name,
        a.appointment_date, 
        LAG(a.appointment_date, 1) OVER (PARTITION BY d.doctor_id ORDER BY a.appointment_date) AS previous_appointment
    FROM appointments a
    JOIN doctors d
    ON d.doctor_id = a.doctor_id
)
SELECT
    doctor_id,
    doctor_name,
    AVG(DATEDIFF(DAY, previous_appointment, appointment_date)) AS avg_gap
FROM prev_appt
WHERE previous_appointment IS NOT NULL
GROUP BY 
    doctor_id,
    doctor_name
ORDER BY avg_gap DESC;


-- How many appointments are completed per doctor per month?

WITH mycte AS (
    SELECT
        d.doctor_id,
        COUNT(a.appointment_id) AS appointment_count
    FROM dbo.appointments a
    JOIN dbo.doctors d ON d.doctor_id = a.doctor_id
    GROUP BY d.doctor_id
)
SELECT
    a.doctor_id,
    CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
    a.appointment_count
FROM mycte a
JOIN dbo.doctors d
ON a.doctor_id = d.doctor_id;


-- What’s the average wait time between a patient’s first and second visit?

WITH first_treatment AS (
    SELECT p.patient_id, 
           CONCAT(p.first_name, ' ', p.last_name) AS full_name, 
           CAST(MIN(t.treatment_date) AS datetime) AS first_visit
    FROM patients p
    JOIN billing b ON p.patient_id = b.patient_id
    JOIN treatments t ON b.treatment_id = t.treatment_id
    GROUP BY p.patient_id, p.first_name, p.last_name
),
second_treatment AS (
    SELECT s.patient_id, s.full_name, CAST(MIN(t.treatment_date) AS datetime) AS second_visit
    FROM first_treatment s
    JOIN patients p ON p.patient_id = s.patient_id
    JOIN billing b ON p.patient_id = b.patient_id
    JOIN treatments t ON b.treatment_id = t.treatment_id
    WHERE t.treatment_date > s.first_visit
    GROUP BY s.patient_id, s.full_name
)
SELECT AVG(DATEDIFF(DAY, t.first_visit, s.second_visit)) AS avg_wait_time_between_first_and_second_visit
FROM first_treatment t
JOIN second_treatment s ON t.patient_id = s.patient_id;


-- What’s the cancellation rate by doctor?

WITH doc_appt_count AS (
    SELECT
        d.doctor_id,
        CONCAT(d.first_name, ' ', d.last_name) AS doctor_full_name,
        COUNT(a.appointment_id) AS appointments_per_doc
    FROM doctors d
    JOIN appointments a ON d.doctor_id = a.doctor_id
    GROUP BY
        d.doctor_id,
        d.first_name,
        d.last_name
),
doc_appt_cancel AS (
    SELECT
        d.doctor_id,
        CONCAT(d.first_name, ' ', d.last_name) AS doctor_full_name,
        COUNT(a.appointment_id) AS cancels_per_doc
    FROM doctors d
    JOIN appointments a ON d.doctor_id = a.doctor_id
    WHERE a.status = 'Cancelled'
    GROUP BY
        d.doctor_id,
        d.first_name,
        d.last_name
)
SELECT
    a.doctor_id,
    a.doctor_full_name,
    CAST(ROUND(b.cancels_per_doc * 1.0 / a.appointments_per_doc, 2) AS decimal(5, 2)) AS cancelation_rate
FROM doc_appt_count a
JOIN doc_appt_cancel b ON a.doctor_id = b.doctor_id;


-- What's the average cost per treatment type?

SELECT
    treatment_type,
    AVG(cost) AS avg_cost_per_treatment
FROM treatments
GROUP BY treatment_type;

-- What’s the total revenue by month? By doctor?

SELECT 
    d.doctor_id, 
    YEAR(a.appointment_date) AS year,
    MONTH(a.appointment_date) AS month,
    CONCAT('$ ', ROUND(SUM(b.amount), 2)) AS revenue_per_month
FROM doctors d
JOIN appointments a ON d.doctor_id = a.doctor_id
JOIN treatments t ON a.appointment_id = t.appointment_id
JOIN billing b ON t.treatment_id = b.treatment_id
WHERE b.payment_status = 'Paid'
GROUP BY 
    d.doctor_id, 
    YEAR(a.appointment_date),
    MONTH(a.appointment_date)
ORDER BY d.doctor_id;


-- What’s the average amount paid vs billed?

WITH paid AS (
    SELECT ROUND(AVG(amount), 2) AS avg_paid
    FROM billing
    WHERE payment_status = 'Paid'
),
unpaid AS (
    SELECT ROUND(AVG(amount), 2) AS avg_unpaid
    FROM billing
    WHERE payment_status NOT IN ('Paid')
)
SELECT a.avg_paid, b.avg_unpaid
FROM paid a
CROSS JOIN unpaid b;

-- Check for duplicates in appointments table

SELECT
    appointment_id,
    patient_id,
    doctor_id,
    appointment_date,
    appointment_time,
    reason_for_visit,
    status
FROM appointments
GROUP BY
    appointment_id,
    patient_id,
    doctor_id,
    appointment_date,
    appointment_time,
    reason_for_visit,
    status
HAVING COUNT(*)>1;

-- Rank doctors by years of experience

WITH doctors_ranked AS (
    SELECT RANK() OVER (ORDER BY years_experience DESC) AS rank, 
           doctor_id, 
           years_experience
    FROM doctors
)
SELECT rank, 
       doctor_id, 
       years_experience
FROM doctors_ranked;
