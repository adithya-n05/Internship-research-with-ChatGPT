import aiohttp
import asyncio
import pandas as pd
import base64
import os
import openai

finance_related = ["BP", "Bloomberg", "Capstone", "Citadel", "Crédit Agricole", 
    "D.E. Shaw", "Deloitte", "DRW", "EY", "Goldman Sachs", "G-Research", 
    "HSBC", "Hudson River Trading", "IMC Trading", "J.P. Morgan", 
    "Jane Street", "Jefferies", "Jump Trading", "KPMG", "Macquarie Group", 
    "Mastercard", "Mizuho", "Morgan Stanley", "MUFG", "Nomura", "Optiver", 
    "PIMCO", "Point72", "Qube RT", "Scotiabank", "Susquehanna International Group", 
    "The Trade Desk", "Two Sigma", "UBS", "Vanguard", "Addepar", 
    "Baillie Gifford", "Balyasny Asset Management", "BGC Partners", 
    "Caxton Associates", "Cboe Global Markets", "Castleton Commodities International", 
    "FactSet", "Financial Conduct Authority", "GSA Capital", 
    "ICBC Standard Bank", "Man Group", "MarketAxess", "Marsh McLennan", 
    "M&G", "Natwest Markets", "PA Consulting", "RBC Capital Markets", 
    "S&P Global", "Schonfeld", "Squarepoint Capital", "Talos", 
    "TD Securities", "Tradeweb", "TP ICAP", "Willis Towers Watson"
]

tech_related = [
    "Amazon", "Apple", "BT", "Cisco", "Cloudflare", 
    "Epic Games", "Facebook", "Google", "HP", "IBM", 
    "Microsoft", "Netflix", "Netcraft", "Oracle", "Palantir", 
    "Siemens", "Spotify", "Tesla", "The Walt Disney Company", 
    "TikTok", "MathWorks", "Accelercom", "Angstrom Sports", 
    "BAE Systems", "Centrica", "Five AI", "Frazer-Nash Consultancy", 
    "FSP", "Galaxy", "Graphcore", "Hiscox", "HME", 
    "Jacobs", "King", "McLaren", "National Highways", 
    "Nutanix", "NXP Semiconductors", "Ocado", "PredictX", 
    "QinetiQ", "Quantcast", "Renishaw", "Ripple", "Rolls-Royce", 
    "Softwire", "Speechmatics", "Squarepoint Capital", "TE Connectivity", 
    "Tesco", "Terra", "Textron", "Thales", "UK Atomic Energy Authority", 
    "Universal Music Group", "Verisk"
]

openaikey = os.getenv("OPENAI_API_KEY")

async def fetch(session, url, payload):
    async with session.post(url, json=payload) as response:
        response_json = await response.json()
        
        if 'choices' in response_json and len(response_json['choices']) > 0:
            content = response_json['choices'][0].get("message", {}).get("content", "No content found")
        else:
            content = "No valid response received"
        
        print(content)
        
        return content

async def main(companylist):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Authorization': f'Bearer {openaikey}',
        'Content-Type': 'application/json',
    }
    
    df = pd.read_excel('Trackr Application Tracker 2024-25 Technology.xlsx')
    prompts = []

    for index in range(len(companylist)):
        prompts.append(f"""[no prose]
                       
        Please refer to the data for {companylist[index]} in the excel file I will attach below in base64 encoding. I wish to create a markdown file for this company containing detailed information about the company in the a format provided below. I have placed instructions for what you will need to fill out for each section inside [] (square brackets). I would like for you to conduct research for each section again if it states that research should be conducted. Please pay attention to the information in the excel file. The data that should be pulled from the excel file is explicitly stated in the template below and you should follow the rules I provide. Fill in the data from the excel file for sections where I say you should using the data in the excel file I will provide below in base64 encoding. Please ensure to only provide a markdown file style response with no prose from you. I do not want "```markdown" and "```" either. I just want the markdown rseponse for the file using the format below. I want long detailed research to be added and I want you to add as much data as possible to the output:

        # [Company name from sheet]

        ## **Programme Name:** [Programme name from sheet]
        - **Opening Date:** [Opening date from sheet. If no opening date is available, state "To be opened"]
            - Last Year Opening Date: [Last Year Opening Date from Sheet to be added here if Opening date is "To be opened". If Opening date is not "To be opened" remove this bullet point.]
        - **Closing Date:** [State if it is on Rolling basis or not and do research online to find out what the usual closing date in past years were if no explicit closing date is available on the sheet.]
        - **Website:** [Add a link to their careers page]
        - **CV**: [State if required or not from the sheet]
        - **Cover Letter**: [State if required or not from the sheet]
        - **Written Answers**: [State if required or not from the sheet]
        ### Application process and interview timeline:
        [Provide a bullet point list on the stages of interviews this company goes through for this role based on research online. I want a breakdown step by step of each stage.]


        ## Research:

        ### General information:
        - Industry: [Industry of the company]
        - Headquarters: [Location of company's headquarters]
        - Number of Employees: [Estimated number of employees]
        - Website: [Link to the company's website]

        ### Key facts (General):
        [Fill in 5 bullet points here using your research on key facts about the company. Information may be about founding date, what the company does, where they stand in the world and other interesting information. This should do with interesting information on the company that is interesting and not just general information.]

        ### Key facts (UK specific):
        [Fill in 5 bullet points, again using your research that have to do with the UK branch of the company and information about how the UK plays a role for the company and what they are trying to do here etc.]

        ### Company culture and values
        [Fill in information about the values of the company and what the company prioritises and tries to focus on within the company. I want a very blunt response with no sugar coating on what their reputation is in terms of behaviour, what they are known for in terms of good and bad things too.]
            **Employee reviews:**
            [Fill in multiple employee reviews from Glassdoor, indeed, cunchbase, levels.fyi and many other sites on what employees generally say about the company and highlight the negatives to keep in mind especially. Ensure to quote the reviews you choose to use here.]

        ### Technologies and tools
        [Provide information about the frameworks the company uses, the languages they use and the reason they choose to use these languages. Also provide information on how they apply these technologies and where they apply them. Also provide information on the type of internal projects they work on with examples.]

        ### Interview experience research
        [Leave this section empty for me to fill in]

        **Sources:**
        [List all the sources you use here]
        
        Here is data corresponding to this company below and data corresponding to the headers from the excel file:
        {df.columns.values}
        {df.loc[df['Company Name'] == companylist[index]]}

        """)
            
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for i, prompt in enumerate(prompts):
            payload = {
                "model": "gpt-4",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            task = asyncio.create_task(fetch(session, url, payload))
            task.add_done_callback(lambda future: print(future.result()))  
            tasks.append(task)
            await asyncio.sleep(30)

        responses = await asyncio.gather(*tasks)

        for i, response in enumerate(responses):
            with open(f"{companylist[i]}.md", "w") as markdownfile:
                markdownfile.write(response)

asyncio.run(main(tech_related))