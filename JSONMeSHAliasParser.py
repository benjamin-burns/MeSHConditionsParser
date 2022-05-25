import json
import csv

def parseFile(inputFile, out):
    '''
    Parses input JSON data given by {inputFile} and appends condition alias mapping data 
    for all properly formatted conditions in {inputFile} to {out}.

        Parameters:
            inputFile (str)
                    file path of JSON input file
            out (DictWriter)
                    output stream to csv file

        Updates:
            out

        Requires:
            {inputFile} is a valid file path to a readable JSON file in proper MeSH Data format,
            {out} is open,
            {out} is a writable file, and
            {out} has a valid csv header with two features

        Ensures:
            The content of {out} is updated to contain all condition alias mappings contained in 
            {inputFile}. If the input file cannot be opened or read, an error is thrown and 
            program execution stops
    '''
    # Open and read in data from {inputFile}
    try:
        with open(inputFile, "r") as input:
            try:
                rawData = input.read()
            except UnicodeDecodeError:
                print("Error: there is something wrong with input formatting in " + inputFile)
                exit()
    except OSError:
        print("Error: could not open file " + inputFile);
        exit()

    data = json.loads(rawData)
    
    for term in data:
        row = {}
        row["term"] = term
        for alias in data[term]["entry_terms"]:
            row["alias"] = alias
            out.writerow(row)

def main():
    '''
    Main method for JSONMeSHAliasParser.
    Outputs a csv file with mappings between MeSH terms aliases and MeSH terms for conditions.
    All input text is converted to lowercase except MeSH codes. Otherwise, output strings are as
    exactly as they appear in input.

    Data is read in from a preprocessed JSON file with relative path {DATA_FILE}.
    Output file is named {OUTPUT_FILE_PATH} and follows formatting {FIELD_NAMES}.
    If output file already exists, all data will be overridden.
    '''
    # Configuration constants
    DATA_FILE = "MeSHConditions.json"
    OUTPUT_FILE_PATH = "aliasToTerm.csv"
    FIELD_NAMES = ["alias", "term"]

    outputFile = open(OUTPUT_FILE_PATH, 'w', encoding='utf-8')
    writer = csv.DictWriter(outputFile, fieldnames=FIELD_NAMES)
    writer.writeheader()

    # Parse and print data from input file
    parseFile(DATA_FILE, writer)

if __name__ == "__main__":
    main()
