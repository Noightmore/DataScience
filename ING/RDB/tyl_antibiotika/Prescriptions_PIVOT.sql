USE RDB2025_PavelTyl
go

/* Dokto?i a po?ty l?k? v jednotliv?ch m?s?c?ch (sloupce) */
/*
SELECT 
    P.id_doctor,
    COUNT(*) AS prescription_count
FROM Prescription P
WHERE P.[date] > DATEADD(MONTH, -1, GETDATE())
GROUP BY P.id_doctor;
go
*/

/*
DECLARE @MonthsBack INT = 6; -- Po?et m?s?c? zp?tn?
SELECT 
    P.id_doctor, 
    FORMAT(P.[date], 'yyyy-MM') AS Month,
    COUNT(*) AS PrescriptionCount
FROM Prescription P
WHERE P.[date] >= DATEADD(MONTH, -@MonthsBack+1, GETDATE()) -- Po??tek obdob? (dnes - N+1 m?s?c?)
GROUP BY P.id_doctor, FORMAT(P.[date], 'yyyy-MM')
ORDER BY P.id_doctor, FORMAT(P.[date], 'yyyy-MM');
go
*/

/*
-- Dynamick? generov?n? m?s?c?
DECLARE @MonthsBack INT = 6; -- Po?et m?s?c? zp?tn?
DECLARE @StartDate DATE = DATEADD(MONTH, -@MonthsBack+1, GETDATE()); -- Po??te?n? datum (N m?s?c? zp?tn?)
DECLARE @EndDate DATE = GETDATE(); -- Kone?n? datum (dne?n? datum)
DECLARE @DynamicSQL NVARCHAR(MAX);
DECLARE @ColumnList NVARCHAR(MAX);
-- Generov?n? seznamu m?s?c? mezi @StartDate a @EndDate
WITH MonthList AS (
    SELECT 
        FORMAT(DATEADD(MONTH, n, @StartDate), 'yyyy-MM') AS Month
    FROM (VALUES(0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12)) AS Numbers(n) -- tady to tedy je?t? nen? dynamicky
    WHERE DATEADD(MONTH, n, @StartDate) <= @EndDate
)
-- Seznam m?s?c? ve form?tu pro PIVOT
SELECT @ColumnList = STRING_AGG(QUOTENAME(Month), ', ') 
FROM MonthList;
-- Generov?n? dynamick?ho SQL pro PIVOT
SET @DynamicSQL = '
WITH DoctorPrescriptionData AS (
    SELECT 
        P.id_doctor, 
        FORMAT(P.[date], ''yyyy-MM'') AS Month,
        COUNT(*) AS PrescriptionCount
    FROM Prescription P
    WHERE P.[date] BETWEEN @StartDate AND @EndDate
    GROUP BY P.id_doctor, FORMAT(P.[date], ''yyyy-MM'')
)
-- PIVOTov?n? a spojen? m?s??n?ch ?daj? s doktory
SELECT 
    id_doctor,
    ' + @ColumnList + '
FROM DoctorPrescriptionData
PIVOT (
    MAX(PrescriptionCount)
    FOR Month IN (' + @ColumnList + ')
) AS PivotedData
ORDER BY id_doctor;
';
-- Spu?t?n? dynamick?ho SQL
EXEC sp_executesql @DynamicSQL, N'@StartDate DATE, @EndDate DATE', @StartDate, @EndDate;
*/

-- Dynamick? generov?n? m?s?c?
DECLARE @MonthsBack INT = 6; -- Po?et m?s?c? zp?tn?
DECLARE @StartDate DATE = DATEADD(MONTH, -@MonthsBack+1, GETDATE());  
DECLARE @EndDate DATE = GETDATE();
DECLARE @DynamicSQL NVARCHAR(MAX);
DECLARE @ColumnList NVARCHAR(MAX);
-- Dynamick? generov?n? seznamu m?s?c? pomoc? rekurzivn?ho CTE (Common Table Expression)
WITH MonthList AS (
    SELECT 0 AS n, FORMAT(@StartDate, 'yyyy-MM') AS Month
    UNION ALL
    SELECT n + 1, FORMAT(DATEADD(MONTH, n + 1, @StartDate), 'yyyy-MM') -- rekurzivn? ??st
    FROM MonthList
    WHERE DATEADD(MONTH, n + 1, @StartDate) <= @EndDate
)
SELECT @ColumnList = STRING_AGG(QUOTENAME(Month), ', ') 
FROM MonthList;
-- Generov?n? dynamick?ho SQL pro PIVOT
SET @DynamicSQL = '
WITH DoctorPrescriptionData AS (
    SELECT 
        D.[name] AS doctor_name,  
        FORMAT(P.[date], ''yyyy-MM'') AS Month,
        COUNT(*) AS PrescriptionCount
    FROM Prescription P JOIN Doctor D ON P.id_doctor = D.id_doctor 
    WHERE P.[date] BETWEEN @StartDate AND @EndDate
    GROUP BY D.[name], P.id_doctor, FORMAT(P.[date], ''yyyy-MM'')
)
-- PIVOTov?n? a spojen? m?s??n?ch ?daj? s doktory
SELECT 
    doctor_name,
    ' + @ColumnList + '
FROM DoctorPrescriptionData
PIVOT (
    MAX(PrescriptionCount)
    FOR Month IN (' + @ColumnList + ')
) AS PivotedData
ORDER BY doctor_name;
';
-- PRINT @DynamicSQL
-- Spu?t?n? SQL
EXEC sp_executesql @DynamicSQL, N'@StartDate DATE, @EndDate DATE', @StartDate, @EndDate;
go

-- ?lo by pou??t tabulku master.dbo.spt_values, 
-- je to rychlej??, ne? rekurze, ale nen? to tak obecn? ?e?en?, proto?e t?eba v Azure nemus? fungovat
-- SELECT number FROM master.dbo.spt_values WHERE type = 'P' and number BETWEEN 0 AND 3000 -- ??sla 0 a? 2047
/*
WITH MonthList AS (
    SELECT 
        FORMAT(DATEADD(MONTH, number, @StartDate), 'yyyy-MM') AS Month
    FROM master.dbo.spt_values
    WHERE type = 'P' AND number BETWEEN 0 AND DATEDIFF(MONTH, @StartDate, @EndDate)
)
SELECT @ColumnList = STRING_AGG(QUOTENAME(Month), ', ') 
FROM MonthList;
*/



/* Dokto?i a po?ty l?k? */
DECLARE @DynamicSQL NVARCHAR(MAX);  
DECLARE @ColumnList NVARCHAR(MAX);  
-- Generov?n? seznamu unik?tn?ch n?zv? l?k? pro PIVOT
SELECT @ColumnList = STRING_AGG(QUOTENAME(trademark_drug), ', ')  
FROM Drug;
-- Sestaven? dynamick?ho SQL s PIVOT podle l?k?
SET @DynamicSQL = '
WITH DoctorDrugData AS (
    SELECT 
        D.[name] AS doctor_name, 
        DR.trademark_drug AS drug_name,
        COUNT(*) AS PrescriptionCount
    FROM Prescription P
    JOIN Doctor D ON P.id_doctor = D.id_doctor
    JOIN Drug DR ON P.id_drug = DR.id_drug
    GROUP BY D.[name], DR.trademark_drug
)
-- PIVOT podle l?k?
SELECT 
    doctor_name,
    ' + @ColumnList + '
FROM DoctorDrugData
PIVOT (
    MAX(PrescriptionCount)
    FOR drug_name IN (' + @ColumnList + ')
) AS PivotedData
ORDER BY doctor_name;
';
-- Spu?t?n? SQL
EXEC sp_executesql @DynamicSQL;
go