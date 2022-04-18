DROP DATABASE IF EXISTS Accounting_education;
CREATE DATABASE Accounting_education;
USE Accounting_education;


-- 1. Создаю таблицу Сотрудники (Staff): 

CREATE TABLE Staff (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    lastname VARCHAR(128) NOT NULL,
    firstname VARCHAR(128) NOT NULL,
    patronymic VARCHAR(128) NOT NULL,
    birthday DATE NOT NULL,
    is_deleted bit DEFAULT 0 -- сотрудников из таблицы не удаляем, а только помечаем на удаление (присваиваем 1)
);

-- 2. Создаю таблицу Учебные заведения (EducationalEstablishments): 

CREATE TABLE EducationalEstablishments (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    establishment_name VARCHAR(255) NOT NULL
);

-- 3. Создаю таблицу Сотрудники_Учебные Заведения (Staff_EducationalEstablishments): 

CREATE TABLE Staff_EducationalEstablishments (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Staff_id INT UNSIGNED NOT NULL,
    EducationalEstablishments_id INT UNSIGNED NOT NULL,
    graduation_year INT NOT NULL, 
    
	FOREIGN KEY (Staff_id) REFERENCES Staff(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (EducationalEstablishments_id) REFERENCES EducationalEstablishments(id) ON DELETE RESTRICT ON UPDATE RESTRICT
);


INSERT INTO Staff(id, lastname, firstname, patronymic, birthday, is_deleted) VALUES
	(1, "Петров", "Олег", "Иванович", '2000-12-12', 0),
	(2, "Сидоров", "Михаил", "Дмитриевич", '1995-01-05', 0),
	(3, "Иванов", "Иван", "Иванович", '1985-11-11', 0),
	(4, "Иванов", "Александр", "Иванович", '1985-11-11', 0);
	
SELECT lastname, firstname, patronymic FROM staff 
WHERE lastname = "Иванов";



SELECT 
	lastname, 
	firstname, 
	patronymic,
	TIMESTAMPDIFF(YEAR, birthday, NOW()) as age
FROM staff 
WHERE TIMESTAMPDIFF(YEAR, birthday, NOW()) < 30;

SELECT COUNT(*) FROM staff 
WHERE lastname = "Иванов";

SELECT 
	DISTINCT birthday
FROM staff;














