from flask import Flask, request, jsonify
import ast
import os
from dotenv import load_dotenv
import re
import cohere
app = Flask(__name__)
# co = cohere.ClientV2("0TsCLO0eraQabfBDpgxqAyi7xjHl4LSJygcCRqwp")
load_dotenv()  # Load environment variables from .env file
# api_key = os.getenv("OPENAI_API_KEY")
co = cohere.ClientV2(os.getenv("cohere_api_key"))
@app.route("/extract-fields", methods=["POST"])
def extract_fields():
    transcript = request.form.get("transcript")
    prompt = "Information: " + transcript + "\n" + "\n" + '''
     
     field_names = [
        "MortgageType", "LoanType", "LoanAmount", "InterestRate", "TermOfLoan", "AmortizationType", "PropertyType", 
        "NumberOfUnits", "PropertyAddress", "LegalDescription", "PurposeOfLoan", "OccupancyType", "BorrowerName", 
        "CoBorrowerName", "SSN", "DOB", "MaritalStatus", "Dependents", "PresentAddress", "PreviousAddress", 
        "PhoneNumber", "Email", "CurrentEmployer", "EmployerAddress", "Position", "YearsInJob", "YearsInProfession", 
        "MonthlyIncome", "Overtime", "Bonuses", "Commissions", "Dividends", "NetRentalIncome", "OtherIncome", "TotalIncome", 
        "CurrentHousingExpense", "Assets", "Liabilities", "RealEstateOwned", "PropertyAddresses", "PropertyTypeOwned", "MarketValue", 
        "MortgageBalance", "MonthlyPayment", "PropertyStatus", "BankruptcyHistory", "ForeclosureHistory", "LawsuitsJudgmentsLiens",
         "DelinquencyChildSupportAlimony", "OtherLegalObligations", "BorrowerSignature", "CoBorrowerSignature", "Date", "Race", "Ethnicity", 
         "Sex"
    ]
    ''' + "\n" + "\n" + '''QUESTION : I am giving you the information and also the list of field_names ,only return the list of tuples that contains the value for each field_name if you don't know the answer fill
    it with empty value and also the confidence score ,please don't output additional information ,only return me the ouput in the form of list and don't return anything other than that in any scenario
    if no actual transcript was given then just return list don't give extra text and if you were not able to extract just return the list dont return any other text
    and finally only the important instruction was to only return the output in list format this is very important!!
    '''
    response = co.chat(
    model="command-a-03-2025", 
    messages=[{"role": "user", "content": prompt}]
    )
    actualResultsString = response.message.content[0].text
    actualResultsString = actualResultsString[actualResultsString.find("[") : actualResultsString.rfind("]") + 1]
    actualresultsList = ast.literal_eval(actualResultsString)
    return jsonify({"value": actualresultsList})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
