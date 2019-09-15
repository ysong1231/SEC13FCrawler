# About the project
This Python3 program is designed for crawling 13F information tables from SEC using CIK. 

## How to Use
To run the project, simply go to terminal/cmd and run:
    python SEC_13F_crawler.py

The project will take three input values: 
    1) CIK
    2) Date
    3) Download path
The program will automatically find the most recent 13F file of the given CIK before the given date, and download the write the table to .tsv file under the given download path.

CIK cannot be null, or the program will raise an error; Date can leave blank and the program will find the most recent 13F file; Download path can also be blank and the tsv file will be saved to current directory, same to the .py file.

## Project Functions
There are 4 major functions within the project.

1) generate_url function: 
    This function takes 3 parameters: CIK, file_type, and date_before. CIK is a positional argument, and file_type and Date_before are key-word arguments with default value of "13F-HR" and "". 

    file_type will enable users to search for different documents, but has not realized yet.

    This function will generate the URL for crawling.

2) get_xml function:
    This function takes url as the only posinal argument, which is the URL the project will begin with.

    Since this project uses selenium, the headless argument will provide the option to run the program in headless version or not.

    This function will find and return the URL of the .xml file we want, as well as the filing date of the file.

3) parse_xml function:
    This function takes only one positional argument, which is the xml file's URL. 

    Each row/record within the xml file will be transfered into a dictionary, and the table will be stored using a list of dictionaries.

    The function will return the list of dictionaries.

4) write_to_file function:
    This function will write the list of dictionaries into tsv file using dataframe, use the given name and date as the file name, and write the file to the given path.

    This function has no return value.

## Further Improvement
1) There is no entry validations for the input.
2) Searching for file types other than 13F hasn't   been realized. 
3) The project doesn't raise errors.
4) The project uses xpath to locate the xml files in get_xml function, which may cause errors under special circumstances.
5) The project uses hard coding to create the intial dataframe in write_to_file function, and this may cause errors for unstructured xml files or files under different format. 