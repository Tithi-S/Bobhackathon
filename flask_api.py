from flask import Flask, request, jsonify
from crewai import Crew, Process
from tasks import *
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import os

# Set the environment variable for the model
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

app = Flask(__name__)

def get_research_result(query, secondary_keywords):
    crew_research = Crew(
        agents=[research_task.agent],
        tasks=[research_task],
        process=Process.sequential
    )
    research_result = crew_research.kickoff(inputs={'topic': query, 'secondary_keyword': secondary_keywords})
    return research_result

def get_product_result():
    crew_product = Crew(
        agents=[product_task.agent],
        tasks=[product_task],
        process=Process.sequential
    )
    product_result = crew_product.kickoff()
    return product_result

def parse_product_result(product_result_str):
    if not product_result_str or not isinstance(product_result_str, str):
        return []
    product_list = [item.strip() for item in product_result_str.split(',')]
    return product_list


@retry(retry=retry_if_exception_type(Exception), stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_blog_result(query, secondary_keywords, product_link, product_link2, must_include, image_link1, image_link2):
    crew_blog = Crew(
        agents=[Blog_writing_task.agent],
        tasks=[Blog_writing_task],
        process=Process.sequential
    )
    blog_result = crew_blog.kickoff(inputs={
        'topic': query,
        'secondary_keyword': secondary_keywords,
    })
    return blog_result

def get_editor_result(product_links):
    editor_task = Editor_tasks(product_links)
    crew_edit = Crew(
        agents=[editor_task.agent],
        tasks=[editor_task],
        process=Process.sequential
    )
    editor_result = crew_edit.kickoff()
    return editor_result

@retry(retry=retry_if_exception_type(Exception), stop=stop_after_attempt(3), wait=wait_fixed(2))
def generate_blog_post(data):
    query = data.get('request_content')
    secondary_keywords = data.get('secondary_keywords', '')

    if not query:
        return {"error": "request_content field is required"}, 400

    # Get the research result
    research_result = get_research_result(query, secondary_keywords)
    print("Research Result:", research_result)

    # Get the product result
    product_result = get_product_result()
    print("Original product_result:", product_result)

    # Parse product result
    product_names = parse_product_result(product_result)
    print("Product Names:", product_names)

    # Get product links
    product_links = get_product_links(product_names)
    print("Product Links:", product_links)

    # Get the blog result
    blog_result = get_blog_result(query, secondary_keywords)
    print("Blog Result:", blog_result)

    # Get the editor result
    editor_result = get_editor_result(product_links)
    print("Editor Result:", editor_result)
    
    # Return the editor result as the final output
    return editor_result

@app.route('/generate_blog', methods=['POST'])
def generate_blog():
    try:
        data = request.get_json()
        result = generate_blog_post(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
