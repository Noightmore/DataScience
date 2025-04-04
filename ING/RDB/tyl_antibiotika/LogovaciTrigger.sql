/*
sp_settriggerorder 'tr_VkladaniSoucastky', 'Last', 'INSERT'
*/

-- procedura, která vytvoøí tabulku Logovani
CREATE PROCEDURE mp_VytvorLogTabulku AS
BEGIN
	CREATE TABLE Logovani (
		id_log int PRIMARY KEY Identity,
		datum datetime,
		tabulka nvarchar(50),
		[trigger] nvarchar(50),
		akce nvarchar(50),
		[system_user] nvarchar(50),
		[current_user] nvarchar(50),
		[host_id] nvarchar(50),
		[host_name] nvarchar(50),
		[client_address] nvarchar(50),
		nove nvarchar(max),
		stare nvarchar(max)
	)
END
go

-- EXEC mp_vytvorlogtabulku
-- go

-- procedura, která zapíše do tabulky Logovani
CREATE PROCEDURE mp_Logovani 
@tabulka nvarchar(50),
@trigger nvarchar(50),
@akce nvarchar(50),
@client_address nvarchar(50),
@nove nvarchar(max),
@stare nvarchar(max)
AS
BEGIN
	IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID('[dbo].[Logovani]') AND type = 'U')
	BEGIN
		EXEC mp_VytvorLogTabulku
	END
	INSERT INTO Logovani (datum, tabulka, [trigger], akce, [system_user], [current_user], [host_id], [host_name], [client_address], nove, stare)
		VALUES (GETDATE(), @tabulka, @trigger, @akce, SYSTEM_USER, CURRENT_USER, HOST_ID(), HOST_NAME(), @client_address, @nove, @stare)
END
go

ALTER TRIGGER mt_LogSoucastka 
ON Soucastka 
AFTER INSERT, UPDATE, DELETE AS
BEGIN
	DECLARE @tabulka nvarchar(50)
	DECLARE @akce nvarchar(50)
	DECLARE @trigger nvarchar(50)
	DECLARE @client_address nvarchar(50)
	DECLARE @nove nvarchar(max) = NULL
	DECLARE @stare nvarchar(max) = NULL

	SET @tabulka = (SELECT SCHEMA_NAME(schema_id) + '.' + OBJECT_NAME(parent_object_id)
		FROM sys.objects 
		WHERE name = OBJECT_NAME(@@PROCID) AND SCHEMA_NAME(sys.objects.schema_id) = OBJECT_SCHEMA_NAME(@@PROCID))
	SET @akce = (SELECT CASE 
		WHEN EXISTS (SELECT 0 FROM inserted) AND EXISTS (SELECT 0 FROM deleted) THEN 'update'
		WHEN EXISTS (SELECT 0 FROM inserted) AND NOT EXISTS (SELECT 0 FROM deleted) THEN 'insert'
		ELSE 'delete'
		END)
	SET @trigger = (SELECT OBJECT_NAME(@@PROCID) AS trigger_name)
	SET @client_address = (SELECT CONVERT(nvarchar(50), CONNECTIONPROPERTY('client_net_address')))
	SET @nove = (SELECT * FROM inserted FOR JSON AUTO);
	SET @stare = (SELECT * FROM deleted FOR JSON AUTO);

	EXEC mp_Logovani @tabulka, @trigger, @akce, @client_address, @nove, @stare
END

-- testování triggeru
INSERT INTO [dbo].[Order] ([id_doctor], [id_drug], [count], [price]) VALUES (1, 1, 5, 100)
UPDATE [dbo].[Order] SET price = 200 WHERE id_drug = 2
DELETE FROM [dbo].[Order] WHERE id_drug = 2

SELECT * FROM [dbo].[Order] WHERE id_drug = 2

SELECT * FROM Logovani
DELETE FROM Logovani