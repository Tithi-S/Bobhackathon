from crewai import Task
from scrap_tool import search_mcgrocer
from agents import *
from tqdm import tqdm
import time
# Task for Topic Researcher

research_task  = Task(
        description = ("""
                        """),
        expected_output='  ',
        agent=topic_researcher,
    )

product_task = Task(
    
    description = ("""

                   """),
    expected_output = "",
    async_execution=False,
    context=[research_task],
    agent = product_extractor
)


Blog_writing_task =  Task(
    
    description = ("""
                        """),
    expected_output=' ',
    agent=blog_writer,
    async_execution=False,
    context=[research_task],  # Pass the research task as context
)
   
def Editor_tasks(product_links):
    print(product_links)
        
    return Task(

    description = (
        """
                    """),
    expected_output = "",
    async_execution=False,
    context=[Blog_writing_task],
    agent = Editor,
    # output_file='blog-posts/apples.html'
    )
    