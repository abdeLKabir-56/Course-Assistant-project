# Course Assistant

## Overview
Course Assistant is a web application designed to help users interact with AI models to get answers to their course-related questions. The application features an intuitive interface where users can select a course, ask questions, and receive responses generated by various AI models.

## Features
- **Interactive UI**: Built with Streamlit for a responsive and user-friendly interface.
- **AI Model Integration**: Supports multiple AI models for answering questions.
- **Database Management**: Uses TiDB Cloud for storing conversation data and feedback.
- **Real-time Feedback**: Allows users to provide feedback on the responses received.

## Inspiration
The Course Assistant project was inspired by the need for a streamlined tool to assist learners with course-related queries using advanced AI technologies. The goal was to create an application that not only provides accurate answers but also collects user feedback to improve over time.

## What It Does
The application allows users to select a course and ask questions. It uses AI models to generate responses and displays relevant information such as response time and cost. Users can provide feedback on the answers, which is stored in a database for analysis.

## How We Built It
- **Languages & Frameworks**: Python, Streamlit, PyMySQL.
- **Database**: TiDB Cloud for scalable data management.
- **AI Integration**: OpenAI API for leveraging advanced language models.
- **Deployment**: Docker for containerization and Docker Compose for managing services.

## Challenges We Ran Into
- **Database Connectivity**: Configuring TiDB Cloud for secure and reliable connections.
- **AI Model Performance**: Ensuring that the chosen models provide relevant and accurate responses.
- **Feedback Handling**: Implementing a robust feedback system to improve the application's performance.

## Accomplishments That We're Proud Of
- Successfully integrated multiple AI models into a single application.
- Developed a responsive and intuitive web interface using Streamlit.
- Implemented a comprehensive feedback system to continuously improve the application's responses.

## What We Learned
- Gained experience with TiDB Cloud and its integration with Python applications.
- Improved skills in building interactive web applications with Streamlit.
- Learned about handling feedback and using it to enhance application performance.

## What's Next for Course Assistant
- **Model Expansion**: Integrate more AI models for broader functionality.
- **Feature Enhancements**: Add new features based on user feedback.
- **Performance Optimization**: Continuously improve the application's performance and response accuracy.

## Built With
- **Languages**: Python
- **Frameworks**: Streamlit, PyMySQL
- **Cloud Services**: TiDB Cloud
- **Databases**: TiDB
- **APIs**: OpenAI API
- **Tools**: Docker, Python-dotenv
- **Libraries**: pandas, requests, tqdm, sentence-transformers

## Getting Started
To get started with Course Assistant, clone this repository and follow the instructions in the `Dockerfile` and `docker-compose.yml` for setting up your environment.

## Contributing

We welcome contributions to the Course Assistant project! To get started, please fork the repository and submit a pull request with your changes. For detailed guidelines, refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to thank the TiDB community and the Streamlit team for their support and excellent documentation, which greatly facilitated the development process.
