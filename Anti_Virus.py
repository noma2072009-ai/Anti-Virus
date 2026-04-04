




# The library allows us to create Path objects, which represent file system paths and give us useful methods and properties to work with them.
# exists(): checks if the path exists.
# is_dir(): checks if the path is a directory (folder).
# iterdir(): returns an iterator of all files and folders inside the given directory.
# (iterator: an object that gives values one at a time instead of all at once.)
# parent: returns the parent directory (the folder that contains the file or folder).
# name: returns the name of the file or folder.
from pathlib import Path 

import time 


import requests 



virus_total_api_scan_url = 'https://www.virustotal.com/vtapi/v2/file/scan'
virus_total_api_key = "50c3e05ae1923bab96c10f74a33e8497fcd8602bc438b03e94b7bed289bb2d44"

virus_total_reports_url = virus_total_reports_url = 'https://www.virustotal.com/vtapi/v2/file/report'
files_with_scan_ids = {}
analysis_results = {}





def scan_files (path):
    
    for f in path.iterdir():
        
        if f.is_dir():
            scan_files(f)
        else:
            files_with_scan_ids[f.name]= send_scan_requests(f)

             




def send_scan_requests(file_name):

    params= { "apikey": virus_total_api_key}
    file = {"file": open(file_name, "rb")}

    response = requests.post(virus_total_api_scan_url, params=params,files=file)
    result=response.json()

    return result['scan_id']
    


def get_reports():

     for key in files_with_scan_ids:
         params = {"apikey": virus_total_api_key,"resource":files_with_scan_ids[key]}

         response = requests.get(virus_total_reports_url, params=params)
         if response is None:
             raise Exception("An Unexpected Error has occured in the response ")
         
         if response.status_code == 200:
             
             
             while response.status_code == -2:
                 print("Waiting the analyzing process to be done...")
                 time.sleep(5)

                 response = requests.get(virus_total_reports_url, params=params)
                 if response is None:
                  raise Exception("An Unexpected Error has occured in the response ")
                 


             result = response.json()    
             analysis_results[key] = result['positives']
                     
         elif response.status_code == 204:
             print('Response without content')  
         elif response.status_code == 400:
             print('Bad request. Your request was somehow incorrect')  
         elif response.status_code == 403:
             print("Forbidden. You don't have enough privileges to make the request")     
         elif response.status_code == 429:
             print(" You may have hit the limit for the allowed requsets today")    



def mirroing_the_results():
    for key in analysis_results:
        if analysis_results[key] == 0:
            print(f"There is no viruses in the file with name: {key} ")
        else:
            print(f"There are {analysis_results[key]} virus/es in the file with name: {key} ")                 

     

       
     




def main():

    # Receiving a path from the user and craete a Path object with this path
     path = Path(input("Please enter a path: "))
     print("Sometimes you will see that there is a problem ('Response without content) ,so try again after 30 seconds")

     if path.exists():
         scan_files(path)
         get_reports()
         mirroing_the_results()
         

     else:
         print("The does not exists in this device!")    
         
         


    
    
    

    

    
if __name__ == "__main__":
    main()
    
   