from service.consultHTTP import consult_page1, consult_page2, consult_page3
import os

async def run_pipeline():
    #age1_data = await consult_page1()
    page2_data = await consult_page2()
    #age3_data = await consult_page3()



    return page2_data