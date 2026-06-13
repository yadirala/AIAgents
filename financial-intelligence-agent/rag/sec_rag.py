import requests
import os
from gateway.llm_gateway import call_llm
import json
from edgar import Company
import re
from bs4 import BeautifulSoup


def fetch_sec_filing(cik):
    headers = {"User-Agent": "yashwanthadirala@gmail.com"}
    
    # get filing metadata
    url = f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json"
    data = requests.get(url, headers=headers).json()
    
    filings = data["filings"]["recent"]
    for i, form in enumerate(filings["form"]):
        if form == "10-K":
            accession = filings["accessionNumber"][i].replace("-", "")
            primary = filings["primaryDocument"][i]
            # correct URL format
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{primary}"
            response = requests.get(filing_url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.get_text()
    
    raise ValueError(f"No 10-K found")

def split_by_sections(text):
    search_start = len(text) // 10
    search_text = text[search_start:]
    section_patterns = {
        "business_overview": r"item\s+1[\.\-\:]\s*business",
        "risk_factors": r"item\s+1a[\.\-\:]\s*risk\s+factors",
        "mda": r"item\s+7[\.\-\:]\s*management",
        "financial_statements": r"item\s+8[\.\-\:]\s*financial\s+statements"
    }
    
    # find start position of each section
    found_sections = {}
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, search_text, re.IGNORECASE)
        if match:
            found_sections[section_name] = match.start() + search_start
    
    # sort sections by position in document
    sorted_sections = sorted(found_sections.items(), key=lambda x: x[1])
    
    # extract text between each section
    sections = {}
    for i, (section_name, start_pos) in enumerate(sorted_sections):
        if i + 1 < len(sorted_sections):
            end_pos = sorted_sections[i + 1][1]
        else:
            end_pos = len(text)
        sections[section_name] = text[start_pos:end_pos].strip()
    
    return sections

def summarize_section(section_text):
    response = call_llm([
        {"role": "system", "content": "You are a financial analyst. Summarize the following section from a 10-K filing in 2-3 concise sentences, focusing on key points relevant for investment risk analysis."},
        {"role": "user", "content": section_text[:4000]}
    ])
    return response.strip()

def get_cik(ticker):
    """Get the CIK for a given ticker symbol."""
    headers = {"User-Agent": "yashwanthadirala@gmail.com"}
    url = f"https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=headers)
    data = response.json()

    for item in data.values():
        if item["ticker"] == ticker.upper():
            return item["cik_str"]

    raise ValueError(f"CIK not found for ticker: {ticker}")

def build_index(filing_content, company):
    # check cache first
    if os.path.exists(f"{company}_index.json"):
        with open(f"{company}_index.json", "r") as f:
            return json.load(f)
    
    # split into sections
    sections = split_by_sections(filing_content)
    
    # build two-level index
    index = {}
    for section_name, section_text in sections.items():
        if section_text:
            summary = summarize_section(section_text)
            index[section_name] = {
                "summary": summary,
                "content": section_text[:8000]  # store first 8000 chars of full content
            }
    
    # save to cache
    with open(f"{company}_index.json", "w") as f:
        json.dump(index, f)
    
    return index