USE RDB2025_PavelTyl
GO

-- Docto?i
INSERT INTO Doctor (id_doctor, name) 
VALUES 
(1, 'Dr. Nov?k'),
(2, 'Dr. ?ern?'),
(3, 'Dr. Mal?');

-- L?ky
INSERT INTO Drug (id_drug, trademark_drug, generic_drug) 
VALUES 
(1, 'Paralen', 'Paracetamol'),
(2, 'Aspirin', 'Acetylsalicylov? kyselina'),
(3, 'Ibuprofen', 'Ibuprofen'),
(4, 'Mucosolvan', 'Ambroxol');

-- Pacienti
INSERT INTO Patient (id_patient, name) 
VALUES 
(1, 'Jan Novotn?'),
(2, 'Eva Dvo??kov?'),
(3, 'Petr Svoboda'),
(4, 'Martina Pol?kov?');

-- Recepty
INSERT INTO Prescription (id_prescription, id_patient, id_doctor, id_drug) 
VALUES 
(1, 1, 1, 1),  -- Jan Novotn?, Dr. Nov?k, Paralen
(2, 1, 2, 2),  -- Jan Novotn?, Dr. ?ern?, Aspirin
(3, 2, 3, 3),  -- Eva Dvo??kov?, Dr. Mal?, Ibuprofen
(4, 3, 1, 4),  -- Petr Svoboda, Dr. Nov?k, Mucosolvan
(5, 4, 2, 1);  -- Martina Pol?kov?, Dr. ?ern?, Paralen