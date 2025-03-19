USE RDB2025_PavelTyl
GO

/*
Zad�n�:
-- 1. Vypi�te seznam doktor�, kte�� maj� v�ce ne� 3 p�edepsan� l�ky.
-- 2. Vypi�te posledn� p�edepsan� l�k pro ka�d�ho pacienta.
-- 3. Spo��tejte pro ka�d�ho doktora, kolikr�t p�edepsal Paralen (id_drug = 1) a Aspirin (id_drug = 2). V�sledky zobrazte pro ka�d� l�k do samostatn�ho sloupce.
-- 4. Spo��tejte pro ka�d�ho doktora celkov� po�et pacient� a po�et pacient�, kter�m p�edepsal Paralen.
-- 5. Vypi�te nej�ast�ji p�edepsan� l�k pro ka�d�ho doktora.
-- 6. Spo��tejte celkov� po�et p�edpis� pro ka�d�ho doktora a tak� kolikr�t p�edepsal Paralen (id_drug = 1) pomoc� subdotaz�. Subdotazy se spust� pro ka�d�ho doktora a vr�t� po�adovan� hodnoty.
-- 7. Pro ka�d� ��dek zobrazte celkov� po�et (kumulativn� sou�et) p�edepsan�ch l�k� pro ka�d�ho doktora do aktu�ln�ho pacienta.
-- 8. Aktualizujte recepty, kde doktor je nap�. "Dr. Nov�k" a l�k je Paralen (id_drug = 1), a zm�n� l�k na Ibuprofen (id_drug = 3).
-- 9. Vypi�te pr�m�rn� po�et p�edpis� na pacienta ka�d� m�s�c dan�ho roku.
-- 10. Vytvo�te transakci pro vkl�d�n� nov�ho pacienta do tabulky Patient, kde pou�ijete transakci pro zaji�t�n�, �e pokud dojde k n�jak� chyb�, kter� se vyp�e, ��dn� data nebudou vlo�ena. Nap�. pokud id_patient nebude PK, stejn� by nem�lo j�t vlo�it pacienta s existuj�c�m id_patient.
*/

-- 1. Agregace s GROUP BY a HAVING
SELECT Doctor.id_doctor, Doctor.name, COUNT(Prescription.id_prescription) AS PrescriptionCount
FROM Doctor
JOIN Prescription ON Doctor.id_doctor = Prescription.id_doctor
GROUP BY Doctor.id_doctor, Doctor.name
HAVING COUNT(Prescription.id_prescription) > 3

-- 2. V�b�r dat s oknem (Window Function) - ROW_NUMBER
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

-- 3. Agregace s v�ce podm�nkami (CASE WHEN)
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

-- 5. Z�sk�n� nej�ast�ji p�edepsan�ho l�ku pro ka�d�ho doktora
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

-- 6. S��t�n� agregovan�ch hodnot a pou�it� subdotazu
SELECT 
    id_doctor,
    (SELECT COUNT(*) FROM Prescription WHERE id_doctor = Doctor.id_doctor) AS PrescriptionCount,
    (SELECT SUM(CASE WHEN id_drug = 1 THEN 1 ELSE 0 END) FROM Prescription WHERE id_doctor = Doctor.id_doctor) AS ParalenPrescriptions
FROM Doctor

-- 7. Kumulativn� sou�et (cumulative sum) s oknem
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

-- 9. Z�sk�n� pr�m�rn�ho po�tu p�edpis� na pacienta za m�s�c
SELECT 
    YEAR(Prescription.date) AS Year,
    MONTH(Prescription.date) AS Month,
    COUNT(DISTINCT Prescription.id_patient) AS TotalPatients,
    COUNT(Prescription.id_prescription) / CONVERT(float, COUNT(DISTINCT Prescription.id_patient)) AS AvgPrescriptionsPerPatient
FROM Prescription
GROUP BY YEAR(Prescription.date), MONTH(Prescription.date)

-- 10. P��klad transakce, kter� se zam��uje pouze na jednu tabulku a jednu operaci. Tento p��klad uk�e, jak transakce funguje p�i vkl�d�n� nov�ho pacienta do tabulky Patient, kde pou�ijeme transakci pro zaji�t�n�, �e pokud dojde k n�jak� chyb�, ��dn� data nebudou vlo�ena.
BEGIN TRANSACTION;

BEGIN TRY
    INSERT INTO Patient (id_patient, name) VALUES (5, 'Pavel Tyl');
    -- tady bude n�jak� kontrola a po n� provedu commit
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    -- Pokud dojde k chyb�, provedu rollback
    ROLLBACK TRANSACTION;
    PRINT 'Chyba p�i vkl�d�n� pacienta: ' + ERROR_MESSAGE();
END CATCH
