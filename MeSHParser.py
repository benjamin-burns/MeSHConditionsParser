import json
import xml.etree.ElementTree as ET

def parseCondition(conditionData):
    '''
    Parses input XML data of an individual condition given by {conditionData}
    and returns a list containing the condition term and its condensed JSON representation.

        Parameters:
            conditionData (XML Element)
                    ElementTree Element Object holding condition information from MeSH Data

        Returns:
            A list of
              * Condition name (str)
              * JSON representation of condition data (JSON object) with the formatting
                * mesh_code (str)
                * entry_terms (list of str)

        Requires:
            {conditionData} formatting is consistent with MeSH Data formatting

        Ensures:
            {parseDrug} = [a list of relevant condition data with the formatting described 
            in {Returns}]. If {conditionData} is not consistent with MeSH Data formatting, 
            an error is thrown and program execution stops
    '''
    # Obtain MeSH term
    try:
        term = conditionData.find('DescriptorName').find('String').text.lower()
    except:
        print("Error: could not retrieve MeSH term of condition")
        exit()

    # Obtain MeSH code
    try:
        code = conditionData.find('TreeNumberList').find('TreeNumber').text
    except:
        print("Error: could not retrieve MeSH code of condition")
        exit()

    # Obtain entry terms
    entryTerms = list()
    try:
        conceptList = conditionData.find('ConceptList')
        for concept in conceptList.findall('Concept'):
            termList = concept.find('TermList')
            for termX in termList.findall('Term'):
                termName = termX.find('String').text.lower()
                entryTerms.append(termName)
    except:
        print("Error: could not retrieve brand name data of drug")
        exit()

    # Create and populate condensed JSON representation of drug
    conditionDataRep = {}
    conditionDataRep["mesh_code"] = code
    conditionDataRep["entry_terms"] = entryTerms

    return [term, conditionDataRep]

def isCondition(descriptor):
    '''
    Determines if input XML data of an individual descriptor given by {descriptor}
    is a condition.

        Parameters:
            conditionData (XML Element)
                    ElementTree Element Object holding descriptor information from MeSH Data

        Returns:
            True [if {descriptor} is a condition]
            False [otherwise]

        Requires:
            {descriptor} formatting is consistent with MeSH Data formatting

        Ensures:
            {isCondition} = True [if {descriptor} is a condition], False [otherwise]
    '''
    # Obtain MeSH code
    try:
        code = descriptor.find('TreeNumberList').find('TreeNumber').text
    except:
        print("Error: could not retrieve MeSH code of descriptor")
        return False

    return code[0] == "C"

def parseFile(inputFile, out):
    '''
    Parses input XML data given by {inputFile} and appends conditions data 
    for all properly formatted conditions in {inputFile} to {out}.

        Parameters:
            inputFile (str)
                    file path of DrugBank input file
            out (str)
                    output file path

        Updates:
            out

        Requires:
            {inputFile} is a valid file path to a readable XML file in proper MeSH Data format,
            {out} is open, and
            {out} is a writable file

        Ensures:
            The content of {out} is updated to contain all conditions data contained in 
            {inputFile}. If the input file cannot be opened or read, an error is thrown and 
            program execution stops
    '''
    # Open and read in data from {inputFile}
    try:
        tree = ET.parse(inputFile)
    except:
        print("Error: could not read in data from file " + inputFile);
        exit()

    root = tree.getroot()

    data = {}

    # Parse and append data of each condition in dict object
    for descriptorRecord in root:
        if isCondition(descriptorRecord):
            parsedCondition = parseCondition(descriptorRecord)
            data[parsedCondition[0]] = parsedCondition[1]

    json.dump(data, out, indent=4)

def main():
    '''
    Main method for MeSHParser.
    Outputs a JSON file storing each condition's MeSH term and their associated 
    MeSH code and entry terms.
    All input text is converted to lowercase except MeSH codes. Otherwise, output strings are as
    exactly as they appear in input.

    Data is read in from xml file with relative path {DATA_FILE}.
    Output file is named {OUTPUT_FILE_PATH} and follows formatting FORMAT.
    If output file already exists, all data will be overridden.

    FORMAT
    - MeSH Term
        - MeSH Code (String)
        - Entry Terms (List of String)
    '''
    # Configuration constants
    DATA_FILE = "rawData.xml"
    OUTPUT_FILE_PATH = "MeSHConditions.json"

    outputFile = open(OUTPUT_FILE_PATH, 'w', encoding='utf-8')

    # Parse and print data from input file
    parseFile(DATA_FILE, outputFile)

if __name__ == "__main__":
    main()
