
CREATE table IF NOT EXISTS courses(
   code_module text,
   code_presentation text,
   module_presentation int,
   CONSTRAINT courses_key UNIQUE (code_module, code_presentation),
   CONSTRAINT courses_key PRIMARY KEY (code_module, code_presentation)
);

CREATE table IF NOT EXISTS assessments(
    code_module text,
    code_presentation text,
    id_assessment int NOT NULL,
    assessment_type text,
    date int,
    weight float,
    CONSTRAINT assessments_key PRIMARY KEY (id_assessment),
    FOREIGN KEY (code_module, code_presentation) references courses(code_module, code_presentation)
);

CREATE table IF NOT EXISTS studentInfo(
    code_module text,
    code_presentation text,
    id_student bigint NOT NULL,
    gender text,
    region text,
    highest_education text,
    imd_brand text,
    age_band text,
    num_of_prev_attempts int,
    studied_credits int,
    disablility text,
    final_result text,
    CONSTRAINT student_key PRIMARY KEY (id_student),
    FOREIGN KEY (code_module, code_presentation) references courses(code_module, code_presentation)
    
);

CREATE table IF NOT EXISTS vle(
    id_site int NOT NULL,
    code_module text,
    code_presentation text,
    activity_type text,
    week_from int,
    week_to int,
    CONSTRAINT vle_key PRIMARY KEY (id_site),
    FOREIGN KEY (code_module, code_presentation) references courses(code_module, code_presentation)
);

CREATE table IF NOT EXISTS studentAssessment(
    id_assessment int NOT NULL,
    id_student bigint NOT NULL,
    date_submitted int,
    is_banked int,
    score  float,
    FOREIGN KEY (id_student) references studentInfo(id_student),
    FOREIGN KEY (id_assessment) references assessments(id_assessment)  
);

CREATE table IF NOT EXISTS studentVle(
    code_module text,
    code_presentation text,
    id_student bigint NOT NULL,
    id_site int NOT NULL,
    date int,
    sum_click int,
    FOREIGN KEY (code_module, code_presentation) references courses,
    FOREIGN KEY (id_site) references vle(id_site),
    FOREIGN KEY (id_student) references studentInfo(id_student)
);

CREATE table IF NOT EXISTS studentRegistration(
    code_module text,
    code_presentation text,
    id_student bigint NOT NULL,
    date_registration int,
    date_unregistration int,
    FOREIGN KEY (code_module, code_presentation) references courses,
    FOREIGN KEY (id_student) references studentInfo(id_student)
);



\COPY courses FROM '/Users/akhilesh/Desktop/col362_project/SAVLIP/courses.csv' DELIMITER ',' CSV HEADER;


/* for assessments table, do similar for others*/
CREATE TEMP TABLE assessments_tmp AS TABLE assessments LIMIT 0;
ALTER TABLE assessments_tmp ALTER date TYPE text;
\COPY assessments_tmp FROM '/Users/akhilesh/Desktop/col362_project/SAVLIP/assessments.csv' DELIMITER ',' CSV HEADER;
INSERT INTO assessments
SELECT code_module, code_presentation, id_assessment, assessment_type, NULLIF(date, '')::int, weight --type casting error is solved here
FROM   assessments_tmp;

/*

\COPY courses FROM 'courses.csv' DELIMITER ',' CSV HEADER;
\COPY assessments FROM 'assessments.csv' DELIMITER ',' CSV HEADER;
\COPY studentInfo FROM 'studentInfo.csv' DELIMITER ',' CSV HEADER;
\COPY studentAssessment FROM 'studentAssessment.csv' DELIMITER ',' CSV HEADER;
\COPY studentRegistration FROM 'studentRegistration.csv' DELIMITER ',' CSV HEADER;
\COPY studentVle FROM 'studentVle.csv' DELIMITER ',' CSV HEADER;
\COPY vle FROM 'vle.csv' DELIMITER ',' CSV HEADER;

*/
