CREATE TABLE appointments (
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255) NOT NULL,
    doctor VARCHAR(255) NOT NULL,
    starting_time VARCHAR(100) NOT NULL,
    PRIMARY KEY (name, starting_time)
);

CREATE TABLE test_results (
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    hemoglobin FLOAT NOT NULL,
    red_blood_cell FLOAT NOT NULL,
    white_blood_cell FLOAT NOT NULL,
    platelets FLOAT NOT NULL,
    neutrophils FLOAT NOT NULL,
    signature TEXT NOT NULL,
    PRIMARY KEY (name)
);
