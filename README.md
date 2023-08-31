# Retrofit and OkHttp3 Annotation Analyzer

Retrofit and OkHttp3 Annotation Analyzer is a Python script that facilitates the analysis of Android APKs, extracting Retrofit HTTP method annotations and OkHttp3 variables from the smali code. This tool provides insights into the API endpoints and network-related components used within the APK, allowing for easy examination and integration into different toolsets.

## Features

- Extracts Retrofit HTTP method annotations and OkHttp3 variables from smali code.
- Supports both APK files and smali folders as input.
- Generates output in user-friendly text or Postman collection JSON format.

## Usage

1. Clone this repository or download the script.
2. Make sure you have `apktool` installed on your system.
3. Run the script with command-line options to analyze APKs or smali folders and specify output preferences.

## Output Formats

- Text Format: Provides annotations and variables in a readable text format.
- Postman Collection Format: Outputs annotations in a JSON format compatible with Postman collections.

## Getting Started

To get started, follow these steps:

1. Install `apktool` if you haven't already.
2. Clone this repository or download the `analyze_annotations.py` script.
3. Open your terminal or command prompt.
4. Navigate to the directory containing the script.
5. Run the script using the provided options. Example:

   ```shell
   python analyze_apk.py -apk my_app.apk -o output.txt
