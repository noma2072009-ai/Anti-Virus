# This is the first step in programming an antivirus.
# The program receives a path and checks whether it exists on the computer.
# If the path exists, it prints the names of all files that can be accessed from it (including files in subfolders).
# If the path does not exist, it prints an appropriate error message. 




# The library allows us to create Path objects, which represent file system paths and give us useful methods and properties to work with them.
# exists(): checks if the path exists.
# is_dir(): checks if the path is a directory (folder).
# iterdir(): returns an iterator of all files and folders inside the given directory.
# (iterator: an object that gives values one at a time instead of all at once.)
# parent: returns the parent directory (the folder that contains the file or folder).
# name: returns the name of the file or folder.
from pathlib import Path 



# This recursion function that print all the files that are accessible with the received path with a message according to where it's 
def print_files_names (path):

    for f in path.iterdir():
        
        if f.is_dir():
            print_files_names(f)
        else:
            
            print(f"In the folder with name ({f.parent.name}) there is a file with the name: {f.name}")
              



def main():
     
    # Receiving a path from the user and craete a Path object with this path
    path = Path(input("Please enter a path: "))

    # Checks if the path exists if it is , all the names of the accessible files with this path will be printed ,if is not ,the user wiil get an appropriate message
    if path.exists():
      print_files_names(path)
    else:
     print("This path does not exist")
    
    

    

    
if __name__ == "__main__":
    main()
    
   