-- ============================================================
-- VETRI IT JOB PORTAL ANALYTICS
-- SQL BUSINESS ANALYSIS
-- ============================================================
-- Database: Vetri_IT_Job_Portal_Analysis
-- Main table: jobs
-- Skills table: skills_data
--
-- Project Phase: Data Analytics
-- Purpose: Answer the six required business questions
-- ============================================================


-- ============================================================
-- 0. DATABASE SELECTION
-- ============================================================

CREATE DATABASE Vetri_IT_Job_Portal_Analysis;

USE Vetri_IT_Job_Portal_Analysis;

SELECT DATABASE();

-- ============================================================
-- 0.1 JOBS TABLE CREATION
-- ============================================================

CREATE TABLE jobs (
    Job_ID BIGINT,
    Job_Title VARCHAR(255),
    Company_Name VARCHAR(255),
    Industry VARCHAR(150),
    Location VARCHAR(255),
    City VARCHAR(100),
    IT_Job_Category VARCHAR(100),
    Salary_Range VARCHAR(100),
    Salary_Min DECIMAL(12,2),
    Salary_Max DECIMAL(12,2),
    Salary_Average DECIMAL(12,2),
    Salary_Available VARCHAR(20),
    Experience_Category VARCHAR(100),
    Seniority_Level VARCHAR(100),
    Job_Function VARCHAR(150),
    Job_Type VARCHAR(100),
    Work_Mode VARCHAR(100),
    Skills_Required TEXT,
    Education_Required VARCHAR(150),
    Posted_Date DATE,
    Posted_Time VARCHAR(50),
    Number_of_Applicants INT,
    Job_Summary TEXT,
    Job_Description TEXT,
    Job_URL TEXT,
    Apply_Link TEXT,
    Company_ID VARCHAR(100),
    Company_URL TEXT,
    Application_Availability VARCHAR(50),
    Easy_Apply VARCHAR(20)
);

SHOW TABLES;

DESCRIBE jobs;

-- ============================================================
-- 0.2 IMPORTING THE JOBS TABLE DATA TO WORKBENCH
-- ============================================================

SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE 'D:/New folder/LinkedIn_IT_Job_Analysis/05_SQL/Jobs_SQL.csv'
INTO TABLE jobs
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT COUNT(*) AS Total_Jobs
FROM jobs;

SELECT COUNT(DISTINCT Job_ID) AS Unique_Job_IDs
FROM jobs;

-- ============================================================
-- 0.3 SKILLS_DATA TABLE CREATION
-- ============================================================

CREATE TABLE skills_data (
    Skills VARCHAR(150),
    Skills_Count INT
);

-- ============================================================
-- 0.4 IMPORTING SKILLS_DATA TO WORKBENCH
-- ============================================================

LOAD DATA LOCAL INFILE 'D:/New folder/LinkedIn_IT_Job_Analysis/05_SQL/Skills_Data.csv'
INTO TABLE skills_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT COUNT(*) AS Total_Skill_Records
FROM skills_data;

-- ============================================================
-- 1. HIGHEST-DEMAND JOB ROLES
-- Business Question:
-- Which job roles are in highest demand?
-- ============================================================

SELECT
    Job_Title,
    COUNT(*) AS Job_Count
FROM jobs
GROUP BY Job_Title
ORDER BY Job_Count DESC
LIMIT 10;


-- ============================================================
-- 2. TOP HIRING LOCATIONS
-- Business Question:
-- Which locations have the most job openings?
-- ============================================================

SELECT
    City,
    COUNT(*) AS Job_Count
FROM jobs
GROUP BY City
ORDER BY Job_Count DESC
LIMIT 10;


-- ============================================================
-- 3. MOST REQUESTED SKILLS
-- Business Question:
-- Which skills are most requested?
--
-- Note:
-- Skills_Count is already calculated in the skills_data table,
-- so COUNT() is not applied again.
-- ============================================================

SELECT
    Skills,
    Skills_Count
FROM skills_data
ORDER BY Skills_Count DESC
LIMIT 10;


-- ============================================================
-- 4. INDUSTRIES HIRING THE MOST
-- Business Question:
-- Which industries are hiring the most?
-- ============================================================

SELECT
    Industry,
    COUNT(*) AS Job_Count
FROM jobs
GROUP BY Industry
ORDER BY Job_Count DESC;


-- ============================================================
-- 5. SALARY RANGES BY JOB ROLE
-- Business Question:
-- What salary ranges are offered for different roles?
--
-- Only jobs where salary is available are included.
-- ============================================================

SELECT
    Job_Title,
    COUNT(*) AS Jobs_With_Salary,
    ROUND(AVG(Salary_Min), 2) AS Avg_Salary_Min,
    ROUND(AVG(Salary_Max), 2) AS Avg_Salary_Max,
    ROUND(AVG(Salary_Average), 2) AS Avg_Salary
FROM jobs
WHERE Salary_Available = 'Yes'
GROUP BY Job_Title
ORDER BY Avg_Salary DESC;


-- ============================================================
-- 6. PREFERRED EXPERIENCE LEVELS
-- Business Question:
-- What experience levels are most preferred?
-- ============================================================

SELECT
    Experience_Category,
    COUNT(*) AS Job_Count
FROM jobs
GROUP BY Experience_Category
ORDER BY Job_Count DESC;


-- ============================================================
-- END OF SQL BUSINESS ANALYSIS
-- ============================================================
