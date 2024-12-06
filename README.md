# NU SkillMatch Repository

Created By: The Matchmakers
Members: Nick Ashizawa, Berke Maltepe, Lea Lang, Colin Chu, Yuta Namba

NU SkillMatch is an application that assesses students' current skills against industry requirements for their desired career paths. By analyzing data from job postings, co-op descriptions, students' academic records, the app identifies skill gaps and recommends specific courses, workshops, or extracurricular activities to bridge those gaps as well as gives a visual and numerical representation of how well their skills align with the employer’s requirements. 

Current solutions such as NUWorks make it difficult to know whether applicants are qualified for job postings with their current skill sets, and leads to many unqualified applicants. A data-driven approach to this problem can streamline the job application process and make it clearer to applicants what skills they need to work on, as well as give employers, co-op advisors and school administrators an idea of what skills students have.

**YouTube Video Link:** https://youtu.be/5SegDjA5NTo

## Project Components

Currently, there are three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- SQL files for your data model and data base in the `./database-files` directory

# Build / Startup
## Necessary Database File(s)
- nu_skill_match.sql
## Docker Compose File
```yaml
services:
  app:
    build: ./app
    container_name: web-app  
    hostname: web-app
    volumes: ['./app/src:/appcode']
    ports:
      - 8501:8501

  api:
    build: ./api
    container_name: web-api
    hostname: web-api
    volumes: ['./api:/apicode']
    ports:
      - 4000:4000

  db:
    env_file:
      - ./api/.env
    image: mysql:9
    container_name: mysql_db
    hostname: db
    volumes:
      - ./skillmatch-db:/docker-entrypoint-initdb.d/:ro
    ports:
      - 3200:3306
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: skillmatch
```
## .env file configuration
- SECRET_KEY=someCrazyS3cR3T!Key.!
- DB_USER=root
- DB_HOST=db
- DB_PORT=3306
- DB_NAME=skillmatch
- MYSQL_ROOT_PASSWORD=password
## External Libraries Used
Within venv folder:
- plotly library used for creating radar charts

## 💼 Student Persona 💼
### Pages:
- **Student Jobs**
  - View jobs by best match as well as all jobs
  - Gives job match percentage for the jobs
  - Lets you navigate to skill match details for specific job
- **Student Skill Match Chart**
  - View match between student and job
  - Visualization with radar chart
  - Numerical gap % between student's skills and employer's required skills
- **Student Profile**
  - View Student Profile Information
  - Student profile
  - Navigate to Student Skills Page
- **Student Skills Page**
  - View Student Skills
  - Add a skill to profile

## 🧳 Employer Persona 🧳
### Pages:
- **View Company Info**
	- Name, ID, contact info, as well as view job listings within the company
	- Can edit the contact info (email address)
- **Candidate Match Chart / Skill Information**
	- Search a student by ID (assumed that name would be obtained through some kind of application to the employer, who can then go into the system and search for the student by ID)
	- Once found, employer can view the match between a student's skills and the required skills for a given job.
	- Visualization with a functional radar chart
	- Numerical gap % between student's skills and employer's required skills
- **Company Job Listing Editor**
	- Edit all info about jobs
		- Name, required skills, salary, etc.
	- Remove jobs
	- Add new jobs
- **View List of Students in System**
	- Complete list of students in the system
		- ID, Name, Major (other information hidden for student privacy)


## 🧑‍🏫 Co-op Advisor Persona 🧑‍🏫
## Pages:
- **Advisor Skill Match**
  - Select a student from the advisor’s assigned list to evaluate their skills.
  - Compare a student's skills to the required skills for a specific job.
    - Visualization with Radar Chart: Compare the student’s proficiency with the employer’s required skills.
    - Skill Gap Analysis: Numerical representation of the total skill gap percentage between the student’s skills and job requirements.
- **Advisor Job Postings**
  - View all active job postings available in the system.
  - Includes job title, company name, location, salary range, and job status.
  - Search and filter job postings based on relevance to the advisor’s students or specific skill requirements.
  - Navigate to job details for in-depth skill analysis.
- **Students List**
  - View the list of students assigned to the advisor.
  - Includes detailed student information: Name, ID, Major, GPA, Co-op Status, and Contact Information.
  - Assign or reassign students to/from the advisor.
  - Add or remove students from the advisor’s list.
- **Advisor Profile**
  - View and update the advisor's profile, including name, email, and department.
  - Manage account settings, such as updating contact information.


## 🏫 Department Head Persona 🏫
### Pages:
- **Top Skills**
  - View top skills among all job postings, ranked by frequency
  - View skill information and analytics (skill type, frequency, average employer weight, average student proficiency)
  - Filter through skills by skill type
  - Add, edit, and remove skill notes (Skill notes are associated by department head, so 
  only the user who wrote them can see them)
- **Major Program Reports**
  - View top student skills according to major, ranked by frequency 
  - View top job skills according to industry, ranked by frequency
  - View skill information and analytics 
  - Compare top student skills in chosen major to top industry skills with a radar chart 
- **Search by Skill**
  - View all job listings and job details (name, company, description, industry, pay range, date posted, status, required skills)
  - View all students and student details (name, major, level email, GPA, co-op status, skills)
  - Filter job postings and students by skill name
  - 

## 🖥️ System Admin Persona 🖥️
### Pages:
- **Admin Home Page**
  - Greets the admin. This page lets admins access the rest of the below pages (which can be accessed through the sidebar as well).
- **Admin Profile Page**
  - Displays the admin's information, including ID, name, email, industry,y and number of applications in the system.
  - Admins can edit their own profile with the edit button and save their changes.
- **Jobs Page**
  - This page lets admins view a table of all jobs and relevant information.
  - Admins can also add a job by giving in all information for a new job, or delete a job using its job ID.
    - All fields must be filled out, and all jobs must have unique job IDs, or the page won't let it add the job.
    - Any changes made will be updated on the table on this page and everywhere else it's accessed.
- **Skills Page**
  - Same as jobs page, admins can view, add, and delete skills.
- **Employers Page**
  - Same as jobs page, but admins don't have the option to delete employers, they can only view and add them.
- **Faculties Page**
  - Same as jobs page, but admins don't have the option to delete faculties, they can only view and add them.
- **Advisors Page**
  - Same as jobs page, but admins don't have the option to delete advisors, they can only view and add them.
- **Students Page**
  - Same as jobs page, admins can view, add, and delete students.
