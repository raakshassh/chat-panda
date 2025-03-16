# Chat Panda

Chat Panda is an AI-powered chatbot built using Flask and OpenRouter's LLM model, designed for intelligent and conversational interactions. The project is deployed on Render and integrates Cloudflare's image generation model. 

## Features
- AI-powered chatbot using OpenRouter API
- Flask-based backend for handling requests
- Cloudflare's image generation model integration
- Deployed on Render with CI/CD pipeline

## Tech Stack
- **Backend:** Flask
- **AI Model:** OpenRouter API
- **Image Generation:** Cloudflare
- **Deployment:** Render
- **CI/CD:** Automated deployment pipeline

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Git
- Virtual Environment (recommended)

### Clone the Repository
```sh
git clone https://github.com/raakshassh/chat-panda.git
cd chat-panda
```

### Set Up Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file in the project root and add your API keys:
```sh
OPENROUTER_API_KEY=your_openrouter_api_key
CLOUDFLARE_IMAGE_API_KEY=your_cloudflare_api_key
```

### Run the Application
```sh
flask run
```

## Deployment
Chat Panda is deployed on Render. To deploy your own version:
1. Push the code to GitHub.
2. Connect the repository to Render.
3. Configure environment variables on Render.
4. Enable automatic deployments.

## CI/CD Pipeline
- Uses Render’s built-in deployment system.
- Automates build and deployment processes.

## Future Enhancements
- Improve chatbot responses with fine-tuned AI models.
- Enhance UI for a more interactive experience.
- Optimize image generation latency.

## Contributing
Contributions are welcome! Feel free to submit pull requests or report issues.

## License
This project is licensed under the MIT License.

## Contact
For questions, reach out via [GitHub Issues](https://github.com/raakshassh/chat-panda/issues) or email.

---
### ⭐ Star the Repository
If you find this project useful, consider giving it a ⭐ on [GitHub](https://github.com/raakshassh/chat-panda)! It helps others discover it and motivates further development.

