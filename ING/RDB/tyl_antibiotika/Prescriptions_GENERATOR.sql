USE RDB2025_PavelTyl
GO

DECLARE @num_doctors INT = 10;  -- Po�et doktor�
DECLARE @num_drugs INT = 15;    -- Po�et l�k�
DECLARE @num_patients INT = 20; -- Po�et pacient�
DECLARE @num_prescriptions INT = 30; -- Po�et p�edpis�

-- Insert random data into Doctor table
DECLARE @i INT = 1;
WHILE @i <= @num_doctors
BEGIN
    INSERT INTO Doctor (id_doctor, name) 
    VALUES (@i, 'Dr. ' + CHAR(65 + (ABS(CHECKSUM(NEWID())) % 26)) + CHAR(65 + (ABS(CHECKSUM(NEWID())) % 26)));
    SET @i = @i + 1;
END

-- Vlo� n�hodn� data do tabulky Drug
SET @i = 1;
WHILE @i <= @num_drugs
BEGIN
    INSERT INTO Drug (id_drug, trademark_drug, generic_drug) 
    VALUES (@i, 'Trademark ' + CAST(@i AS NVARCHAR), 'Generic ' + CAST(@i AS NVARCHAR));
    SET @i = @i + 1;
END

-- Vlo� n�hodn� data do tabulky Patient
SET @i = 1;
WHILE @i <= @num_patients
BEGIN
    INSERT INTO Patient (id_patient, name) 
    VALUES (@i, 'Patient ' + CAST(@i AS NVARCHAR));
    SET @i = @i + 1;
END

-- Vlo� n�hodn� data do tabulky Prescription
SET @i = 1;
WHILE @i <= @num_prescriptions
BEGIN
	-- N�hodn� datum mezi 1 rokem vzad a aktu�ln�m dnem
    DECLARE @random_date DATE = DATEADD(DAY, -(ABS(CHECKSUM(NEWID())) % 365), GETDATE());

    INSERT INTO Prescription (id_prescription, id_patient, id_doctor, id_drug, [date]) 
    VALUES (@i, (ABS(CHECKSUM(NEWID())) % @num_patients) + 1, 
                (ABS(CHECKSUM(NEWID())) % @num_doctors) + 1, 
                (ABS(CHECKSUM(NEWID())) % @num_drugs) + 1, 
                @random_date);
    SET @i = @i + 1;
END

/*
Vysv�tlen�:
1. Po�et ��dk�: Na za��tku skriptu m��ete zm�nit hodnoty pro @num_doctors, @num_drugs, @num_patients a @num_prescriptions, abyste ur�ili, kolik dat chcete m�t v ka�d� tabulce.
2. Generov�n� n�hodn�ch hodnot:
   Pro jm�na doktor� (name) se generuj� n�hodn� p�smena (nap��klad "Dr. AB").
	  NEWID() generuje unik�tn� identifik�tor, kter� je n�sledn� pou�it k vytvo�en� n�hodn�ho ��sla pomoc� funkce CHECKSUM().
      SELECT CHECKSUM(NEWID()) AS Nahodne_cislo
	  SELECT ABS(CHECKSUM(NEWID())) % 26 AS Nahodne_kladne_cislo_0_az_25 -- 26 je znak� abecedy
	  SELECT CHAR(65) AS Znak A
	  SELECT CHAR(65 + ABS(CHECKSUM(NEWID())) % 26) AS Nahodne_pismeno_abecedy
   Pro n�zvy l�k� (trademark_drug a generic_drug) se pou��vaj� hodnoty jako "Trademark 1", "Generic 1", atd.
   Pro pacienty se op�t pou��v� generov�n� jmen jako "Patient 1", "Patient 2", atd.
3. P�edpisy: Pro ka�d� p�edpis se n�hodn� vyb�r� pacient, doktor, l�k a datum. Sloupec date generuje n�hodn� datum mezi posledn�m rokem a dne�n�m datem. K tomu vyu��v�me funkci DATEADD a GETDATE(). Pomoc� funkce CHECKSUM(NEWID()) se generuj� n�hodn� ��sla (pomoc� modula�n� operace %, co� zajist�, �e se hodnoty pohybuj� v rozsahu odpov�daj�c�m existuj�c�m z�znam�m), kter� pak ur�uj�, kolik dn� se p�id� k aktu�ln�mu datu.
*/