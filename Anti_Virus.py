

# The library allows us to create Path objects, which represent file system paths and give us useful methods and properties to work with them.
# exists(): checks if the path exists.
# is_dir(): checks if the path is a directory (folder).
# iterdir(): returns an iterator of all files and folders inside the given directory.
# (iterator: an object that gives values one at a time instead of all at once.)
# parent: returns the parent directory (the folder that contains the file or folder).
# name: returns the name of the file or folder.
from pathlib import Path 


# This library allows us to stop the code from runing for a speacifc amount of time (in seconds).
import time 

# This library allows us to send HHTP requests in order to communicate with VirusTotal using an API key.
import requests 


# This the URL for sending the scan requsets for VirusTotal.
virus_total_api_scan_url = 'https://www.virustotal.com/vtapi/v2/file/scan'

# This is a authentication key that allows the VirusTotal to identify us when it receives our requests.
virus_total_api_key = "50c3e05ae1923bab96c10f74a33e8497fcd8602bc438b03e94b7bed289bb2d44"

#This the URL for sending requests for VirusTotal in order to get the reports about the filesthat we have sent for scanning.
virus_total_reports_url = virus_total_reports_url = 'https://www.virustotal.com/vtapi/v2/file/report'

# This dictionary stores the files names as files and the scan ids as values ,that allow us to send a request with the scan id in order to get the report ,so the VirusTotal will identify the required file.
files_with_scan_ids = {}

# This dictionary stores the files names as keys and the number of viruses in each file as values.
analysis_results = {}




# This function receives a path and for each file that can be accessed with this path is sends a request to VirusTotal to scan the file ,then it tsores thhe scan id that can extracted from the response that we get for each file.
def scan_files (path):
    
    for f in path.iterdir():
        
        if f.is_dir():
            scan_files(f)
        else:
            files_with_scan_ids[f.name]= send_scan_requests(f)

             



# This function receives a file name and sends a request with file to VirusTotal in order to scan it and then it returns the scan id for this file that can extracted from the response. 
def send_scan_requests(file_name):

    params= { "apikey": virus_total_api_key}
    file = {"file": open(file_name, "rb")}

    response = requests.post(virus_total_api_scan_url, params=params,files=file)
    result=response.json()

    return result['scan_id']
    

# This recursion function is responsible for the process of sending requests to VirusTotal in order to receive the reports for each file.
# After sending the first request if the status code of the response is not 200 , so there is problem and a proper string message will be printed only if the code is 400,429,403.
# If the status code of the response is 200 ,the function will check if the verbose message that attached with the response in json format is "Your resource is still queued for analysis:" ,if the condition is true that means that the report is not ready yet ,so the function get_reports will start again nad if the condition is false the function will insert the number of viruses in a dictionary as value and its key is the name file(we extract the positives of the report that reffers to the number of the viruses in the file).
# Between ecah time the function runs the code stops for 5 seconds ,the code stop from running for 5 seconds in oreder to give the VirusTotal time to finish the analyzing and in order to keep the code safe from carshing from the enormous number of request that the VirusTotal will recieves ,so it will send us responses with errors.
# After every received response ,the function checks if there is a reponse or not and if not it raise an exeption with a proper message.
def get_reports():

     for key in files_with_scan_ids:
         params = {"apikey": virus_total_api_key,"resource":files_with_scan_ids[key]}

         response = requests.get(virus_total_reports_url, params=params)
         if response is None:
             raise Exception("An Unexpected Error has occured in the response ")
         
         if response.status_code == 200:
             
             result = response.json()

             if result["verbose_msg"] == "Your resource is still queued for analysis:":
                 print(" Waiting for the report to be ready!")
                 time.sleep(5)
                 get_reports()


             analysis_results[key] = result.get('positives', 0)


         elif response.status_code == 204:
             print('Response without content , try again after 30 seconds')  

         elif response.status_code == 400:
             print('Bad request. Your request was somehow incorrect') 

         elif response.status_code == 403:
             print("Forbidden. You don't have enough privileges to make the request")  

         elif response.status_code == 429:
             print(" You may have hit the limit for the allowed requsets today")    



# THis function prints the results of the analysis for each file in a porper string.
def mirroing_the_results():

    for key in analysis_results:

        if analysis_results[key] == 0:

            print(f"There is no viruses in the file with name: {key} ")

        else:

            print(f"There are {analysis_results[key]} virus/es in the file with name: {key} ")                 

     

       
     




def main():

  # Receiving a path from the user and craete a Path object with this path
   path = Path(input("Please enter a path: "))
    
 # This message is for the user because sometimes the VirusToatal will receive a huge number of requests in the same time ,and it will send responses without content because of the huge number of the requests it can not reply to all of them ,so the user need to try again after 30 seconds.
   print("Sometimes you will see that there is a problem ('Response without content) ,so try again after 30 seconds")


# Here intially we check if the path is already exists in the device ,if is not a proper message will be printed.
# If it exists we will call the function scan_files in order to send to the VirusTotal scan requests for each file that can be accessible with this path.
# After this we will call the function get_reports send requets to VirusTotal in order to get the reports for ecah file that we have sent for it a request for scanning.
# Then we call the function mirroing_the_results and it print for ecah file how many viruses exist in it.
   if path.exists():
         
      scan_files(path)
      get_reports()
      mirroing_the_results()
         

   else:
       print("The does not exists in this device!")    
         
         


    
    
    

    

    
if __name__ == "__main__":
    main()
    
   