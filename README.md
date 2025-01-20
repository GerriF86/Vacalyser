AI-powered talent acquisition app that helps you streamline your hiring process.

## Features

-   Extracts key information from job descriptions (PDF).
-   Generates job ad variations for different audiences and styles.
-   Suggests relevant interview questions.
-   Creates onboarding checklists.
-   Provides insights into company culture, salary benchmarks, and competitor analysis.
-   Uses a local AI model (Llama 3.2) and a FAISS vector database for efficient information retrieval.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    ```
2.  Create a virtual environment (recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate    # On Windows
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Usage

1.  Upload a PDF job description or enter the job title manually.
2.  Review and edit the extracted information.
3.  Provide details about the company and the role.
4.  Use the AI-powered tools to generate job ad variations, interview questions, and more.

## Data

The app uses a FAISS index for efficient similarity search. The index is located in the `vector_databases` directory. The data used to populate the index should be placed in the `data/processed` directory in JSON format.

## Configuration

You can configure the app by modifying the `config.py` file. The following parameters are available:

-   `MODEL_NAME`: The name of the Ollama model to use.
-   `OLLAMA_URL`: The URL of the Ollama API.
-   `DATA_DIR`: The directory containing the processed data.
-   `INDEX_PATH`: The path to the FAISS index file.
-   `DIMENSION`: The dimension of the vectors in the FAISS index.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.