CREATE DATABASE theologian_chatbot;

-- Switch to the database
USE theologian_chatbot;

-- Create the users table (optional, depends on your usage)
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    signup_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create the interaction table to store user interactions
CREATE TABLE interaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    theologian VARCHAR(50) NOT NULL,
    response TEXT NOT NULL,
    interaction_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
