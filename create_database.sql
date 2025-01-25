DROP DATABASE IF EXISTS theoswaters;
CREATE DATABASE theoswaters;
USE theoswaters;


CREATE TABLE IF NOT EXISTS merchants (
	username VARCHAR(200) PRIMARY KEY,
    password VARCHAR(100)
);

INSERT INTO merchants (username, password)
VALUES
  ('john_doe', 'P@ssw0rd1'),
  ('mary_smith', 'C0mpl3xP@ss'),
  ('tom_jones', 'S3cur3P@$$'),
  ('linda_brown', 'Str0ngP@ssw0rd'),
  ('michael_clark', 'P@$$w0rd!'),
  ('sarah_white', 'C0mpl1c@ted!'),
  ('david_harris', 'S3cur1tyRul3s'),
  ('jennifer_thomas', 'P@ssw0rd123'),
  ('robert_green', 'ComplexP@$$'),
  ('emily_miller', 'S@f3P@ssw0rd'),
  ('james_wilson', 'P@$$w0rd!123'),
  ('jessica_jackson', 'S3cur3P@ssw0rd'),
  ('william_taylor', 'Str0ngP@$$w0rd'),
  ('olivia_martin', 'P@ssw0rd123!'),
  ('charles_brown', 'C0mpl1c@t3dP@$$'),
  ('adam_smith', 'P@ssw0rd!456'),
  ('samantha_davis', 'C0mp1exP@ssw0rd'),
  ('matthew_miller', 'S3cur3P@ss123'),
  ('olivia_wilson', 'Str0ngP@$$456'),
  ('daniel_taylor', 'P@$$w0rd789!'),
  ('ava_johnson', 'C0mpl1c@tedP@$$'),
  ('jacob_anderson', 'S@f3P@ss!789'),
  ('emma_martin', 'P@$$w0rd!789'),
  ('liam_thompson', 'S3cur3P@$$123'),
  ('olivia_williams', 'Str0ngP@$$w0rd!'),
  ('william_wilson', 'P@ssw0rd!123'),
  ('isabella_davis', 'C0mpl3xP@$$789'),
  ('james_smith', 'S@f3P@ss!123'),
  ('sophia_brown', 'P@$$w0rd!789'),
  ('mason_thomas', 'S3cur3P@$$456'),
  ('avamax_johnson', 'Str0ngP@$$!123'),
  ('logan_walker', 'P@ssw0rd789!'),
  ('mia_martinez', 'C0mpl1c@tedP@$$'),
  ('benjamin_martin', 'S@f3P@ssw0rd!'),
  ('amelia_rodriguez', 'P@$$w0rd!123'),
  ('williamx_taylor', 'C0mpl3xP@$$!789'),
  ('harper_anderson', 'S@f3P@ssw0rd!'),
  ('samuel_davis', 'P@$$w0rd789!'),
  ('abigail_thompson', 'C0mpl1c@tedP@$$'),
  ('henry_clark', 'S3cur3P@$$123'),
  ('olivia_white', 'Str0ngP@$$w0rd!');

CREATE TABLE abigail_thompson_customers (
  `Serial NO` INT AUTO_INCREMENT PRIMARY KEY,
  `Full name` VARCHAR(50),
  `Address` VARCHAR(100),
  `Contact NO` VARCHAR(20),
  `Date Encoded` DATE
);

INSERT INTO abigail_thompson_customers (`Full name`, `Address`, `Contact NO`, `Date Encoded`)
VALUES
  ('John Doe', '123 Main St, CityA', '1234567890', '2023-05-01'),
  ('Jane Smith', '456 Elm St, CityB', '9876543210', '2023-05-02'),
  ('Michael Johnson', '789 Oak St, CityC', '4561237890', '2023-05-03'),
  ('Sarah Williams', '321 Pine St, CityD', '7894561230', '2023-05-04'),
  ('Robert Brown', '654 Maple St, CityE', '3216549870', '2023-05-05'),
  ('Emily Davis', '987 Cedar St, CityF', '6547893210', '2023-05-06'),
  ('Daniel Miller', '159 Birch St, CityG', '9873216540', '2023-05-07'),
  ('Olivia Wilson', '753 Walnut St, CityH', '1237894560', '2023-05-08'),
  ('Matthew Anderson', '357 Sycamore St, CityI', '4569873210', '2023-05-09'),
  ('Sophia Taylor', '951 Oakwood St, CityJ', '7891234560', '2023-05-10'),
  ('David Thomas', '753 Elmwood St, CityK', '1234569870', '2023-05-11'),
  ('Isabella Martinez', '456 Pinecrest St, CityL', '9873214560', '2023-05-12'),
  ('Joseph Davis', '159 Maplewood St, CityM', '6547891230', '2023-05-13'),
  ('Ava Garcia', '753 Willow St, CityN', '3214569870', '2023-05-14'),
  ('Andrew Rodriguez', '357 Cedarwood St, CityO', '7891236540', '2023-05-15'),
  ('Mia Hernandez', '951 Birchwood St, CityP', '1237893210', '2023-05-16'),
  ('William Wilson', '753 Walnutwood St, CityQ', '4569871230', '2023-05-17'),
  ('Abigail Thompson', '456 Oakcrest St, CityR', '9873217890', '2023-05-18'),
  ('Samantha Clark', '159 Pinehurst St, CityS', '6547894560', '2023-05-19'),
  ('Benjamin Lewis', '753 Maplehurst St, CityT', '3214567890', '2023-05-20');

CREATE TABLE IF NOT EXISTS abigail_thompson_bottles (
	`NO` INT AUTO_INCREMENT PRIMARY KEY,
    `Bottle size` INT,
    `Measurement unit` VARCHAR(100),
    `Cost` DECIMAL(10, 2)
);

INSERT INTO abigail_thompson_bottles (`Bottle size`, `Measurement unit`, `Cost`) 
VALUES
	(10, "Liters", 5),
  (20, "Liters", 10),
  (30, "Liters", 10),
  (40, "Liters", 20),
  (60, "Liters", 50),
  (20, "Liters", 10),
  (20, "Liters", 10),
  (20, "Liters", 10),
  (100, "Liters", 80);
  
