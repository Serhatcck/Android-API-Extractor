import os
import re
import argparse
import subprocess
import json

def process_smali_files(folder_path):
    http_annotations = []
    okhttp3_variables = []

    annotation_pattern = re.compile(r'\.annotation runtime Lretrofit2/http/([A-Z]+);([\s\S]*?)\.end annotation')
    okhttp3_pattern = re.compile(r'\.field .*? Lokhttp3/')

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.smali'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as smali_file:
                    content = smali_file.read()
                    http_annotations.extend(annotation_pattern.findall(content))
                    okhttp3_variables.extend(okhttp3_pattern.findall(content))

    return http_annotations, okhttp3_variables

def parse_apk(apk_path):
    try:
        subprocess.run(["apktool", "d", apk_path])
        return True
    except Exception as e:
        print("APK parsing failed:", e)
        return False

def generate_txt_output(http_annotations, okhttp3_variables, output_file):
    result = ""
    if http_annotations:
        result += "HTTP Method Annotations:\n"
        for annotation in http_annotations:
            http_method = annotation[0].strip()
            value = annotation[1].strip()
            result += f"HTTP Method: {http_method}\n"
            result += f"Value: {value}\n\n"

    if okhttp3_variables:
        result += "OkHttp3 Variables:\n"
        for variable in okhttp3_variables:
            variable_name = variable.strip()
            result += f"OkHttp3 Variable: {variable_name}\n\n"

    with open(output_file, 'w') as file:
        file.write(result)
    print(f"Output file created: {output_file}")

def generate_postman_output(http_annotations, output_file):
    postman_collection = {
        "info": {
            "name": "Retrofit Analysis",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    if http_annotations:
        http_item = {
            "name": "HTTP Method Annotations",
            "item": []
        }

        for annotation in http_annotations:
            http_method = annotation[0].strip()
            value = annotation[1].strip()

            request_item = {
                "name": f"HTTP Method: {http_method}",
                "request": {
                    "method": http_method,
                    "url": "{{base_url}}" + value
                }
            }

            http_item["item"].append(request_item)

        postman_collection["item"].append(http_item)

    with open(output_file, 'w') as file:
        json.dump(postman_collection, file, indent=2)
    print(f"Output collection JSON file created: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Retrofit and OkHttp3 Annotation Analyzer')
    parser.add_argument('-apk', '--apk-path', help='Path to the APK file')
    parser.add_argument('-s', '--smali-folder', help='Path to the smali folder')
    parser.add_argument('-o', '--output-file', help='Path to the output file')
    parser.add_argument('-f', '--output-format', choices=['txt', 'postman'], default='txt', help='Output format (txt or postman)')
    args = parser.parse_args()

    apk_path = args.apk_path
    smali_folder_path = args.smali_folder
    output_file = args.output_file
    output_format = args.output_format

    if apk_path and not smali_folder_path:
        apk_name = os.path.splitext(os.path.basename(apk_path))[0]
        if parse_apk(apk_path):
            smali_folder_path = os.path.join(os.getcwd(), apk_name)

    http_annotations = []
    okhttp3_variables = []

    if smali_folder_path:
        http_annotations, okhttp3_variables = process_smali_files(smali_folder_path)

    if output_format == 'postman':
        generate_postman_output(http_annotations, output_file)
    else:
        generate_txt_output(http_annotations, okhttp3_variables, output_file)

if __name__ == "__main__":
    main()
