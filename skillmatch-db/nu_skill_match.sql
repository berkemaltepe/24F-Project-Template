
DROP SCHEMA IF EXISTS skillmatch;
CREATE DATABASE skillmatch;
USE skillmatch;

CREATE TABLE IF NOT EXISTS Skill (
    skill_id int PRIMARY KEY,
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

CREATE TABLE IF NOT EXISTS Skill_Note (
    note_id int PRIMARY KEY AUTO_INCREMENT,
    faculty_id int,
    skill_id int,
    description VARCHAR(100),
    CONSTRAINT fk_faculty
        FOREIGN KEY (faculty_id) REFERENCES Dpt_Faculty (faculty_id)
            ON UPDATE cascade
            ON DELETE restrict, 
    CONSTRAINT fk_skill
        FOREIGN KEY (skill_id) REFERENCES Skill (skill_id)
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
    industry varchar(50),
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
(5, 'SQL', 'Programming', 10),
(6, 'Java', 'Programming', 9),
(7, 'Machine Learning', 'Programming', 8),
(8, 'Communication', 'Soft Skill', 7),
(9, 'Problem Solving', 'Soft Skill', 8),
(10, 'HTML/CSS', 'Programming', 6),
(11, 'Cloud Computing', 'Skill', 9),
(12, 'Data Visualization', 'Skill', 7),
(13, 'Teamwork', 'Soft Skill', 9),
(14, 'Python Django', 'Programming', 10),
(15, 'Cybersecurity', 'Skill', 8),
(16, 'Kubernetes', 'Programming', 9),
(17, 'DevOps', 'Skill', 8),
(18, 'React.js', 'Programming', 7),
(19, 'Angular', 'Programming', 6),
(20, 'Product Management', 'Soft Skill', 9),
(21, 'Creative Thinking', 'Soft Skill', 8),
(22, 'Leadership', 'Soft Skill', 10),
(23, 'Rust', 'Programming', 7),
(24, 'Go', 'Programming', 8),
(25, 'Terraform', 'Skill', 9),
(26, 'Azure', 'Skill', 7),
(27, 'Figma', 'Skill', 6),
(28, 'Docker', 'Programming', 10),
(29, 'Node.js', 'Programming', 9),
(30, 'Jira', 'Skill', 8),
(31, 'Adobe Photoshop', 'Skill', 7),
(32, 'Illustrator', 'Skill', 7),
(33, 'Data Engineering', 'Skill', 8),
(34, 'Pandas', 'Programming', 9),
(35, 'Numpy', 'Programming', 8),
(36, 'Apache Spark', 'Skill', 9),
(37, 'Blockchain', 'Programming', 10),
(38, 'Artificial Intelligence', 'Programming', 10),
(39, 'Business Analysis', 'Skill', 8),
(40, 'Public Speaking', 'Soft Skill', 8),
(41, 'Marketing Strategy', 'Skill', 9),
(42, 'Risk Analysis', 'Skill', 8),
(43, 'Financial Modeling', 'Skill', 7),
(44, 'Database Administration', 'Skill', 8),
(45, 'Big Data Analytics', 'Skill', 10),
(46, 'ElasticSearch', 'Programming', 7),
(47, 'C++', 'Programming', 9),
(48, 'TypeScript', 'Programming', 8),
(49, '3D Modeling', 'Skill', 7),
(50, 'Game Development', 'Skill', 9);

-- System_Admin Table
INSERT INTO System_Admin (admin_id, name, email, industry, num_applications) VALUES
(1, 'Alice Johnson', 'alice.johnson@example.com', 'Tech', 50),
(2, 'Bob Smith', 'bob.smith@example.com', 'Education', 30);

-- Dpt_Faculty Table
INSERT INTO Dpt_Faculty (faculty_id, admin_id, name, email, department) VALUES
(1, 1, 'Dr. Emily Davis', 'emily.davis@example.edu', 'Computer Science'),
(2, 1, 'Dr. John Lee', 'john.lee@example.edu', 'Information Systems'),
(3, 2, 'Dr. Clara Oswald', 'clara.oswald@example.edu', 'Mathematics');

-- Skill note table
INSERT INTO Skill_Note (note_id, faculty_id, skill_id, description) VALUES
(1, 1, 1, 'Python workshop for advanced programming techniques.'),
(2, 2, 15, 'Discussing the latest trends in cybersecurity.'),
(3, 3, 9, 'Developing strategies to improve problem-solving skills.'),
(4, 1, 38, 'AI seminar focusing on real-world applications.'),
(5, 2, 24, 'Go language training for cloud-based systems.'),
(6, 3, 44, 'Database administration best practices.'),
(7, 1, 45, 'Big data analytics certification course.'),
(8, 2, 20, 'Leadership training for cross-department collaboration.'),
(9, 3, 37, 'Exploring blockchain technology in modern systems.'),
(10, 1, 28, 'Hands-on workshop for Docker containerization.');

-- Advisor Table
INSERT INTO Advisor (advisor_id, admin_id, name, email, department) VALUES
(1, 1, 'Mark Brown', 'mark.brown@example.edu', 'Engineering'),
(2, 2, 'Linda White', 'linda.white@example.edu', 'Business'),
(3, 1, 'Nancy Green', 'nancy.green@example.edu', 'Science');

-- Employer Table
INSERT INTO Employer (emp_id, admin_id, name, email, industry, num_applications) VALUES
(1, 1, 'TechCorp', 'hr@techcorp.com', 'Technology', 25),
(2, 2, 'EduWorld', 'contact@eduworld.com', 'Education', 15),
(3, 1, 'MediCare', 'jobs@medicare.com', 'Healthcare', 10),
(4, 2, 'BuildIt', 'jobs@buildit.com', 'Construction', 12),
(5, 1, 'GreenEnergy', 'careers@greenenergy.com', 'Energy', 18),
(6, 1, 'AgriTech', 'jobs@agritech.com', 'Agriculture', 22),
(7, 2, 'FinSmart', 'hr@finsmart.com', 'Finance', 20),
(8, 1, 'TravelNow', 'careers@travelnow.com', 'Travel', 15),
(9, 2, 'EduPro', 'hr@edupro.com', 'Education', 8),
(10, 1, 'SafeHome', 'careers@safehome.com', 'Real Estate', 10),
(11, 2, 'BrightPath', 'jobs@brightpath.com', 'Education', 14),
(12, 1, 'QuickFix', 'hr@quickfix.com', 'Technology', 9),
(13, 2, 'SkillUp', 'jobs@skillup.com', 'Education', 11),
(14, 1, 'LifeCare', 'jobs@lifecare.com', 'Healthcare', 16),
(15, 1, 'SmartSolutions', 'careers@smartsolutions.com', 'Technology', 13),
(16, 2, 'FutureEd', 'hr@futureed.com', 'Education', 10),
(17, 1, 'TechWave', 'jobs@techwave.com', 'Technology', 21),
(18, 2, 'MindGrow', 'careers@mindgrow.com', 'Education', 8),
(19, 1, 'MediLink', 'jobs@medilink.com', 'Healthcare', 17),
(20, 2, 'InnoBuild', 'jobs@innobuild.com', 'Construction', 14),
(21, 1, 'AgriSolutions', 'hr@agrisolutions.com', 'Agriculture', 18),
(22, 2, 'TravelEasy', 'jobs@traveleasy.com', 'Travel', 20),
(23, 1, 'UrbanPlan', 'careers@urbanplan.com', 'Real Estate', 12),
(24, 2, 'GreenFuture', 'hr@greenfuture.com', 'Energy', 15),
(25, 1, 'BrightMind', 'jobs@brightmind.com', 'Technology', 16),
(26, 2, 'LearnPro', 'jobs@learnpro.com', 'Education', 10),
(27, 1, 'QuickStart', 'careers@quickstart.com', 'Technology', 11),
(28, 2, 'HealthSync', 'jobs@healthsync.com', 'Healthcare', 12),
(29, 1, 'TechVibes', 'jobs@techvibes.com', 'Technology', 14),
(30, 2, 'SkillMax', 'jobs@skillmax.com', 'Education', 13),
(31, 1, 'BrightWave', 'careers@brightwave.com', 'Technology', 17),
(32, 2, 'MindShift', 'hr@mindshift.com', 'Education', 9),
(33, 1, 'HealthTech', 'jobs@healthtech.com', 'Healthcare', 18),
(34, 2, 'GreenWorks', 'jobs@greenworks.com', 'Energy', 19),
(35, 1, 'BuildSmart', 'hr@buildsmart.com', 'Construction', 16),
(36, 2, 'TravelMore', 'jobs@travelmore.com', 'Travel', 14),
(37, 1, 'SafeHaven', 'jobs@safehaven.com', 'Real Estate', 13),
(38, 2, 'EduBright', 'jobs@edubright.com', 'Education', 12),
(39, 1, 'TechFuture', 'jobs@techfuture.com', 'Technology', 15),
(40, 2, 'SkillBoost', 'hr@skillboost.com', 'Education', 10);

-- Student Table
INSERT INTO Student (student_id, name, email, location, major, coop_status, resume, level, linkedin_profile, gpa, advisor_id, admin_id) VALUES
(1, 'Jane Doe', 'jane.doe@example.com', 'New York', 'Computer Science', 'Seeking', 'Resume Link 1', 'Junior', 'linkedin.com/janedoe', 3.8, 1, 1),
(2, 'John Smith', 'john.smith@example.com', 'Los Angeles', 'Information Systems', 'Co-op', 'Resume Link 2', 'Senior', 'linkedin.com/johnsmith', 3.6, 2, 1),
(3, 'Sara Connor', 'sara.connor@example.com', 'Chicago', 'Engineering', 'Seeking', 'Resume Link 3', 'Sophomore', 'linkedin.com/saraconnor', 3.7, 1, 2),
(4, 'Emily Clark', 'emily.clark@example.com', 'Houston', 'Business Administration', 'Seeking', 'Resume Link 4', 'Senior', 'linkedin.com/emilyclark', 3.9, 2, 2),
(5, 'Michael Brown', 'michael.brown@example.com', 'San Francisco', 'Data Science', 'Co-op', 'Resume Link 5', 'Junior', 'linkedin.com/michaelbrown', 3.8, 3, 1),
(6, 'Jessica Green', 'jessica.green@example.com', 'Miami', 'Biology', 'Seeking', 'Resume Link 6', 'Sophomore', 'linkedin.com/jessicagreen', 3.7, 2, 2),
(7, 'David Wilson', 'david.wilson@example.com', 'Seattle', 'Physics', 'Co-op', 'Resume Link 7', 'Junior', 'linkedin.com/davidwilson', 3.6, 3, 1),
(8, 'Sophia Martinez', 'sophia.martinez@example.com', 'Austin', 'Mechanical Engineering', 'Seeking', 'Resume Link 8', 'Senior', 'linkedin.com/sophiamartinez', 3.9, 1, 2),
(9, 'Chris Lee', 'chris.lee@example.com', 'Chicago', 'Economics', 'Co-op', 'Resume Link 9', 'Sophomore', 'linkedin.com/chrislee', 3.5, 3, 1),
(10, 'Ashley Davis', 'ashley.davis@example.com', 'Boston', 'Marketing', 'Seeking', 'Resume Link 10', 'Junior', 'linkedin.com/ashleydavis', 3.8, 2, 1),
(11, 'Daniel Young', 'daniel.young@example.com', 'New York', 'Mathematics', 'Seeking', 'Resume Link 11', 'Senior', 'linkedin.com/danielyoung', 3.9, 1, 1),
(12, 'Megan Hernandez', 'megan.hernandez@example.com', 'San Diego', 'Civil Engineering', 'Co-op', 'Resume Link 12', 'Sophomore', 'linkedin.com/meganhernandez', 3.6, 3, 2),
(13, 'Joshua Hall', 'joshua.hall@example.com', 'Denver', 'Finance', 'Seeking', 'Resume Link 13', 'Junior', 'linkedin.com/joshuahall', 3.7, 1, 1),
(14, 'Emma Wright', 'emma.wright@example.com', 'Atlanta', 'Psychology', 'Seeking', 'Resume Link 14', 'Senior', 'linkedin.com/emmawright', 3.8, 2, 2),
(15, 'Olivia Adams', 'olivia.adams@example.com', 'San Jose', 'Electrical Engineering', 'Co-op', 'Resume Link 15', 'Junior', 'linkedin.com/oliviaadams', 3.9, 1, 2),
(16, 'Jacob Lewis', 'jacob.lewis@example.com', 'Phoenix', 'Chemistry', 'Seeking', 'Resume Link 16', 'Sophomore', 'linkedin.com/jacoblewis', 3.5, 2, 1),
(17, 'Mia Robinson', 'mia.robinson@example.com', 'Portland', 'Environmental Science', 'Seeking', 'Resume Link 17', 'Senior', 'linkedin.com/miarobinson', 3.6, 3, 1),
(18, 'Ethan King', 'ethan.king@example.com', 'Philadelphia', 'History', 'Co-op', 'Resume Link 18', 'Junior', 'linkedin.com/ethanking', 3.7, 1, 2),
(19, 'Isabella Perez', 'isabella.perez@example.com', 'Las Vegas', 'Graphic Design', 'Seeking', 'Resume Link 19', 'Sophomore', 'linkedin.com/isabellaperez', 3.8, 2, 1),
(20, 'Liam Walker', 'liam.walker@example.com', 'Charlotte', 'Art', 'Seeking', 'Resume Link 20', 'Senior', 'linkedin.com/liamwalker', 3.9, 3, 2),
(21, 'Harper Scott', 'harper.scott@example.com', 'Orlando', 'Nursing', 'Co-op', 'Resume Link 21', 'Junior', 'linkedin.com/harperscott', 3.6, 1, 1),
(22, 'Avery Hill', 'avery.hill@example.com', 'Dallas', 'Law', 'Seeking', 'Resume Link 22', 'Senior', 'linkedin.com/averyhill', 3.7, 2, 2),
(23, 'Ryan Moore', 'ryan.moore@example.com', 'Detroit', 'Computer Engineering', 'Seeking', 'Resume Link 23', 'Junior', 'linkedin.com/ryanmoore', 3.8, 1, 1),
(24, 'Chloe Taylor', 'chloe.taylor@example.com', 'Indianapolis', 'Public Health', 'Co-op', 'Resume Link 24', 'Sophomore', 'linkedin.com/chloetaylor', 3.5, 3, 2),
(25, 'Logan Thomas', 'logan.thomas@example.com', 'Minneapolis', 'Philosophy', 'Seeking', 'Resume Link 25', 'Senior', 'linkedin.com/loganthomas', 3.6, 1, 2),
(26, 'Zoey Allen', 'zoey.allen@example.com', 'Memphis', 'Political Science', 'Seeking', 'Resume Link 26', 'Junior', 'linkedin.com/zoeyallen', 3.7, 2, 1),
(27, 'Elijah Carter', 'elijah.carter@example.com', 'Nashville', 'Biomedical Engineering', 'Co-op', 'Resume Link 27', 'Sophomore', 'linkedin.com/elijahcarter', 3.8, 3, 2),
(28, 'Ella Anderson', 'ella.anderson@example.com', 'Raleigh', 'Geology', 'Seeking', 'Resume Link 28', 'Senior', 'linkedin.com/ellaanderson', 3.9, 1, 1),
(29, 'Luke Martinez', 'luke.martinez@example.com', 'Salt Lake City', 'Astronomy', 'Seeking', 'Resume Link 29', 'Junior', 'linkedin.com/lukemartinez', 3.5, 2, 2),
(30, 'Hannah Jackson', 'hannah.jackson@example.com', 'Omaha', 'Architecture', 'Co-op', 'Resume Link 30', 'Sophomore', 'linkedin.com/hannahjackson', 3.6, 3, 1),
(31, 'Aiden Brooks', 'aiden.brooks@example.com', 'Richmond', 'Anthropology', 'Seeking', 'Resume Link 31', 'Senior', 'linkedin.com/aidenbrooks', 3.7, 1, 1),
(32, 'Charlotte Kelly', 'charlotte.kelly@example.com', 'Kansas City', 'Veterinary Medicine', 'Seeking', 'Resume Link 32', 'Junior', 'linkedin.com/charlottekelly', 3.8, 2, 2),
(33, 'Grayson Evans', 'grayson.evans@example.com', 'Louisville', 'Accounting', 'Co-op', 'Resume Link 33', 'Sophomore', 'linkedin.com/graysonevans', 3.9, 3, 2),
(34, 'Lily Rivera', 'lily.rivera@example.com', 'Columbus', 'English', 'Seeking', 'Resume Link 34', 'Senior', 'linkedin.com/lilyrivera', 3.6, 1, 1),
(35, 'Samuel Gray', 'samuel.gray@example.com', 'Milwaukee', 'Education', 'Seeking', 'Resume Link 35', 'Junior', 'linkedin.com/samuelgray', 3.7, 2, 2),
(36, 'Zoe Howard', 'zoe.howard@example.com', 'Baltimore', 'Journalism', 'Co-op', 'Resume Link 36', 'Sophomore', 'linkedin.com/zoehoward', 3.8, 3, 2),
(37, 'Evelyn Cook', 'evelyn.cook@example.com', 'New Orleans', 'Criminal Justice', 'Seeking', 'Resume Link 37', 'Senior', 'linkedin.com/evelyncook', 3.9, 1, 1),
(38, 'James Morgan', 'james.morgan@example.com', 'Jacksonville', 'Music', 'Seeking', 'Resume Link 38', 'Junior', 'linkedin.com/jamesmorgan', 3.5, 2, 1),
(39, 'Addison Bennett', 'addison.bennett@example.com', 'Oklahoma City', 'Kinesiology', 'Seeking', 'Resume Link 39', 'Sophomore', 'linkedin.com/addisonbennett', 3.6, 1, 2),
(40, 'Gabriel Bailey', 'gabriel.bailey@example.com', 'Tucson', 'Communications', 'Co-op', 'Resume Link 40', 'Senior', 'linkedin.com/gabrielbailey', 3.7, 2, 1),
(41, 'Madison Powell', 'madison.powell@example.com', 'Fresno', 'Theater', 'Seeking', 'Resume Link 41', 'Junior', 'linkedin.com/madisonpowell', 3.8, 1, 2),
(42, 'Jayden Adams', 'jayden.adams@example.com', 'El Paso', 'Sociology', 'Co-op', 'Resume Link 42', 'Senior', 'linkedin.com/jaydenadams', 3.9, 3, 1),
(43, 'Lillian Ward', 'lillian.ward@example.com', 'Colorado Springs', 'Statistics', 'Seeking', 'Resume Link 43', 'Sophomore', 'linkedin.com/lillianward', 3.5, 2, 1),
(44, 'Matthew Ortiz', 'matthew.ortiz@example.com', 'Tampa', 'Sports Science', 'Seeking', 'Resume Link 44', 'Senior', 'linkedin.com/matthewortiz', 3.6, 1, 2),
(45, 'Victoria Cox', 'victoria.cox@example.com', 'Bakersfield', 'Fashion Design', 'Seeking', 'Resume Link 45', 'Junior', 'linkedin.com/victoriacox', 3.7, 2, 1),
(46, 'Jackson Simmons', 'jackson.simmons@example.com', 'Aurora', 'Supply Chain Management', 'Seeking', 'Resume Link 46', 'Sophomore', 'linkedin.com/jacksonsimmons', 3.8, 1, 2),
(47, 'Layla Foster', 'layla.foster@example.com', 'Corpus Christi', 'Agricultural Science', 'Co-op', 'Resume Link 47', 'Senior', 'linkedin.com/laylafoster', 3.9, 3, 1),
(48, 'Dylan Long', 'dylan.long@example.com', 'Reno', 'Film Production', 'Seeking', 'Resume Link 48', 'Junior', 'linkedin.com/dylanlong', 3.5, 2, 2),
(49, 'Savannah Foster', 'savannah.foster@example.com', 'Boise', 'Public Policy', 'Seeking', 'Resume Link 49', 'Senior', 'linkedin.com/savannahfoster', 3.6, 1, 1),
(50, 'Owen Brooks', 'owen.brooks@example.com', 'Anchorage', 'Linguistics', 'Co-op', 'Resume Link 50', 'Sophomore', 'linkedin.com/owenbrooks', 3.7, 2, 2),
(51, 'Hannah Kotler', 'hannah.kotler@example.com', 'Seattle', 'Computer Science', 'Co-op', 'Resume Link 51', 'Sophomore', 'linkedin.com/berkemaltepe', 3.8, 3, 1);

-- Student_Skill Table
INSERT INTO Student_Skill (skill_id, student_id, weight) VALUES
(1, 1, 5), (2, 1, 2), (6, 1, 5), (7, 1, 3), (8, 1, 4),
(3, 2, 3),
(4, 2, 4),
(5, 3, 5),
(6, 4, 4),
(7, 5, 5),
(8, 6, 3),
(9, 7, 4),
(10, 8, 5),
(11, 9, 4),
(12, 10, 3),
(13, 11, 5),
(14, 12, 4),
(15, 13, 5),
(16, 14, 3),
(17, 15, 4),
(18, 16, 5),
(19, 17, 3),
(20, 18, 4),
(21, 19, 5),
(22, 20, 4),
(23, 21, 5),
(24, 22, 3),
(25, 23, 4),
(26, 24, 5),
(27, 25, 3),
(28, 26, 4),
(29, 27, 5),
(30, 28, 3),
(31, 29, 4),
(32, 30, 5),
(33, 31, 4),
(34, 32, 5),
(35, 33, 3),
(36, 34, 4),
(37, 35, 5),
(38, 36, 4),
(39, 37, 3),
(40, 38, 5),
(41, 39, 4),
(42, 40, 5),
(1, 51, 4), (15, 51, 3), (9, 51, 4), (6, 51, 4.5), (24, 51, 2), (26, 51, 4), (42, 51, 3);

-- Job Table with Updated Industries
INSERT INTO Job (job_id, title, emp_id, description, location, pay_range, industry, date_posted, status) VALUES
(1, 'Software Engineer', 1, 'Develop software applications.', 'Remote', '70k-90k', 'Technology', '2024-11-01', 'Open'),
(2, 'Data Analyst', 2, 'Analyze data and generate insights.', 'Los Angeles', '60k-80k', 'Technology', '2024-11-02', 'Open'),
(3, 'Project Manager', 3, 'Manage projects and teams.', 'Chicago', '80k-100k', 'Business', '2024-11-03', 'Open'),
(4, 'Web Developer', 1, 'Build and maintain websites.', 'Houston', '50k-70k', 'Technology', '2024-11-04', 'Open'),
(5, 'System Administrator', 2, 'Manage IT infrastructure.', 'New York', '60k-80k', 'Technology', '2024-11-05', 'Open'),
(6, 'Machine Learning Engineer', 1, 'Develop ML models.', 'San Francisco', '90k-120k', 'Technology', '2024-11-06', 'Open'),
(7, 'Graphic Designer', 2, 'Design marketing materials.', 'Chicago', '50k-65k', 'Creative', '2024-11-07', 'Open'),
(8, 'DevOps Engineer', 1, 'Manage CI/CD pipelines.', 'Seattle', '80k-100k', 'Technology', '2024-11-08', 'Open'),
(9, 'Game Developer', 1, 'Develop video games.', 'Austin', '70k-90k', 'Entertainment', '2024-11-09', 'Open'),
(10, 'UI/UX Designer', 2, 'Design user experiences.', 'Remote', '60k-80k', 'Creative', '2024-11-10', 'Open'),
(11, 'Database Administrator', 1, 'Manage database systems.', 'Miami', '70k-90k', 'Technology', '2024-11-11', 'Open'),
(12, 'Business Analyst', 2, 'Analyze business processes.', 'Los Angeles', '60k-80k', 'Business', '2024-11-12', 'Open'),
(13, 'Cybersecurity Analyst', 3, 'Protect digital assets.', 'New York', '80k-100k', 'Technology', '2024-11-13', 'Open'),
(14, 'Data Scientist', 1, 'Generate insights from data.', 'San Francisco', '90k-120k', 'Technology', '2024-11-14', 'Open'),
(15, 'Mobile App Developer', 1, 'Develop mobile apps.', 'Chicago', '70k-90k', 'Technology', '2024-11-15', 'Open'),
(16, 'Technical Writer', 2, 'Write technical documentation.', 'Remote', '50k-70k', 'Business', '2024-11-16', 'Open'),
(17, 'Product Manager', 1, 'Oversee product development.', 'San Diego', '90k-110k', 'Business', '2024-11-17', 'Open'),
(18, 'Network Engineer', 3, 'Design and maintain networks.', 'Houston', '75k-95k', 'Technology', '2024-11-18', 'Open'),
(19, 'Cloud Architect', 1, 'Design cloud-based solutions.', 'Seattle', '100k-130k', 'Technology', '2024-11-19', 'Open'),
(20, 'Software Tester', 2, 'Ensure software quality.', 'Austin', '60k-80k', 'Technology', '2024-11-20', 'Open'),
(21, 'Full Stack Developer', 1, 'Develop end-to-end solutions.', 'Chicago', '80k-100k', 'Technology', '2024-11-21', 'Open'),
(22, 'IT Support Specialist', 2, 'Provide technical support.', 'New York', '50k-70k', 'Technology', '2024-11-22', 'Open'),
(23, 'SEO Specialist', 2, 'Improve website rankings.', 'Los Angeles', '50k-65k', 'Marketing', '2024-11-23', 'Open'),
(24, 'Blockchain Developer', 1, 'Develop blockchain applications.', 'San Francisco', '100k-130k', 'Technology', '2024-11-24', 'Open'),
(25, 'Data Engineer', 1, 'Build data pipelines.', 'Austin', '90k-120k', 'Technology', '2024-11-25', 'Open'),
(26, 'Salesforce Developer', 2, 'Develop Salesforce applications.', 'Remote', '80k-100k', 'Technology', '2024-11-26', 'Open'),
(27, 'AR/VR Developer', 1, 'Develop AR/VR solutions.', 'Seattle', '90k-110k', 'Technology', '2024-11-27', 'Open'),
(28, 'Embedded Systems Engineer', 3, 'Develop embedded systems.', 'Chicago', '80k-100k', 'Technology', '2024-11-28', 'Open'),
(29, 'Digital Marketing Specialist', 2, 'Execute marketing campaigns.', 'Houston', '50k-70k', 'Marketing', '2024-11-29', 'Open'),
(30, 'Social Media Manager', 2, 'Manage social media platforms.', 'Remote', '50k-65k', 'Marketing', '2024-11-30', 'Open'),
(31, 'Data Visualization Specialist', 1, 'Create data visualizations.', 'San Francisco', '80k-100k', 'Technology', '2024-12-01', 'Open'),
(32, 'AI Researcher', 1, 'Conduct AI research.', 'Remote', '100k-130k', 'Technology', '2024-12-02', 'Open'),
(33, 'Game Designer', 1, 'Design gameplay mechanics.', 'Austin', '70k-90k', 'Entertainment', '2024-12-03', 'Open'),
(34, 'Automation Engineer', 2, 'Develop automation tools.', 'Seattle', '80k-100k', 'Technology', '2024-12-04', 'Open'),
(35, 'Robotics Engineer', 3, 'Develop robotics systems.', 'Houston', '90k-120k', 'Technology', '2024-12-05', 'Open'),
(36, 'Penetration Tester', 1, 'Identify security vulnerabilities.', 'New York', '80k-100k', 'Technology', '2024-12-06', 'Open'),
(37, 'Technical Recruiter', 2, 'Recruit technical talent.', 'Austin', '60k-80k', 'Human Resources', '2024-12-07', 'Open'),
(38, 'Hardware Engineer', 1, 'Design hardware components.', 'San Francisco', '100k-130k', 'Technology', '2024-12-08', 'Open'),
(39, 'AI Product Manager', 1, 'Manage AI products.', 'Remote', '110k-140k', 'Technology', '2024-12-09', 'Open'),
(40, 'Customer Success Manager', 2, 'Ensure customer satisfaction.', 'Chicago', '70k-90k', 'Business', '2024-12-10', 'Open'),
(41, 'Cybersecurity Consultant', 3, 'Advise on security practices.', 'Los Angeles', '90k-120k', 'Technology', '2024-12-11', 'Open'),
(42, 'Game Producer', 1, 'Manage game development.', 'Austin', '80k-100k', 'Entertainment', '2024-12-12', 'Open'),
(43, 'Data Governance Analyst', 1, 'Ensure data compliance.', 'Remote', '80k-100k', 'Technology', '2024-12-13', 'Open'),
(44, 'Financial Systems Analyst', 2, 'Manage financial systems.', 'New York', '70k-90k', 'Finance', '2024-12-14', 'Open'),
(45, 'Site Reliability Engineer', 1, 'Ensure system reliability.', 'San Francisco', '90k-120k', 'Technology', '2024-12-15', 'Open'),
(46, 'Performance Marketing Manager', 2, 'Optimize ad campaigns.', 'Los Angeles', '70k-90k', 'Marketing', '2024-12-16', 'Open'),
(47, 'CRM Manager', 2, 'Manage CRM systems.', 'Remote', '60k-80k', 'Marketing', '2024-12-17', 'Open'),
(48, 'Digital Strategist', 2, 'Develop digital strategies.', 'Houston', '80k-100k', 'Marketing', '2024-12-18', 'Open');

-- Job_Skill Table
INSERT INTO Job_Skill (skill_id, job_id, weight) VALUES
-- Job 1: Software Engineer
(1, 1, 5), (2, 1, 4), (6, 1, 4), (10, 1, 5), (21, 1, 3),
-- Job 2: Data Analyst
(2, 2, 5), (3, 2, 4), (8, 2, 4), (26, 2, 3), (11, 2, 5),
-- Job 3: Project Manager
(4, 3, 5), (9, 3, 4), (14, 3, 3), (15, 3, 5), (8, 3, 4),
-- Job 4: Web Developer
(1, 4, 5), (23, 4, 4), (10, 4, 5), (24, 4, 3), (7, 4, 4),
-- Job 5: System Administrator
(5, 5, 5), (6, 5, 4), (8, 5, 5), (20, 5, 3), (9, 5, 4),
-- Job 6: Machine Learning Engineer
(11, 6, 5), (18, 6, 5), (25, 6, 4), (37, 6, 5), (10, 6, 3),
-- Job 7: Graphic Designer
(13, 7, 5), (15, 7, 4), (34, 7, 5), (14, 7, 3), (21, 7, 5),
-- Job 8: DevOps Engineer
(6, 8, 5), (20, 8, 5), (17, 8, 5), (22, 8, 4), (8, 8, 3),
-- Job 9: Game Developer
(1, 9, 5), (27, 9, 5), (33, 9, 5), (22, 9, 4), (14, 9, 4),
-- Job 10: UI/UX Designer
(13, 10, 5), (15, 10, 4), (14, 10, 4), (21, 10, 5), (34, 10, 5),
-- Job 11: Database Administrator
(5, 11, 5), (6, 11, 4), (20, 11, 5), (37, 11, 4), (22, 11, 4),
-- Job 12: Business Analyst
(26, 12, 5), (3, 12, 4), (8, 12, 5), (27, 12, 4), (15, 12, 4),
-- Job 13: Cybersecurity Analyst
(19, 13, 5), (6, 13, 5), (25, 13, 4), (10, 13, 4), (37, 13, 5),
-- Job 14: Data Scientist
(11, 14, 5), (2, 14, 5), (26, 14, 4), (37, 14, 5), (10, 14, 4),
-- Job 15: Mobile App Developer
(1, 15, 5), (32, 15, 5), (31, 15, 5), (22, 15, 4), (14, 15, 4),
-- Job 16: Technical Writer
(40, 16, 5), (21, 16, 4), (8, 16, 3), (14, 16, 5), (3, 16, 4),
-- Job 17: Product Manager
(4, 17, 5), (15, 17, 5), (21, 17, 4), (9, 17, 3), (27, 17, 4),
-- Job 18: Network Engineer
(5, 18, 5), (6, 18, 4), (22, 18, 5), (19, 18, 5), (20, 18, 4),
-- Job 19: Cloud Architect
(17, 19, 5), (6, 19, 5), (11, 19, 4), (20, 19, 5), (22, 19, 4),
-- Job 20: Software Tester
(1, 20, 5), (3, 20, 4), (8, 20, 4), (20, 20, 3), (6, 20, 4),
-- Job 21: Full Stack Developer
(1, 21, 5), (5, 21, 4), (10, 21, 5), (7, 21, 4), (23, 21, 3),
-- Job 22: IT Support Specialist
(8, 22, 5), (9, 22, 4), (20, 22, 4), (6, 22, 3), (15, 22, 4),
-- Job 23: SEO Specialist
(29, 23, 5), (28, 23, 4), (13, 23, 5), (14, 23, 4), (15, 23, 3),
-- Job 24: Blockchain Developer
(30, 24, 5), (11, 24, 4), (6, 24, 5), (5, 24, 4), (37, 24, 3),
-- Job 25: Data Engineer
(2, 25, 5), (5, 25, 4), (11, 25, 5), (26, 25, 4), (37, 25, 3),
-- Job 26: Salesforce Developer
(1, 26, 5), (26, 26, 4), (6, 26, 5), (20, 26, 4), (11, 26, 3),
-- Job 27: AR/VR Developer
(38, 27, 5), (37, 27, 4), (34, 27, 5), (13, 27, 4), (14, 27, 3),
-- Job 28: Embedded Systems Engineer
(36, 28, 5), (6, 28, 4), (5, 28, 5), (18, 28, 5), (25, 28, 4),
-- Job 29: Digital Marketing Specialist
(29, 29, 5), (13, 29, 4), (15, 29, 5), (14, 29, 4), (40, 29, 3),
-- Job 30: Social Media Manager
(28, 30, 5), (29, 30, 4), (13, 30, 5), (15, 30, 4), (27, 30, 3),
-- Job 31: Data Visualization Specialist
(21, 31, 5), (11, 31, 5), (2, 31, 4), (26, 31, 5), (10, 31, 3),
-- Job 32: AI Researcher
(11, 32, 5), (25, 32, 5), (37, 32, 5), (10, 32, 4), (26, 32, 4),
-- Job 33: Game Designer
(33, 33, 5), (34, 33, 4), (13, 33, 5), (27, 33, 4), (14, 33, 3),
-- Job 34: Automation Engineer
(6, 34, 5), (17, 34, 5), (5, 34, 4), (20, 34, 5), (11, 34, 3),
-- Job 35: Robotics Engineer
(36, 35, 5), (5, 35, 4), (25, 35, 5), (18, 35, 4), (37, 35, 3),
-- Job 36: Penetration Tester
(19, 36, 5), (5, 36, 4), (6, 36, 5), (8, 36, 4), (18, 36, 3),
-- Job 37: Technical Recruiter
(40, 37, 5), (15, 37, 4), (8, 37, 3), (9, 37, 5), (13, 37, 4),
-- Job 38: Hardware Engineer
(6, 38, 5), (36, 38, 5), (25, 38, 4), (18, 38, 4), (37, 38, 3),
-- Job 39: AI Product Manager
(25, 39, 5), (11, 39, 4), (37, 39, 5), (15, 39, 4), (14, 39, 3),
-- Job 40: Customer Success Manager
(9, 40, 5), (15, 40, 4), (40, 40, 3), (8, 40, 5), (27, 40, 4),
-- Job 41: Cybersecurity Consultant
(19, 41, 5), (5, 41, 4), (25, 41, 5), (8, 41, 4), (20, 41, 3),
-- Job 42: Game Producer
(33, 42, 5), (34, 42, 4), (27, 42, 5), (15, 42, 4), (13, 42, 3),
-- Job 43: Data Governance Analyst
(26, 43, 5), (2, 43, 4), (11, 43, 5), (37, 43, 4), (10, 43, 3),
-- Job 44: Financial Systems Analyst
(2, 44, 5), (5, 44, 4), (26, 44, 5), (11, 44, 4), (37, 44, 3),
-- Job 45: Site Reliability Engineer
(6, 45, 5), (17, 45, 5), (20, 45, 5), (11, 45, 4), (22, 45, 4),
-- Job 46: Performance Marketing Manager
(29, 46, 5), (13, 46, 5), (27, 46, 4), (15, 46, 4), (28, 46, 3),
-- Job 47: CRM Manager
(26, 47, 5), (5, 47, 4), (6, 47, 5), (20, 47, 4), (28, 47, 3),
-- Job 48: Digital Strategist
(29, 48, 5), (13, 48, 5), (15, 48, 4), (28, 48, 4), (27, 48, 3);

