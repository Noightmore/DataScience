USE RDB2025_PavelTyl
GO

CREATE TABLE Doctor (
    id_doctor int  NOT NULL,
    [name] nvarchar(20)  NOT NULL,
    CONSTRAINT Doctor_pk PRIMARY KEY  (id_doctor)
);

-- Table: Drug
CREATE TABLE Drug (
    id_drug int  NOT NULL,
    trademark_drug nvarchar(20)  NOT NULL,
    generic_drug nvarchar(20)  NOT NULL,
    CONSTRAINT Drug_pk PRIMARY KEY  (id_drug)
);

-- Table: Patient
CREATE TABLE Patient (
    id_patient int  NOT NULL,
    [name] nvarchar(20)  NOT NULL,
    CONSTRAINT Patient_pk PRIMARY KEY  (id_patient)
);

-- Table: Prescription
CREATE TABLE Prescription (
    id_prescription int  NOT NULL,
    id_patient int  NOT NULL,
    id_doctor int  NOT NULL,
    id_drug int  NOT NULL,
	[date] datetime NOT NULL,
    CONSTRAINT Prescription_pk PRIMARY KEY  (id_prescription)
);

-- foreign keys
-- Reference: Prescription_Doctor (table: Prescription)
ALTER TABLE Prescription ADD CONSTRAINT Prescription_Doctor
    FOREIGN KEY (id_doctor)
    REFERENCES Doctor (id_doctor);

-- Reference: Prescription_Drug (table: Prescription)
ALTER TABLE Prescription ADD CONSTRAINT Prescription_Drug
    FOREIGN KEY (id_drug)
    REFERENCES Drug (id_drug);

-- Reference: Prescription_Patient (table: Prescription)
ALTER TABLE Prescription ADD CONSTRAINT Prescription_Patient
    FOREIGN KEY (id_patient)
    REFERENCES Patient (id_patient);