USE RDB2025_PavelTyl
GO

/*
Zadání:
-- 1. Vypište seznam doktorù, kteøí mají více než 3 pøedepsané léky.
-- 2. Vypište poslední pøedepsaný lék pro každého pacienta.
-- 3. Spoèítejte pro každého doktora, kolikrát pøedepsal Paralen (id_drug = 1) a Aspirin (id_drug = 2). Výsledky zobrazte pro každý lék do samostatného sloupce.
-- 4. Spoèítejte pro každého doktora celkový poèet pacientù a poèet pacientù, kterým pøedepsal Paralen.
-- 5. Vypište nejèastìji pøedepsaný lék pro každého doktora.
-- 6. Spoèítejte celkový poèet pøedpisù pro každého doktora a také kolikrát pøedepsal Paralen (id_drug = 1) pomocí subdotazù. Subdotazy se spustí pro každého doktora a vrátí požadované hodnoty.
-- 7. Pro každý øádek zobrazte celkový poèet (kumulativní souèet) pøedepsaných lékù pro každého doktora do aktuálního pacienta.
-- 8. Aktualizujte recepty, kde doktor je napø. "Dr. Novák" a lék je Paralen (id_drug = 1), a zmìní lék na Ibuprofen (id_drug = 3).
-- 9. Vypište prùmìrný poèet pøedpisù na pacienta každý mìsíc daného roku.
-- 10. Vytvoøte transakci pro vkládání nového pacienta do tabulky Patient, kde použijete transakci pro zajištìní, že pokud dojde k nìjaké chybì, která se vypíše, žádná data nebudou vložena. Napø. pokud id_patient nebude PK, stejnì by nemìlo jít vložit pacienta s existujícím id_patient.
*/

-- 1. Agregace s GROUP BY a HAVING
SELECT Doctor.id_doctor, Doctor.name, COUNT(Prescription.id_prescription) AS PrescriptionCount
FROM Doctor
JOIN Prescription ON Doctor.id_doctor = Prescription.id_doctor
GROUP BY Doctor.id_doctor, Doctor.name
HAVING COUNT(Prescription.id_prescription) > 3

-- 2. Výbìr dat s oknem (Window Function) - ROW_NUMBER
SELECT id_prescription, id_patient, id_doctor, id_drug
FROM (
    SELECT id_prescription, id_patient, id_doctor, id_drug, 
           ROW_NUMBER() OVER (PARTITION BY id_patient ORDER BY id_prescription DESC) AS RowNum
    FROM Prescription
) AS RankedPrescriptions
WHERE RowNum = 1

SELECT id_prescription, id_patient, id_doctor, id_drug
FROM (
    SELECT id_prescription, id_patient, id_doctor, id_drug, 
           ROW_NUMBER() OVER (PARTITION BY id_patient ORDER BY id_prescription DESC) AS RowNum
    FROM Prescription
) AS RankedPrescriptions
WHERE RowNum = 1

WITH RankedPrescriptions AS (
    SELECT id_prescription, id_patient, id_doctor, id_drug, 
           ROW_NUMBER() OVER (PARTITION BY id_patient ORDER BY id_prescription DESC) AS RowNum
    FROM Prescription
)
SELECT id_prescription, id_patient, id_doctor, id_drug
FROM RankedPrescriptions
WHERE RowNum = 1

-- 3. Agregace s více podmínkami (CASE WHEN)
SELECT 
    id_doctor,
    COUNT(CASE WHEN id_drug = 1 THEN 1 END) AS ParalenPrescriptions,
    COUNT(CASE WHEN id_drug = 2 THEN 1 END) AS AspirinPrescriptions
FROM Prescription
GROUP BY id_doctor

-- 4. Kombinace INNER JOIN, LEFT JOIN a agregace
SELECT 
    Doctor.name, 
    COUNT(DISTINCT Prescription.id_patient) AS NumberOfPatients,
    COUNT(DISTINCT CASE WHEN Drug.id_drug = 1 THEN Prescription.id_patient END) AS ParalenPatients
FROM Doctor
JOIN Prescription ON Doctor.id_doctor = Prescription.id_doctor
LEFT JOIN Drug ON Prescription.id_drug = Drug.id_drug
GROUP BY Doctor.name
GO

-- 5. Získání nejèastìji pøedepsaného léku pro každého doktora
WITH DoctorDrugs AS (
    SELECT id_doctor, id_drug, COUNT(*) AS PrescriptionCount
    FROM Prescription
    GROUP BY id_doctor, id_drug
)
SELECT id_doctor, id_drug
FROM (
    SELECT id_doctor, id_drug, PrescriptionCount,
           RANK() OVER (PARTITION BY id_doctor ORDER BY PrescriptionCount DESC) AS Rank
    FROM DoctorDrugs
) AS RankedDrugs
WHERE Rank = 1

SELECT id_doctor, id_drug
FROM (
    SELECT id_doctor, id_drug, COUNT(*) AS PrescriptionCount,
           RANK() OVER (PARTITION BY id_doctor ORDER BY COUNT(*) DESC) AS Rank
    FROM Prescription
    GROUP BY id_doctor, id_drug
) AS RankedDrugs
WHERE Rank = 1

-- 6. Sèítání agregovaných hodnot a použití subdotazu
SELECT 
    id_doctor,
    (SELECT COUNT(*) FROM Prescription WHERE id_doctor = Doctor.id_doctor) AS PrescriptionCount,
    (SELECT SUM(CASE WHEN id_drug = 1 THEN 1 ELSE 0 END) FROM Prescription WHERE id_doctor = Doctor.id_doctor) AS ParalenPrescriptions
FROM Doctor

-- 7. Kumulativní souèet (cumulative sum) s oknem
SELECT 
    id_patient,
    id_doctor,
    id_drug,
    COUNT(*) AS PrescriptionCount,
    SUM(COUNT(*)) OVER (PARTITION BY id_doctor ORDER BY id_patient) AS CumulativePrescriptions
FROM Prescription
GROUP BY id_patient, id_doctor, id_drug
ORDER BY id_doctor, id_patient

-- 8. UPDATE s poddotazem a INNER JOIN
UPDATE Prescription
SET id_drug = 3
FROM Prescription p
JOIN Doctor d ON p.id_doctor = d.id_doctor
WHERE d.name = 'Dr. PU' AND p.id_drug = 1

-- 9. Získání prùmìrného poètu pøedpisù na pacienta za mìsíc
SELECT 
    YEAR(Prescription.date) AS Year,
    MONTH(Prescription.date) AS Month,
    COUNT(DISTINCT Prescription.id_patient) AS TotalPatients,
    COUNT(Prescription.id_prescription) / CONVERT(float, COUNT(DISTINCT Prescription.id_patient)) AS AvgPrescriptionsPerPatient
FROM Prescription
GROUP BY YEAR(Prescription.date), MONTH(Prescription.date)

-- 10. Pøíklad transakce, který se zamìøuje pouze na jednu tabulku a jednu operaci. Tento pøíklad ukáže, jak transakce funguje pøi vkládání nového pacienta do tabulky Patient, kde použijeme transakci pro zajištìní, že pokud dojde k nìjaké chybì, žádná data nebudou vložena.
BEGIN TRANSACTION;

BEGIN TRY
    INSERT INTO Patient (id_patient, name) VALUES (5, 'Pavel Tyl');
    -- tady bude nìjaká kontrola a po ní provedu commit
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    -- Pokud dojde k chybì, provedu rollback
    ROLLBACK TRANSACTION;
    PRINT 'Chyba pøi vkládání pacienta: ' + ERROR_MESSAGE();
END CATCH
