# Chatbot Testing System

This project is designed to evaluate how well a chatbot understands and responds to both original and paraphrased questions. It uses the PEGASUS model to generate paraphrased test inputs and compares the chatbot’s accuracy and response time across different variations of the same query.

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/nadeemghafoori/chatbot-testing-system.git
   ```
2. Navigate to the project folder:
   ```bash
   cd chatbot-testing-system
   ```
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   python run.py
   ```
6. After running, check the terminal output for something like `Running on http://127.0.0.1:5000/`, Open that URL in your browser to view it.
