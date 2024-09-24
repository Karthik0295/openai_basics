
# Chat Application with OpenAI Integration

This project is a chat application built using FastAPI and SQLAlchemy, which integrates OpenAI's API for various functionalities like summarizing text, translating languages, and processing file uploads. The application uses MySQL Workbench as the database.

## Features

- **User Management**: Creating user(a basic one with minimal features)
- **Chat Threads**: Users can create chat threads to maintain conversation history.
- **Messaging**: Send messages within chat threads and receive AI-generated responses.
- **File Uploads**: Upload documents (only PDF) for summarization.
- **Text Translation**: Translate text between specified languages.
- **Audio Transcription**: Upload audio files to transcribe speech and summarize the content.

## Technology Stack

- **Backend**: FastAPI
- **Database**: Microsoft SQL Server (MSSQL)
- **ORM**: SQLAlchemy
- **OpenAI API**: For chat responses, translations, and summarization
- **File Handling**: Python libraries for handling different file formats (PDF, DOCX, XLSX)

## Getting Started

### Prerequisites

- Python 3.x
- Microsoft SQL Server
- OpenAI API Key
- Install required packages: requirements.txt


### Environment Variables

Create a `.env` file in the project root and add your OpenAI API key:

```plaintext
OPENAI_API_KEY=
DATABASE_URL= 
```

### Database Setup

Make sure to set up your MSSQL database and update the connection details in your `database.py` file. 

### Running the Application

To run the application, use the command:

```bash
main python.py
```

Visit `http://127.0.0.1:8000/docs` to access the automatically generated API documentation and test the endpoints.

## API Endpoints

### Create a Chat Thread

- **POST** `/chat/threads`
- **Parameters**:
  - `username`: The username of the user.
  - `thread_name`: The name of the chat thread.

### Send a Message

- **POST** `/chat/threads/{thread_id}/messages`
- **Parameters**:
  - `username`: The username of the user.
  - `message`: The message to send.
  - `thread_id`: The ID of the chat thread.

### Summarize a Document

- **POST** `/summary`
- **Parameters**:
  - `file`: The document file to be summarized (only PDF).

### Translate Text

- **POST** `/translate`
- **Parameters**:
  - `language1`: Source language.
  - `language2`: Target language.
  - `message`: The message to be translated.

### Speech to Summary

- **POST** `/speech-to-summary`
- **Parameters**:
  - `file`: The audio file to be transcribed and summarized.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.


