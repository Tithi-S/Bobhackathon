from crewai import Agent
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool,
    SeleniumScrapingTool,
    ScrapeWebsiteTool
)

docs_tool = DirectoryReadTool(directory='./blog-posts')
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

# Topic Researcher Agent
topic_researcher = Agent(
    role='Topic Researcher',
    goal='Conducts research for understanding the format for writing a new blog by going through various existing blogs and extracts the primary and secondary keywords',
    verbose=True,
    memory=True,
    backstory="You are an expert researcher, skilled in finding and synthesizing information from various sources.",
    tools=[search_tool, web_rag_tool], 
    allow_delegation=True
)

blog_writer = Agent(
    role='Blog Writer',
    goal='Crafts a blog post using information from external research and extracted product details to market the products.',
    verbose=True,
    memory=True,
    backstory="You're a senior writer at a company named McGrocer. You are responsible for creating content to the business. You are currently working on creating long blogs that provides information to the people along with publicising the product as a solution",
    tools=[],
    allow_delegation=False
)

product_extractor = Agent(
    role = 'Content reviewer',
    goal = 'In the provided keywords, extract the name of the products from the keywords',
    verbose = True,
    memory = True,
    backstory = '',
    tools = [],
    allow_delegation = False
)

Editor = Agent(
    role = 'Content editor',
    goal = 'In the provided blog, embed the provided product links with their products to enhance the user experience',
    verbose = True,
    memory = True,
    backstory = 'You are a very experienced online blog editor with experience of user experiences. You mainly work in embedding the products with their links in the blogs',
    tools = [],
    allow_delegation = False
)
