from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import httpx
import time

#Creating FastAPI app
app = FastAPI()

#CORS middleware to allow requests (not required for vercel deployment, local testing only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#@ is a decorator. Tells FastAPI when given url is visited to run the function below.
@app.get("/api/audit")
async def audit_url(url: str):

    #1. Check for making sure they provide a full URL
    if not url.startswith("http://") and not url.startswith("https://"):
        raise HTTPException(status_code=400, detail="URL must begin with https:// or http://")

    start_time = time.time()  # Start the timer
    
    try:
        #Fetching page
        #5s timeout to prevent vercel function from crashing
        #follow_redirects=True ensures links are followed (http -> https)
        #additional feature: preventing 403Forbidden by emulating a browser

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }


        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0, follow_redirects=True, headers=headers)

        #check if  website returns an error (eg. 404)
        response.raise_for_status()

        #check if page is HTML and not a pdf or image
        content_type = response.headers.get("content-type", "")
        if "text/html" not in content_type:
            raise HTTPException(status_code=400, detail="URL does not point to an HTML page")

        #Parsing with BeautifulSoup
        #Load HTML into bs
        soup = BeautifulSoup(response.text, "html.parser")

        #Get Title
        title = soup.title.string.strip() if soup.title and  soup.title.string else "Title not found"

        #Get Meta Description
        meta_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else "Description not found"

        #H1 Tags
        h1_no = len(soup.find_all("h1"))

        #images missing alt text
        images_without_alt = sum(1 for img in soup.find_all("img") if not img.get("alt") or img.get("alt").strip())

        #Word count
        visible_text = soup.get_text(separator="", strip=True)
        word_count = len(visible_text.split())

        #stop timer and convert to ms
        response_time_ms = round((time.time() - start_time) * 1000)



        #if all tests passed, return basic info (temporary)
        return{
            "status": response.status_code,
            "response_time_ms": response_time_ms,
            "title": title,
            "meta_description": meta_desc,
            "h1_count": h1_no,
            "images_missing_alt": images_without_alt,
            "word_count": word_count
        }
    
    #catching other exceptions
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timed out")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Error occured while fetching URL. Please check if the URL is correct")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Website returned an error: {e.response.status_code}{e.response.reason_phrase}" )
