# Documentation for the Medical Analysis Telegram Bot Project

## Description

This project is a Telegram bot that accepts medical analysis and research documents, extracts data from them, and responds to user questions based on the stored data.

## Functional Requirements

1. **Document Reception**
   - The bot must accept documents in PDF, PNG, and JPEG formats.
   - The user uploads a file containing medical analyses to the chat with the bot.

2. **Data Extraction**
   - The bot must extract the following data from documents:
     - For medical analyses:
       - Name of the analysis (e.g., "Hemoglobin," "Glucose").
       - Reference values (normal ranges) for the analysis.
       - Units of measurement (e.g., g/dL, %).
       - Results of the analysis (e.g., numerical values or text).
       - Date of the analysis.
       - Location where the analysis was conducted (e.g., name of the medical institution).
       - Address of the institution.
     - For medical research:
       - Name of the research (e.g., "Ultrasound").
       - Date of the research.
       - Location where the research was conducted (e.g., name of the medical institution).
       - The equipment used for the research.
       - Research protocol.
       - Research conclusions.
       - Research recommendations.
       - Address of the institution.
   - The extracted data must be structured and presented as a list to the user.

3. **Data Storage**
   - The extracted data must be saved in a PostgreSQL database.
   - The database structure should allow for efficient data storage and querying.

4. **User Interaction**
   - The bot must be able to answer user questions based on the uploaded medical analyses and research.
   - Users should be able to ask questions to the bot, such as:
     - "What were my results for [analysis name]?"
     - "Show me the test results from [time period]."
   - The bot should correctly interpret user queries and provide appropriate responses based on the data in the database.

5. **Request Handling**
   - The bot must correctly extract and display information from the database based on user queries.
   - The bot's responses should be accurate and include all requested data.

## Non-Functional Requirements

1. **Documentation**
   - A brief documentation of the solution architecture should be provided, including a description of the database structure, libraries, and APIs used.
   - Documentation for deployment and running the bot must be included.

2. **Tools and Technologies**
   - Telegram Bot API for bot creation.
   - Any library for processing and extracting text from PDF, PNG, and JPEG.
   - Any proprietary large language model API.
   - PostgreSQL for data storage.
   - Any ORM for database interactions.
   - Docker for containerization (optional, but preferred).

## Key Evaluation Metrics

1. **Data Extraction Accuracy**
   - The percentage of correctly extracted data from documents compared to the actual data in the analyses.
   - Accuracy of extracting all required fields (analysis name, reference values, results, date, location).

2. **Correct User Query Responses**
   - The accuracy and completeness of the bot's answers to user requests.
   - The bot's ability to interpret various query formulations.

3. **Performance**
   - Document processing time and response generation for user queries.

## Solution Architecture

### Project Files

- **`bot.py`**: Main file that handles Telegram webhooks, uploads files, extracts text, and interacts with the GPT-4 model.
- **`llm.py`**: Module for interacting with the OpenAI API to get responses from the GPT-4 model.
- **`text_extraction.py`**: Module for extracting text from PDFs and images.
- **`models.py`**: Defines the database structure using SQLAlchemy.
- **`db_setup.py`**: Sets up the database connection and creates sessions.

### Database

The PostgreSQL database structure includes two main tables:

- **`users`**: Table storing user information (ID, first name, last name, username).
- **`files`**: Table storing file information (ID, user ID, file name, file type, content).

### Deployment Process

1. **Environment Setup**
   - Install necessary dependencies.
   - Set up environment variables (e.g., `TOKEN`, `OPENAI_API_KEY`, `DATABASE_URL`).

2. **Running the Application**
   - Start the Flask server using the command `python bot.py`.
   - Set the Telegram webhook using the `/set-webhook` endpoint.

## Notes

- Ensure all environment variables are set correctly.
- Check that all dependencies are installed.
- Tesseract-OCR must be installed for image processing.
- The bot does not retain previous interactions and can only provide answers based on the information contained in the uploaded documents.
- If the file size exceeds the allowed limit, the bot will not be able to process the request.
