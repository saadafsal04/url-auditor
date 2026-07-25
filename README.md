# URL Auditor

A lightweight webtool that audits any given URL and returns a JSON report. Built with a FastAPI backend and a vanilla JS + Tailwind CSS frontend.

## Live Demo

https://url-auditor-opal.vercel.app/

## Setup & Installation

1. **Clone repository**

2. **Create a virtual environment and activate it: **
python -m venv venv
source venv/Scripts/activate

3. **Install dependancies:**
pip install -r requirements.txt

4. **Run the backend server:**
uvicorn api.main:app --reload

5. **Boot the frontend**

## API Contract
**Endpoint:** 
GET /api/audit?url={target_url}

**Example:**
/api/audit?url=https://www.example.com

**On success (200 OK)**
JSON Body
{
    "status": 200,
    "response_time_ms": 160,
    "title":"Example Page",
    "meta_description":"No description",
    "h1_count":1,
    "images_missing_alt":0,
    "word_count":18
}

**Error Response (400 Bad Request)**
JSON Body
{
    "detail": "URL does not point to an HTML page"
}

**Design Decisions and Reasoning**

1. Python + FASTAPI:
I preferred FASTAPI over node.js + express since python is a more familiar language and offers more versatility. FASTAPI also supports asynchronous routing with httpx, and provide API testing without the need of an external application like POSTMAN or additonal initiliazation like with Scalar.

2. BeautifulSoup4 for parsing
For web scraping, BeautifulSoup4 remains the premier choice. Compared to Selenium, it is faster and more lightweight, consuming less memory and is perfect for scraping HTML. 

3. Vercel
Vercel deployment setup is incredibly intuitive and requires minimal implementation, only requiring a simple vercel.json file. Deploying both frontend and backend becomes easier with Vercel, bringing it into a single deployed project.