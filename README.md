# NU SkillMatch Repository

NU SkillMatch is an application that assesses students' current skills against industry requirements for their desired career paths. By analyzing data from job postings, co-op descriptions, students' academic records, the app identifies skill gaps and recommends specific courses, workshops, or extracurricular activities to bridge those gaps as well as gives a visual and numerical representation of how well their skills align with the employer’s requirements. 

Current solutions such as NUWorks make it difficult to know whether applicants are qualified for job postings with their current skill sets, and leads to many unqualified applicants. A data-driven approach to this problem can streamline the job application process and make it clearer to applicants what skills they need to work on, as well as give employers, co-op advisors and school administrators an idea of what skills students have.

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
