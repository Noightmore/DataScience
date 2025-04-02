ALTER TABLE Drug ADD price INT
-- ALTER TABLE Drug DROP COLUMN price

UPDATE Drug SET price = 10 + ABS(CHECKSUM(NEWID())) % 91

-- UPDATE Drug SET price = 10 + CAST(RAND(CHECKSUM(NEWID())) * 91 AS INT) -- asi horší øešení

CREATE TABLE [Order] (
	id_doctor int NOT NULL,
	id_drug int NOT NULL,
	id_order int NOT NULL PRIMARY KEY IDENTITY(1, 1),
	[count] int NOT NULL,
	price money NULL,
	CONSTRAINT FK_Drug FOREIGN KEY (id_drug) REFERENCES Drug(id_drug),
	CONSTRAINT FK_Doctor FOREIGN KEY (id_doctor) REFERENCES Doctor(id_doctor)
)

INSERT INTO [Order] (id_doctor, id_drug, [count], price) VALUES (1, 4, 10, NULL), (1, 3, 10, NULL)
go

CREATE TRIGGER tr_VypocetCenyAFTER
ON [Order]
AFTER INSERT
AS
BEGIN
	SET NOCOUNT ON;
	UPDATE [Order] SET [Order].price = (
		SELECT Drug.price * inserted.[count] 
		FROM Drug INNER JOIN inserted ON Drug.id_drug = inserted.id_drug 
			AND inserted.id_order = [Order].id_order
	) WHERE [Order].price IS NULL
END
go

CREATE TRIGGER tr_VypocetCenyINSTEADOF
ON [Order]
INSTEAD OF INSERT
AS
BEGIN
	SET NOCOUNT ON;
	INSERT INTO [Order] (id_doctor, id_drug, [count], price)
	SELECT id_doctor, inserted.id_drug, [count], (
		SELECT price FROM Drug WHERE id_drug = inserted.id_drug
	) * [count] FROM inserted 
END
go

CREATE PROCEDURE sp_VyberLekuPod20
AS
SELECT * FROM Drug WHERE price < 20
go

CREATE VIEW uv_VyberLekuPod20
AS
SELECT * FROM Drug WHERE price < 20
go

EXECUTE sp_VyberLekuPod20

SELECT * FROM uv_VyberLekuPod20 ORDER BY price
go

CREATE PROCEDURE sp_VyberLekuPodCenu
@cena money,
@pocet int
AS
SELECT TOP (@pocet) * FROM Drug WHERE price < @cena
go

EXEC sp_VyberLekuPodCenu @cena = 50, @pocet = 5
go