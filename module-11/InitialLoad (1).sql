-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS outland_adventures;

-- Switch to the database
USE outland_adventures;


-- Drop all views first (to avoid dependency errors)
DROP VIEW IF EXISTS EquipmentProfitViewWithRentals;
DROP VIEW IF EXISTS EquipmentAgeAndInventoryStatus;

-- Drop all tables (reverse dependency order)
DROP TABLE IF EXISTS Waiver;
DROP TABLE IF EXISTS EquipmentTransaction;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS TwoFactorMethod;
DROP TABLE IF EXISTS FamilyMember;
DROP TABLE IF EXISTS Equipment;
DROP TABLE IF EXISTS Trip;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS CustomerAccount;


-- =========================
-- Table: CustomerAccount
-- =========================
CREATE TABLE CustomerAccount (
  AccountID INT AUTO_INCREMENT PRIMARY KEY,
  AccountName VARCHAR(100),
  PrimaryContactName VARCHAR(100),
  Email VARCHAR(100) UNIQUE,
  Phone VARCHAR(20),
  Username VARCHAR(50) UNIQUE,
  PasswordHash VARCHAR(255),
  AccountStatus VARCHAR(20), -- e.g. Active, Suspended, Closed
  TwoFactorEnabled BOOLEAN DEFAULT FALSE
);

INSERT INTO CustomerAccount (AccountName, PrimaryContactName, Email, Phone, Username, PasswordHash, AccountStatus, TwoFactorEnabled)
VALUES
('Smith Family','John Smith','smith@example.com','555-1111','smithfam','hash1','Active',TRUE),
('Johnson Family','Mary Johnson','johnson@example.com','555-2222','johnsonfam','hash2','Active',FALSE),
('Williams Family','Robert Williams','williams@example.com','555-3333','williamsfam','hash3','Active',TRUE),
('Brown Family','Linda Brown','brown@example.com','555-4444','brownfam','hash4','Suspended',FALSE),
('Jones Family','Michael Jones','jones@example.com','555-5555','jonesfam','hash5','Active',TRUE),
('Garcia Family','Maria Garcia','garcia@example.com','555-6666','garciafam','hash6','Active',FALSE),
('Miller Family','David Miller','miller@example.com','555-7777','millerfam','hash7','Closed',FALSE),
('Davis Family','Susan Davis','davis@example.com','555-8888','davisfam','hash8','Active',TRUE),
('Rodriguez Family','James Rodriguez','rodriguez@example.com','555-9999','rodriguezfam','hash9','Active',FALSE),
('Martinez Family','Patricia Martinez','martinez@example.com','555-0000','martinezfam','hash10','Active',TRUE);


-- =========================
-- Table: FamilyMember
-- =========================
CREATE TABLE FamilyMember (
  MemberID INT AUTO_INCREMENT PRIMARY KEY,
  AccountID INT,
  Name VARCHAR(100),
  Age INT,
  Relationship VARCHAR(50), -- e.g. Parent, Child
  FOREIGN KEY (AccountID) REFERENCES CustomerAccount(AccountID)
);


INSERT INTO FamilyMember (AccountID, Name, Age, Relationship)
VALUES
(1,'John Smith',40,'Parent'),
(1,'Jane Smith',38,'Parent'),
(1,'Tom Smith',12,'Child'),
(2,'Mary Johnson',42,'Parent'),
(2,'Sam Johnson',15,'Child'),
(2,'Ella Johnson',10,'Child'),
(3,'Robert Williams',45,'Parent'),
(3,'Lucy Williams',43,'Parent'),
(3,'Anna Williams',17,'Child'),
(4,'Linda Brown',39,'Parent');

-- =========================
-- Table: Waiver
-- =========================
CREATE TABLE Waiver (
  WaiverID INT AUTO_INCREMENT PRIMARY KEY,
  MemberID INT,
  SignedByMember BOOLEAN,
  SignedByParent BOOLEAN,
  ParentMemberID INT,
  DateSigned DATE,
  FOREIGN KEY (MemberID) REFERENCES FamilyMember(MemberID),
  FOREIGN KEY (ParentMemberID) REFERENCES FamilyMember(MemberID)
);

INSERT INTO Waiver (MemberID, SignedByMember, SignedByParent, ParentMemberID, DateSigned)
VALUES
(1,TRUE,FALSE,NULL,'2025-01-01'),
(2,TRUE,FALSE,NULL,'2025-01-01'),
(3,FALSE,TRUE,1,'2025-01-02'),
(4,TRUE,FALSE,NULL,'2025-01-03'),
(5,FALSE,TRUE,4,'2025-01-03'),
(6,FALSE,TRUE,4,'2025-01-03'),
(7,TRUE,FALSE,NULL,'2025-01-04'),
(8,TRUE,FALSE,NULL,'2025-01-04'),
(9,FALSE,TRUE,7,'2025-01-05'),
(10,TRUE,FALSE,NULL,'2025-01-06');

-- =========================
-- Table: Trip
-- =========================
CREATE TABLE Trip (
  TripID INT AUTO_INCREMENT PRIMARY KEY,
  Destination VARCHAR(100),
  Region VARCHAR(50), -- e.g. Africa, Asia, Southern Europe
  StartDate DATE,
  EndDate DATE,
  Price DECIMAL(10,2),
  SuggestedMaxParticipants INT
);

INSERT INTO Trip (Destination, Region, StartDate, EndDate, Price, SuggestedMaxParticipants)
VALUES
('Kilimanjaro Trek','Africa','2025-02-01','2025-02-10',2500.00,12),
('Safari Adventure','Africa','2025-03-01','2025-03-07',1800.00,20),
('Everest Base Camp','Asia','2025-04-01','2025-04-15',3000.00,15),
('Annapurna Circuit','Asia','2025-05-01','2025-05-14',2800.00,12),
('Alps Hiking','Southern Europe','2025-06-01','2025-06-07',1500.00,10),
('Pyrenees Trek','Southern Europe','2025-07-01','2025-07-10',1600.00,10),
('Sahara Desert Trek','Africa','2025-08-01','2025-08-05',1200.00,8),
('Great Wall Hike','Asia','2025-09-01','2025-09-07',2000.00,20),
('Dolomites Adventure','Southern Europe','2025-10-01','2025-10-08',1700.00,12),
('Atlas Mountains','Africa','2025-11-01','2025-11-09',1900.00,15);

-- =========================
-- Table: Booking
-- =========================
CREATE TABLE Booking (
  BookingID INT AUTO_INCREMENT PRIMARY KEY,
  AccountID INT,
  TripID INT,
  BookingDate DATE,
  Status VARCHAR(20), -- e.g. Confirmed, Cancelled, Pending
  NumberOfParticipants INT,
  FOREIGN KEY (AccountID) REFERENCES CustomerAccount(AccountID),
  FOREIGN KEY (TripID) REFERENCES Trip(TripID)
);


INSERT INTO Booking (AccountID, TripID, BookingDate, Status, NumberOfParticipants)
VALUES
(1,1,'2025-01-15','Confirmed',3),
(2,2,'2025-01-20','Confirmed',4),
(3,3,'2025-02-01','Pending',2),
(4,4,'2025-02-10','Cancelled',1),
(5,5,'2025-03-01','Confirmed',2),
(6,6,'2025-03-15','Confirmed',3),
(7,7,'2025-04-01','Pending',2),
(8,8,'2025-04-20','Confirmed',4),
(9,9,'2025-05-01','Confirmed',2),
(10,10,'2025-05-15','Pending',1);

-- Table: Equipment
-- =========================
CREATE TABLE Equipment (
  EquipmentID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100),
  Category VARCHAR(50),        -- e.g. Tent, Backpack, Sleeping Bag
  PurchaseDate DATE,
  EquipCondition VARCHAR(50),  -- e.g. New, Good, Worn
  AvailableQuantity INT,
  InitialCost DECIMAL(10,2),   -- acquisition cost
  SalePrice DECIMAL(10,2),     -- selling price
  RentalPrice DECIMAL(10,2)    -- rental fee
);

-- =========================
-- Sample Data Inserts
-- =========================
INSERT INTO Equipment (Name, Category, PurchaseDate, EquipCondition, AvailableQuantity, InitialCost, SalePrice, RentalPrice)
VALUES
('Tent A','Tent','2020-01-01','Good',5,200.00,300.00,25.00),
('Tent B','Tent','2019-05-01','Worn',3,150.00,220.00,20.00),
('Backpack A','Backpack','2021-03-01','New',10,80.00,120.00,10.00),
('Sleeping Bag A','Sleeping Bag','2018-07-01','Worn',2,60.00,90.00,8.00),
('Sleeping Bag B','Sleeping Bag','2022-01-01','New',8,70.00,100.00,9.00),
('Stove A','Cooking','2020-09-01','Good',4,50.00,75.00,6.00),
('Lantern A','Lighting','2019-11-01','Good',6,40.00,60.00,5.00),
('Lantern B','Lighting','2021-02-01','New',7,45.00,70.00,6.00),
('Boots A','Footwear','2022-05-01','New',12,90.00,130.00,12.00),
('Boots B','Footwear','2017-06-01','Worn',1,70.00,100.00,10.00);


-- =========================
-- Table: EquipmentTransaction
-- =========================
CREATE TABLE EquipmentTransaction (
  TransactionID INT AUTO_INCREMENT PRIMARY KEY,
  AccountID INT,
  EquipmentID INT,
  TransactionType VARCHAR(20), -- e.g. Rental, Purchase
  TransactionDate DATE,
  Quantity INT,
  MemberID INT,
  FOREIGN KEY (AccountID) REFERENCES CustomerAccount(AccountID),
  FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID),
  FOREIGN KEY (MemberID) REFERENCES FamilyMember(MemberID)
);

INSERT INTO EquipmentTransaction (AccountID, EquipmentID, TransactionType, TransactionDate, Quantity, MemberID)
VALUES
(1,1,'Rental','2025-01-10',1,3),
(2,2,'Purchase','2025-01-12',1,5),
(3,3,'Rental','2025-01-15',2,9),
(4,4,'Rental','2025-01-18',1,10),
(5,5,'Purchase','2025-01-20',2,5),
(6,6,'Rental','2025-01-22',1,6),
(7,7,'Rental','2025-01-25',2,7),
(8,8,'Purchase','2025-01-28',1,8),
(9,9,'Rental','2025-02-01',2,9),
(10,10,'Purchase','2025-02-03',1,10),
(1,3,'Purchase','2025-02-05',1,2),
(2,4,'Rental','2025-02-07',1,4),
(3,2,'Rental','2025-02-09',2,9),
(4,1,'Purchase','2025-02-11',1,10);

-- =========================
-- Table: TwoFactorMethod
-- =========================
CREATE TABLE TwoFactorMethod (
  MethodID INT AUTO_INCREMENT PRIMARY KEY,
  AccountID INT,
  MethodType VARCHAR(50), -- e.g. SMS, Email, AuthenticatorApp
  Destination VARCHAR(100),
  IsPrimary BOOLEAN,
  DateEnabled DATE,
  FOREIGN KEY (AccountID) REFERENCES CustomerAccount(AccountID)
);


INSERT INTO TwoFactorMethod (AccountID, MethodType, Destination, IsPrimary, DateEnabled)
VALUES
(1,'SMS','555-1111',TRUE,'2025-01-01'),
(1,'Email','smith@example.com',FALSE,'2025-01-02'),
(2,'AuthenticatorApp','smithfam-app',TRUE,'2025-01-05'),
(3,'SMS','555-3333',TRUE,'2025-01-10'),
(3,'Email','williams@example.com',FALSE,'2025-01-11'),
(5,'SMS','555-5555',TRUE,'2025-01-15'),
(6,'Email','garcia@example.com',TRUE,'2025-01-20'),
(7,'AuthenticatorApp','millerfam-app',TRUE,'2025-01-25'),
(8,'SMS','555-8888',TRUE,'2025-01-30'),
(10,'Email','martinez@example.com',TRUE,'2025-02-01');

-- =========================
-- Table: Staff
-- =========================
CREATE TABLE Staff (
  StaffID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100),
  Role VARCHAR(50), -- e.g. Guide, Marketing, Inventory, Developer, Admin
  Responsibilities TEXT
);


-- Staff table sample data based on original ERD case study
INSERT INTO Staff (Name, Role, Responsibilities)
VALUES
('John MacNell','Guide','Organizes and leads treks, handles logistics like airfare, visas, and inoculations'),
('D.B. Duke Marland','Guide','Plans and guides trips, ensures safety and compliance with travel requirements'),
('Anita Gallegos','Marketing','Develops advertising campaigns, manages promotions and customer outreach'),
('Dimitrios Stravopolous','Inventory','Orders supplies, manages equipment inventory, tracks rentals and purchases'),
('Mei Wong','Developer','Builds and maintains the e-commerce site for trip schedules and equipment sales'),
('Blythe Timmerson','Admin','Handles office operations and overall administration of Outland Adventures'),
('Jim Ford','Admin','Handles office operations and overall administration of Outland Adventures');

-- Granting user account permissions to outland_adventures staff members
/* GRANT SELECT, INSERT, UPDATE, DELETE ON outland_adventures.* TO 'john.macneil@outlandadventures.com';
GRANT SELECT, INSERT, UPDATE, DELETE ON outland_adventures.* TO 'db.marland@outlandadventures.com';
GRANT SELECT, INSERT, UPDATE, DELETE ON outland_adventures.* TO 'anita.gallegos@outlandadventures.com';
GRANT SELECT, INSERT, UPDATE, DELETE ON outland_adventures.* TO 'dimitrios.stravopolous@outlandadventures.com';
GRANT SELECT, INSERT, UPDATE, DELETE ON outland_adventures.* TO 'mei.wong@outlandadventures.com';
GRANT SELECT, INSERT, UPDATE, DELETE ON outland_adventures.* TO 'blythe.timmerson@outlandadventures.com';
GRANT SELECT, INSERT, UPDATE, DELETE ON outland_adventures.* TO 'jim.ford@outlandadventures.com'; */

-- View: EquipmentProfitViewWithRentals
-- Combines equipment financials with actual rental revenue from transactions
CREATE VIEW EquipmentProfitViewWithRentals AS
SELECT
    e.EquipmentID,
    e.Name,
    e.Category,
    e.InitialCost,
    e.SalePrice,
    e.RentalPrice,
    (e.SalePrice - e.InitialCost) AS SaleProfit,
    ROUND((e.RentalPrice / e.InitialCost) * 100, 2) AS RentalROI_Percent,
    COALESCE(SUM(CASE WHEN t.TransactionType = 'Rental' 
                      THEN t.Quantity * e.RentalPrice ELSE 0 END),0) AS TotalRentalRevenue,
    COALESCE(SUM(CASE WHEN t.TransactionType = 'Rental' 
                      THEN t.Quantity ELSE 0 END),0) AS TotalRentalCount
FROM Equipment e
LEFT JOIN EquipmentTransaction t ON e.EquipmentID = t.EquipmentID
GROUP BY e.EquipmentID, e.Name, e.Category, e.InitialCost, e.SalePrice, e.RentalPrice;

-- ============================================
-- View: EquipmentAgeAndInventoryStatus
-- ============================================
CREATE VIEW EquipmentAgeAndInventoryStatus AS
SELECT
    EquipmentID,
    Name,
    Category,
    EquipCondition AS EquipCondition,
    AvailableQuantity AS InventoryLevel,
    PurchaseDate,
    DATEDIFF(CURDATE(), PurchaseDate) AS DaysSincePurchase,
    TIMESTAMPDIFF(YEAR, PurchaseDate, CURDATE()) AS YearsSincePurchase,
    CASE
        WHEN TIMESTAMPDIFF(YEAR, PurchaseDate, CURDATE()) >= 5 THEN 'Over 5 Years Old'
        ELSE 'Under 5 Years Old'
    END AS AgeStatus
FROM
    Equipment;