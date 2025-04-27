-- ----------------------------------------
-- Create Database
-- ----------------------------------------

CREATE DATABASE eReserveData;
GO

-- ----------------------------------------
-- Use Database
-- ----------------------------------------

USE eReserveData;
GO

-- ----------------------------------------
-- Table: School
-- ----------------------------------------

CREATE TABLE School (
    ereserve_id INT PRIMARY KEY NOT NULL,
    name NVARCHAR(255) NOT NULL
);
GO

-- ----------------------------------------
-- Table: Unit
-- ----------------------------------------

CREATE TABLE Unit (
    ereserve_id INT PRIMARY KEY NOT NULL,
    code NVARCHAR(50) NOT NULL,
    name NVARCHAR(255) NOT NULL
);
GO

-- ----------------------------------------
-- Table: TeachingSession
-- ----------------------------------------

CREATE TABLE TeachingSession (
    ereserve_id INT PRIMARY KEY NOT NULL,
    name NVARCHAR(255),
    start_date DATE,
    end_date DATE,
    archived BIT DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME
);
GO

-- ----------------------------------------
-- Table: Reading
-- ----------------------------------------

CREATE TABLE Reading (
    ereserve_id INT PRIMARY KEY NOT NULL,
    reading_title NVARCHAR(100),
    genre NVARCHAR(100),
    source_document_title NVARCHAR(100),
    article_number NVARCHAR(100),
    created_at DATETIME,
    updated_at DATETIME
);
GO

-- ----------------------------------------
-- Table: ReadingList
-- ----------------------------------------

CREATE TABLE ReadingList (
    ereserve_id INT PRIMARY KEY NOT NULL,
    unit_id INT,
    teaching_session_id INT,
    name NVARCHAR(255) NOT NULL,
    duration NVARCHAR(50),
    start_date DATE,
    end_date DATE,
    hidden BIT DEFAULT 0,
    usage_count BIGINT,
    item_count BIGINT,
    approved_item_count BIGINT,
    deleted BIT DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME,

    -- Foreign Keys
    CONSTRAINT FK_ReadingList_Unit FOREIGN KEY (unit_id) REFERENCES Unit (ereserve_id),
    CONSTRAINT FK_ReadingList_TeachingSession FOREIGN KEY (teaching_session_id) REFERENCES TeachingSession (ereserve_id)
);
GO

-- ----------------------------------------
-- Table: ReadingListItem
-- ----------------------------------------

CREATE TABLE ReadingListItem (
    ereserve_id INT PRIMARY KEY NOT NULL,
    list_id INT NOT NULL,
    reading_id INT NOT NULL,
    status NVARCHAR(50),
    hidden BIT DEFAULT 0,
    reading_utilisations_count BIGINT DEFAULT 0,
    reading_importance NVARCHAR(100),
    usage_count BIGINT DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME,

    -- Foreign Keys
    CONSTRAINT FK_ReadingListItem_ReadingList FOREIGN KEY (list_id) REFERENCES ReadingList (ereserve_id),
    CONSTRAINT FK_ReadingListItem_Reading FOREIGN KEY (reading_id) REFERENCES Reading (ereserve_id)
);
GO

-- ----------------------------------------
-- Table: UnitOffering
-- ----------------------------------------

CREATE TABLE UnitOffering (
    ereserve_id INT PRIMARY KEY NOT NULL,
    unit_id INT NOT NULL,
    reading_list_id INT NOT NULL,
    source_unit_code NVARCHAR(100),
    source_unit_name NVARCHAR(255),
    source_unit_offering NVARCHAR(100),
    result NVARCHAR(255),
    list_publication_method NVARCHAR(100),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    -- Foreign Keys
    CONSTRAINT FK_UnitOffering_Unit FOREIGN KEY (unit_id) REFERENCES Unit (ereserve_id),
    CONSTRAINT FK_UnitOffering_ReadingList FOREIGN KEY (reading_list_id) REFERENCES ReadingList (ereserve_id)
);
GO
