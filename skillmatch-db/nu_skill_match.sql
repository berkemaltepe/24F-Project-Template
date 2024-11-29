DROP SCHEMA IF EXISTS skillmatch;
CREATE DATABASE skillmatch;
USE skillmatch;

CREATE TABLE IF NOT EXISTS Skill (
    skill_id int PRIMARY KEY AUTO_INCREMENT,
    skill_name varchar(50),
    skill_type varchar(50),
    weight int
);

CREATE TABLE IF NOT EXISTS System_Admin (
    admin_id int PRIMARY KEY,
    name varchar(50),
    email varchar(50),
    industry varchar(50),
    num_applications int
);

CREATE TABLE IF NOT EXISTS Dpt_Faculty (
    faculty_id int PRIMARY KEY,
    admin_id int,
    name varchar(50),
    email varchar(50),
    department varchar(50),
    CONSTRAINT fk_1
        FOREIGN KEY (admin_id) REFERENCES System_Admin (admin_id)
            ON UPDATE cascade
            ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Advisor (
    advisor_id int PRIMARY KEY,
    admin_id int,
    name varchar(50),
    email varchar(50),
    department varchar(50),
    CONSTRAINT fk_2
        FOREIGN KEY (admin_id) REFERENCES System_Admin (admin_id)
            ON UPDATE cascade
            ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Employer (
    emp_id int PRIMARY KEY,
    admin_id int,
    name varchar(50),
    email varchar(50),
    industry varchar(50),
    num_applications int,
    CONSTRAINT fk_3
        FOREIGN KEY (admin_id) REFERENCES System_Admin (admin_id)
            ON UPDATE cascade
            ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Student (
    student_id int PRIMARY KEY,
    name varchar(50),
    email varchar(50),
    location varchar(50),
    major varchar(50),
    coop_status varchar(30),
    resume varchar(5000),
    level varchar(50),
    linkedin_profile varchar(50),
    gpa int,
    advisor_id int,
    admin_id int,
    CONSTRAINT fk_4
        FOREIGN KEY (advisor_id) REFERENCES Advisor (advisor_id)
            ON UPDATE cascade
            ON DELETE restrict,
    CONSTRAINT fk_5
        FOREIGN KEY (admin_id) REFERENCES System_Admin (admin_id)
            ON UPDATE cascade
            ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Student_Skill (
    skill_id int,
    student_id int,
    weight int,
    PRIMARY KEY (skill_id, student_id),
    CONSTRAINT fk_6
        FOREIGN KEY (skill_id) REFERENCES Skill (skill_id)
            ON UPDATE cascade
            ON DELETE cascade,
    CONSTRAINT fk_7
        FOREIGN KEY (student_id) REFERENCES Student (student_id)
            ON UPDATE cascade
            ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Job (
    job_id int PRIMARY KEY AUTO_INCREMENT,
    title varchar(50),
    emp_id int,
    description varchar(1000),
    location varchar(50),
    pay_range varchar(50),
    date_posted datetime,
    status varchar(30),
    CONSTRAINT fk_8
        FOREIGN KEY (emp_id) REFERENCES Employer (emp_id)
            ON UPDATE cascade
            ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS Job_Skill (
    skill_id int,
    job_id int,
    weight int,
    PRIMARY KEY (skill_id, job_id),
    CONSTRAINT fk_9
        FOREIGN KEY (skill_id) REFERENCES Skill (skill_id)
            ON UPDATE cascade
            ON DELETE cascade,
    CONSTRAINT fk_10
        FOREIGN KEY (job_id) REFERENCES Job (job_id)
            ON UPDATE cascade
            ON DELETE cascade
);

INSERT INTO Skill (skill_id, skill_name, skill_type, weight) VALUES
(1, 'Python', 'Programming', 10),
(2, 'Data Analysis', 'Skill', 8),
(3, 'Leadership', 'Soft Skill', 7),
(4, 'Project Management', 'Soft Skill', 9),
(5, 'SQL', 'Programming', 10);

-- System_Admin Table
INSERT INTO System_Admin (admin_id, name, email, industry, num_applications) VALUES
(1, 'Alice Johnson', 'alice.johnson@example.com', 'Tech', 50),
(2, 'Bob Smith', 'bob.smith@example.com', 'Education', 30);

-- Dpt_Faculty Table
INSERT INTO Dpt_Faculty (faculty_id, admin_id, name, email, department) VALUES
(1, 1, 'Dr. Emily Davis', 'emily.davis@example.edu', 'Computer Science'),
(2, 1, 'Dr. John Lee', 'john.lee@example.edu', 'Information Systems'),
(3, 2, 'Dr. Clara Oswald', 'clara.oswald@example.edu', 'Mathematics');

-- Advisor Table
INSERT INTO Advisor (advisor_id, admin_id, name, email, department) VALUES
(1, 1, 'Mark Brown', 'mark.brown@example.edu', 'Engineering'),
(2, 2, 'Linda White', 'linda.white@example.edu', 'Business'),
(3, 1, 'Nancy Green', 'nancy.green@example.edu', 'Science');

-- Employer Table
INSERT INTO Employer (emp_id, admin_id, name, email, industry, num_applications) VALUES
(1, 1, 'TechCorp', 'hr@techcorp.com', 'Technology', 25),
(2, 2, 'EduWorld', 'contact@eduworld.com', 'Education', 15),
(3, 1, 'MediCare', 'jobs@medicare.com', 'Healthcare', 10);

-- Student Table
INSERT INTO Student (student_id, name, email, location, major, coop_status, resume, level, linkedin_profile, gpa, advisor_id, admin_id) VALUES
(1, 'Jane Doe', 'jane.doe@example.com', 'New York', 'Computer Science', 'Seeking', 'Resume Link 1', 'Junior', 'linkedin.com/janedoe', 3.8, 1, 1),
(2, 'John Smith', 'john.smith@example.com', 'Los Angeles', 'Information Systems', 'Co-op', 'Resume Link 2', 'Senior', 'linkedin.com/johnsmith', 3.6, 2, 1),
(3, 'Sara Connor', 'sara.connor@example.com', 'Chicago', 'Engineering', 'Seeking', 'Resume Link 3', 'Sophomore', 'linkedin.com/saraconnor', 3.7, 1, 2);

-- Student_Skill Table
INSERT INTO Student_Skill (skill_id, student_id, weight) VALUES
(1, 1, 5),
(2, 1, 4),
(3, 2, 3),
(4, 2, 4),
(5, 3, 5);

-- Job Table
INSERT INTO Job (job_id, title, emp_id, description, location, pay_range, date_posted, status) VALUES
(1, 'Software Engineer', 1, 'Develop software applications.', 'Remote', '70k-90k', '2024-11-01', 'Open'),
(2, 'Data Analyst', 2, 'Analyze data and generate insights.', 'Los Angeles', '60k-80k', '2024-11-02', 'Open'),
(3, 'Project Manager', 3, 'Manage projects and teams.', 'Chicago', '80k-100k', '2024-11-03', 'Open');

-- Job_Skill Table
INSERT INTO Job_Skill (skill_id, job_id, weight) VALUES
(1, 1, 5),
(2, 1, 4),
(3, 2, 3),
(4, 3, 4),
(5, 3, 5);