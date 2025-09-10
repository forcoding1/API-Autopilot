API Autopilot 🤖✈️
An autonomous AI agent that turns API documentation into ready-to-use Python clients.

## Overview
API Autopilot is an advanced agentic AI project designed to eliminate the tedious and error-prone task of integrating third-party APIs. By simply providing a link to an API's documentation and a high-level goal, the agent autonomously scrapes and understands the API's structure, generates a robust and ready-to-use client library, and saves it as a local Python file.

This tool acts as a force multiplier for developers, turning hours of manual work—reading docs, writing boilerplate, and structuring code—into a process that takes just minutes.

## Key Features
Autonomous Web Scraping: Uses Playwright to reliably fetch content from both static and dynamic, JavaScript-heavy documentation sites.

Intelligent Information Extraction: Leverages a Google Gemini model to read the scraped text and intelligently extract structured information about API endpoints, parameters, and functionality based on the user's task.

Automated Code Generation: Translates the structured API information into a clean, well-documented, and functional Python client class.

Stateful Workflow: Orchestrated by LangGraph, the entire process is managed as a stateful graph, ensuring a clear and extensible workflow from scraping to file generation.

## How It Works
The agent operates through a simple yet powerful workflow orchestrated by LangGraph.

Scrape & Understand (scrape_content node):

The agent takes a URL and a task (e.g., "get pokemon abilities").

Playwright navigates to the URL, waits for all dynamic content to load, and extracts the clean text.

Gemini analyzes this text to identify the API's title and the specific endpoints needed to accomplish the user's task, outputting a structured APIDescription.

Generate Code (code_gen node):

The structured APIDescription is passed to the next node.

Gemini uses a specialized prompt to transform this structured data into a high-quality Python client class, complete with methods, docstrings, and error handling.

Write to File (file_writer node):

The generated code is received from the previous step.

The agent creates a new file named after the API (e.g., PokeAPI.py) and writes the complete, ready-to-use client library to disk.

## Installation
Clone the repository:

Bash

git clone https://github.com/your-username/api-autopilot.git
cd api-autopilot
Install Python dependencies: dependencies available in pyproject.toml
Install Playwright browser

## Configuration
This project requires a Google API key to use the Gemini model.

Create a .env file in the root of the project directory.

Add your API key to the file:

GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
## Usage
Run the application from your terminal.

Start the agent:

Bash

python main.py
Provide the task: The agent will prompt you for your objective.

Developer Tools query: Create a python client to get pokemon abilities
Provide the URL: Next, enter the URL for the API documentation.

Resource (web link, swagger html, etc...): https://pokeapi.co/docs/v2
The agent will then execute its workflow. Upon completion, you will find a new Python file (e.g., PokeAPI.py) in your project directory.

## Future Roadmap
This initial version provides a solid foundation. Future development will focus on making the agent even more autonomous and powerful:

Implement a Self-Correction Loop: Add test and debug nodes to the graph, allowing the agent to execute its generated code, analyze failures, and automatically fix its own bugs.

Support for OpenAPI/Swagger: Enable the agent to directly parse structured OpenAPI specifications for more accurate and faster client generation.

Advanced Refactoring: Give the agent the ability to integrate its generated code into an existing codebase rather than just creating a new file.

Interactive Credential Handling: Allow the agent to pause and ask for API keys if it discovers they are needed during the testing phase. ---ADDED.
