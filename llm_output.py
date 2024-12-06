from openai import OpenAI
import pandas as pd
import csv
import os
import time


GPToutputlist = []
abstract_processedlist = []
title_processedlist = []
counts = 0

def extract_high_entropy_elements(abstract, ti):
    api_key = "your api_key"
    base_url = "your base_url"

    try:
        client = OpenAI(api_key=api_key,
                        base_url=base_url)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a research chemist focus on Cu-based catalysts for CO2 reduction."},
                {"role": "user", "content": f" Cu-based catalysts usually refer to catalysts with Cu as the main component and doped with other elements. "},
                {"role": "user", "content": f"Electrocatalytic CO2 reduction refers to the process of converting CO2 into more valuable chemicals (such as carbon monoxide, formic acid, methanol, ethanol, or other hydrocarbons) and fuels through an electrochemical method facilitated by a specific electrocatalyst at the electrode surface. This process is driven by externally applied electrical energy and can operate under relatively mild conditions, offering enhanced selectivity and reaction rates."},
                {"role": "user", "content": f"According to previous result, CO2 reduction could be misunderstood with CO reduction , but it is not."},
                {"role": "user", "content": f"I will submit Abstract of a research article ,identify if this article is studying CO2 reduction: if yes,reply'yes';if not, reply'No"},
                {"role": "user", "content": f"Analysis the detail research field of this article, identify if this article is studying catalyst or catalytic: if yes,reply'Catalytic Research';if not, reply'Other Research'"},
                {"role": "user", "content": f"Analysis the specified research field of this article, identify if this article is studying electrocatalytic CO2 reduction : if yes,reply'Research on CO2RR';if not, reply'Other Research"},
                {"role": "user", "content": f"If this abstract from the article studies electrocatalytic CO2 reduction,recognize it is a review article or a research article, reply 'research' or 'review',if don't belong to both, reply 'NULL"},
                {"role": "user", "content": f"If this abstract from a research article, summarize the abstract and analysis the metal elements that authors choosen as the compound of Cu-based catalysts they investigated, if there were no metal elements mentioned or Empty Input or any information is not provided or you are unsure, reply 'NULL'"},
                {"role": "user", "content": f" Abstact:{abstract}"},
                {"role": "user", "content": f" title:{ti}"},
                {"role": "user",
                 "content": f" Your answer should be standardized with the following chart: \nArticle research on CO2 reduction or not:\nDetailed Research Field:\nSpecified Research Field:\nArticle Type: Research or Review\nElements: 1, 2, 3, \n. To be noted, if you are unsure, please reply 'NULL', and the elements should be symbolized with English abbreviation only, for example, if the elements are Iron, Cobalt, Nickel, please reply 'Fe, Co, Ni'"},
                {"role": "user",
                 "content": f" Please check your answer, read the abstract and title again and reply again"},
                 ],
            timeout=10.0,  # 设置超时时间（以秒为单位），这里设置为10秒
        )

        return response.choices[0].message.content.strip()
    except:
        return "API time out"



for file in os.listdir(datapath):
    file = os.path.join(datapath, file)

    with open(file, newline='', encoding='utf-8') as csvfile:

        reader = pd.read_excel(file, sheet_name=0, header=0, index_col=0)

        for row in range(len(reader['Abstract'])):
            title_list = reader['Article Title'].values
            abstract_list = reader['Abstract'].values
            abstract = abstract_list[row]
            ti = title_list[row]
            counts += 1
            if counts > 0:
                GPToutput = extract_high_entropy_elements(abstract, a)
                a += 1
                if a == 4:
                    a = 1

                while GPToutput == "API time out":
                    time.sleep(20)
                    GPToutput = extract_high_entropy_elements(abstract, a)
                    print(f"API time out，waiting for 20s to request again")


                GPToutputlist.append(GPToutput)
                abstract_processedlist.append(abstract)
                title_processedlist.append(title_list[row])

                print(f"Title：{title_list[row]}")
                print(f"GPToutput：{GPToutput}")
                print("-" * 50)
