# Course Assistant

## Inspiration

The Course Assistant project was inspired by the need for a comprehensive tool that helps educators and students manage and evaluate course interactions more effectively. We wanted to create a solution that would streamline the process of tracking conversations and feedback, enabling better insights into course effectiveness and student engagement. Our goal was to build a tool that not only captures this data but also provides actionable insights to enhance the overall learning experience.

## What it does

Course Assistant is a robust application designed to manage and analyze course-related interactions. It captures detailed data on conversations between students and course assistants, including the questions asked, answers provided, and various metrics related to these interactions. Additionally, it collects feedback from users to evaluate and improve the quality of responses. The application offers features such as:

- **Conversation Management**: Tracks questions, answers, and associated metrics.
- **Feedback Collection**: Allows users to provide feedback on the quality of interactions.
- **Analytics Dashboard**: Provides insights into conversation metrics and feedback statistics.
- **Real-Time Monitoring**: Displays recent conversations and feedback for quick assessment.

## How we built it

We built Course Assistant using a combination of modern technologies to ensure robustness and scalability:

- **Backend**: Developed with Python, utilizing the `mysql-connector-python` library to interact with TiDB, a distributed SQL database.
- **Database**: TiDB was chosen for its high availability and scalability, with SSL/TLS for secure connections.
- **Frontend**: Streamlit was used for creating an interactive web application for users to interact with the data and visualize metrics.
- **Deployment**: Docker was employed for containerization, ensuring consistent environments across development and production. Terraform was used for managing infrastructure as code, facilitating automated deployments.

## Challenges we ran into

Throughout the development of Course Assistant, we encountered several challenges:

- **Database Connection Issues**: We faced difficulties with TiDB connections and authentication, which required thorough debugging and configuration of SSL/TLS settings.
- **Data Security**: Ensuring secure communication with the database and proper handling of sensitive information was a significant concern.
- **Integration Difficulties**: Integrating the backend with the frontend and ensuring smooth data flow between the components required careful design and testing.

## Accomplishments that we're proud of

We are particularly proud of:

- **Seamless Integration**: Successfully integrating various technologies into a cohesive solution.
- **Real-Time Analytics**: Implementing real-time monitoring and analytics features that provide valuable insights into course interactions.
- **User-Friendly Interface**: Developing an intuitive frontend with Streamlit that simplifies interaction with complex data.

## What we learned

During the project, we learned:

- **Effective Debugging**: Techniques for troubleshooting database connection issues and SSL/TLS configurations.
- **Secure Data Handling**: Best practices for managing sensitive data and ensuring secure connections.
- **Technology Integration**: Insights into integrating various technologies, from databases to containerization and deployment tools.

## What's next for Course Assistant

The future of Course Assistant includes:

- **Enhanced Features**: Adding more advanced analytics and reporting capabilities.
- **User Feedback**: Incorporating user feedback to improve the application’s usability and performance.
- **Scalability**: Exploring further optimizations to handle larger datasets and more concurrent users.

## Built with

- **Programming Language**: Python
- **Backend**: `mysql-connector-python`, `pymysql`
- **Database**: TiDB
- **Frontend**: Streamlit
- **Containerization**: Docker
- **Infrastructure**: Terraform

## Contributing

We welcome contributions to the Course Assistant project! To get started, please fork the repository and submit a pull request with your changes. For detailed guidelines, refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to thank the TiDB community and the Streamlit team for their support and excellent documentation, which greatly facilitated the development process.
