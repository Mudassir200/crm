import frappe
from datetime import datetime,timedelta
from frappe.utils import getdate
import math
import requests


@frappe.whitelist()
def get_financial_discoveries():
    financial_discoveries = frappe.db.get_all("FD Financial Discovery",filters={"user":frappe.session.user},fields=["fd_name","timeframe","weekly_income_goal","name", "creation", "modified", "household_type", "dependant", "tenure_type", "years_lived_in_current_address", "retirement_age_goal","annual_income_goal"], order_by="modified desc")
    return financial_discoveries


@frappe.whitelist()
def get_financial_discovery(id):  # Get Financial Discovery
    try:
        if id:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            real_estate_assets = get_real_estate_assets(id)
            liabilities = get_liabilities(id)
            monthly_expenses = get_monthly_expenses(id)
            other_assets = get_other_assets(id)
            tax_rates = get_tax_rates()
            return {
                "financial_discovery":financial_discovery,
                "real_estate_assets":real_estate_assets,
                "monthly_expenses":monthly_expenses,
                "liabilities":liabilities,
                "other_assets":other_assets,
                "tax_rates":tax_rates,
            }
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
        return e


@frappe.whitelist(allow_guest=True)
def create_financial_discovery(data,buyers):  # Create Financial Discovery
    try:
        financial_discovery = frappe.get_doc({
            "doctype": "FD Financial Discovery",
            "household_type": data.get("household_type"),
            "dependant": data.get("dependant"),
            "tenure_type": data.get("tenure_type"),
            "years_lived_in_current_address": data.get("years_lived_in_current_address"),
            "retirement_age_goal": data.get("retirement_age_goal"),
            "annual_income_goal": data.get("annual_income_goal"),
            "timeframe": data.get("timeframe"),
        })

        if "dealname" in data:
            financial_discovery.crm_deal = data.get("dealname")
        if "organization" in data:
            financial_discovery.crm_organization = data.get("organization")

        if buyers and len(buyers) != 0:
            for buyer in buyers:
                doc = frappe.get_doc({
                        "doctype": "FD Individual",
                        "first_name": buyer.get("first_name"),
                        "surname": buyer.get("surname"),
                        "date_of_birth": getdate(buyer.get("date_of_birth")),
                        "gross_annual_income": buyer.get("gross_annual_income")
                })
                
                if "contact" in buyer:
                    doc.contact = buyer.get("contact")
                if "occupation" in buyer:
                    doc.occupation = buyer.get("occupation")
                if "length_of_employment_yrs" in buyer:
                    doc.length_of_employment_yrs = buyer.get("length_of_employment_yrs")
                if "employment_type" in buyer:
                    doc.employment_type = buyer.get("employment_type")
                if "untaxed_income" in buyer:
                    doc.untaxed_income = buyer.get("untaxed_income")

                doc.insert(ignore_permissions=True,ignore_mandatory=True) 
                frappe.db.commit()

                # Append buyer in Financial Discovery and save
                financial_discovery.append("buyers",{
                    "buyer" : doc.name
                })

            financial_discovery.insert(ignore_permissions=True,ignore_mandatory=True)
            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
        else:
            frappe.log_error({ "message":"Buyers data is required!"})
            return False
    except Exception as e:
        return e
   
@frappe.whitelist(allow_guest=True)
def update_financial_discovery(id,data,buyers):  # Update Financial Discovery
    try:
        financial_discovery = frappe.get_doc("FD Financial Discovery",id)
        if financial_discovery:
            frappe.db.delete("FD Household Buyers", {
                "parent": financial_discovery.name
            })
            frappe.db.commit()
            financial_discovery.reload()
            financial_discovery.household_type = data.get("household_type")
            financial_discovery.dependant = data.get("dependant")
            financial_discovery.tenure_type = data.get("tenure_type")
            financial_discovery.years_lived_in_current_address = data.get("years_lived_in_current_address")
            financial_discovery.retirement_age_goal = data.get("retirement_age_goal")
            financial_discovery.annual_income_goal = data.get("annual_income_goal")
            financial_discovery.timeframe = data.get("timeframe")

            newBuyers = []
            if buyers and len(buyers) != 0:
                for buyer in buyers:
                    existBuyer = False
                    if "buyer" in buyer:
                        tempBuyer = frappe.db.exists("FD Individual",buyer.get("buyer"))
                        if tempBuyer:
                            existBuyer = True
                            doc = frappe.get_doc("FD Individual",buyer.get("buyer"))
                            doc.first_name = buyer.get("first_name")
                            doc.surname = buyer.get("surname")
                            doc.date_of_birth = getdate(buyer.get("date_of_birth"))
                            doc.gross_annual_income = buyer.get("gross_annual_income")

                            if "occupation" in buyer:
                                doc.occupation = buyer.get("occupation")
                            if "length_of_employment_yrs" in buyer:
                                doc.length_of_employment_yrs = buyer.get("length_of_employment_yrs")
                            if "employment_type" in buyer:
                                doc.employment_type = buyer.get("employment_type")
                            if "untaxed_income" in buyer:
                                doc.untaxed_income = buyer.get("untaxed_income")
                            
                            doc.save(ignore_permissions=True)
                            newBuyers.append(doc.name)
                    
                    if existBuyer == False:
                        doc = frappe.get_doc({
                                "doctype": "FD Individual",
                                "first_name": buyer.get("first_name"),
                                "surname": buyer.get("surname"),
                                "date_of_birth": getdate(buyer.get("date_of_birth")),
                                "gross_annual_income": buyer.get("gross_annual_income")
                        })
                        
                        if "occupation" in buyer:
                            doc.occupation = buyer.get("occupation")
                        if "length_of_employment_yrs" in buyer:
                            doc.length_of_employment_yrs = buyer.get("length_of_employment_yrs")
                        if "employment_type" in buyer:
                            doc.employment_type = buyer.get("employment_type")
                        if "untaxed_income" in buyer:
                            doc.untaxed_income = buyer.get("untaxed_income")
                        doc.insert(ignore_permissions=True,ignore_mandatory=True) 
                        newBuyers.append(doc.name)
            else:
                frappe.log_error({ "message":"Buyers data is required!"})
                return False

            if len(newBuyers) > 0:
                for buyer in newBuyers:
                    financial_discovery.append("buyers",{
                        "buyer" : buyer
                    })

            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
    except Exception as e:
        return e


# @frappe.whitelist(allow_guest=True)
# def updateAnnualGrowth(id,rate): 
#     try:
#         if id and rate != 0:
#             financial_discovery = frappe.get_doc("FD Financial Discovery",id)
#             financial_discovery.assumed_annual_growth = rate
#             financial_discovery.save(ignore_permissions=True)
#             frappe.db.commit()
#             return financial_discovery
#         else:
#             frappe.log_error({ "message":"Annual Growth Rate data is invalid!"})
#             return False
#     except Exception as e:
#         return e
    
@frappe.whitelist(allow_guest=True)
def updateAnnualGrowth_of_prop_investment(id,rate): 
    try:
        if id and rate != 0:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            financial_discovery.annual_growth_of_investment_property = rate
            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
        else:
            frappe.log_error({ "message":"Property Investment Annual Growth Rate data is invalid!"})
            return False
    except Exception as e:
        return e
@frappe.whitelist(allow_guest=True)
def updateAnnualGrowth_of_superannuation(id,rate): 
    try:
        if id and rate != 0:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            financial_discovery.annual_growth_of_superannuation = rate
            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
        else:
            frappe.log_error({ "message":"Superannuation Annual Growth Rate data is invalid!"})
            return False
    except Exception as e:
        return e
@frappe.whitelist(allow_guest=True)
def updateAnnualGrowth_of_cash_savings(id,rate): 
    try:
        if id and rate != 0:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            financial_discovery.annual_growth_of_cash_savings = rate
            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
        else:
            frappe.log_error({ "message":"Cash Savings Annual Growth Rate data is invalid!"})
            return False
    except Exception as e:
        return e
@frappe.whitelist(allow_guest=True)
def updateAnnualGrowth_of_share_equities(id,rate): 
    try:
        if id and rate != 0:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            financial_discovery.annual_growth_of_share_equities = rate
            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
        else:
            frappe.log_error({ "message":"Shares & Equities Annual Growth Rate data is invalid!"})
            return False
    except Exception as e:
        return e

@frappe.whitelist(allow_guest=True)
def updateAverage_annual_inflation_rate(id,rate): 
    try:
        if id and rate != 0:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            financial_discovery.average_annual_inflation_rate = rate
            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
        else:
            frappe.log_error({ "message":"Average annual inflation rate data is invalid!"})
            return False
    except Exception as e:
        return e
@frappe.whitelist(allow_guest=True)
def updatePassive_income_rate_of_return_in_retirement(id,rate): 
    try:
        if id and rate != 0:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            financial_discovery.passive_income_rate_of_return_in_retirement = rate
            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
        else:
            frappe.log_error({ "message":"Passive income rate of return in retirement data is invalid!"})
            return False
    except Exception as e:
        return e
@frappe.whitelist(allow_guest=True)
def updateLife_expectancy(id,rate): 
    try:
        if id and rate != 0:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            financial_discovery.life_expectancy = rate
            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
        else:
            frappe.log_error({ "message":"Life expectancy data is invalid!"})
            return False
    except Exception as e:
        return e
  

# @frappe.whitelist(allow_guest=True)
# def updatePropertyGrowth(id,rate): 
#     try:
#         if id:
#             financial_discovery = frappe.get_doc("FD Financial Discovery",id)
#             financial_discovery.property_investment_growth = rate
#             financial_discovery.save(ignore_permissions=True)
#             frappe.db.commit()
#             return financial_discovery
#         else:
#             frappe.log_error({ "message":"Property Growth Rate data is invalid!"})
#             return False
#     except Exception as e:
#         return e
    

@frappe.whitelist(allow_guest=True)
def get_tax_rates():  # Get Tax Rates
    try:
        tax_rates = frappe.db.get_all(
                            "FD Tax Rates", 
                            fields=["name","low_limit", "high_limit","fixed_portion","variable_portion"],
                            order_by='creation asc'
                            )  
        return tax_rates
    except Exception as e:
        return e
       
@frappe.whitelist(allow_guest=True)
def getInvestor():
    teminvestors = frappe.db.get_all("FD Individual", fields=["name as value","first_name","Surname"])
    investors = []
    for investor in teminvestors:
        investors.append({
            "value": investor.value,
            "label": investor.first_name + " " + investor.surname
        })

    return investors
    


# FD Individual Functions


@frappe.whitelist(allow_guest=True)
def updateBuyers(fdId,id,data):  # Update Buyers
    try:

        buyer = frappe.get_doc("FD Individual", id) 
        buyer.reload()
        buyer.first_name = data.get('first_name')
        buyer.surname = data.get('surname')
        buyer.date_of_birth = getdate(data.get('date_of_birth'))
        buyer.gross_annual_income = data.get('gross_annual_income')

        if "occupation" in data:
            buyer.occupation = data.get("occupation")
        if "length_of_employment_yrs" in data:
            buyer.length_of_employment_yrs = data.get("length_of_employment_yrs")
        if "employment_type" in data:
            buyer.employment_type = data.get("employment_type")
        if "untaxed_income" in data:
            buyer.untaxed_income = data.get("untaxed_income")

        buyer.save(ignore_permissions=True)


        financial_discovery = frappe.get_doc("FD Financial Discovery",fdId)
        # buyers = financial_discovery.buyers
        for temp in financial_discovery.get('buyers'):
            temp.buyer = temp.buyer

        financial_discovery.save(ignore_permissions=True)
        frappe.db.commit()
        calculateAllFDFields(fdId)
        return buyer
    except Exception as e:
        return e
    
@frappe.whitelist(allow_guest=True)
def create_buyer(id,data):
    try:
        # Get Financial Discovery
        financial_discovery = frappe.get_doc("FD Financial Discovery",id)
        if financial_discovery and data:
            # Create FD Buyer
            doc = frappe.get_doc({
                "doctype": "FD Individual",
                "first_name": data.get("first_name"),
                "surname": data.get("surname"),
                "date_of_birth": getdate(data.get("date_of_birth")),
                "gross_annual_income": data.get("gross_annual_income")
            })
            
            if "occupation" in data:
                doc.occupation = data.get("occupation")
            if "length_of_employment_yrs" in data:
                doc.length_of_employment_yrs = data.get("length_of_employment_yrs")
            if "employment_type" in data:
                doc.employment_type = data.get("employment_type")
            if "untaxed_income" in data:
                doc.untaxed_income = data.get("untaxed_income")

            doc.insert(ignore_permissions=True,ignore_mandatory=True) 

            # Append buyer in Financial Discovery and save
            financial_discovery.append("buyers",{
                "buyer" : doc.name
            })
            financial_discovery.save(ignore_permissions=True)
            frappe.db.commit()
            return financial_discovery
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
            return e




# FD Liabilities Functions

@frappe.whitelist(allow_guest=True)
def get_liabilities(id):  # Get Liabilities
    try:
        if id:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            liabilities = frappe.db.get_all(
                                "FD Liabilities", 
                                fields=["name","liability_name", "owning","limit","lender","rate", "monthly_repayment"],
                                filters={
                                    "financial_discovery": id
                                },order_by='creation asc')
            return liabilities
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
        return e

@frappe.whitelist(allow_guest=True)
def create_liabilities(id,data):
    try:
        # Get Financial Discovery
        financial_discovery = frappe.get_doc("FD Financial Discovery",id)
        if financial_discovery and data:
            # Create FD Liabilities
            doc = frappe.get_doc({
                "doctype": "FD Liabilities",
                "financial_discovery": id,
                "liability_name": data.get("liability_name"),
                "owning": data.get("owning"),
                "lender": data.get("lender")
            })

            if "limit" in data:
                doc.limit = data.get("limit")
            if "rate" in data:
                doc.rate = data.get("rate")
            if "monthly_repayment" in data:
                doc.monthly_repayment = data.get("monthly_repayment")

            doc.insert(ignore_permissions=True) 
            frappe.db.commit()

            return doc
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
            return e
    
@frappe.whitelist(allow_guest=True)
def edit_liabilities(id,data):  # Update Liabilities
    try:
        liability = frappe.get_doc("FD Liabilities",id)
        if liability and data:
            liability.reload()
            liability.liability_name = data.get('liability_name')
            liability.owning = data.get('owning')
            liability.lender = data.get('lender')

            if "limit" in data:
                liability.limit = data.get("limit")
            if "rate" in data:
                liability.rate = data.get("rate")
            if "monthly_repayment" in data:
                liability.monthly_repayment = data.get("monthly_repayment")

            liability.save(ignore_permissions=True)
            return liability
        else:
            frappe.log_error({ "message":"FD Liability is not valid!"})
            return False
    except Exception as e:
        return e

@frappe.whitelist(allow_guest=True)
def delete_liabilities(id):  # Delete Liabilities
    try:
        liability = frappe.get_doc("FD Liabilities",id)
        if liability:
            frappe.delete_doc("FD Liabilities",id)
            return True
        else:
            frappe.log_error({ "message":"FD Liability is not valid!"})
            return False
    except Exception as e:
        return e



# FD Monthly Expense Functions

@frappe.whitelist(allow_guest=True)
def get_monthly_expenses(id):  # Get Monthly Expenses
    try:
        if id:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            monthly_expenses = frappe.db.get_all(
                                "FD Monthly Expenses", 
                                fields=["name","expense_name", "amount"],
                                filters={
                                    "financial_discovery": id
                                },order_by='creation asc')  
            return monthly_expenses
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
        return e
    
@frappe.whitelist(allow_guest=True)
def create_monthly_expense(id,data):
    try:
        # Get Financial Discovery
        financial_discovery = frappe.get_doc("FD Financial Discovery",id)
        if financial_discovery and data:
            # Create FD Monthly Expenses
            doc = frappe.get_doc({
                "doctype": "FD Monthly Expenses",
                "financial_discovery": id,
                "expense_name": data.get("expense_name"),
                "amount": data.get("amount")
            })

            doc.insert(ignore_permissions=True) 

            return doc
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
            return e

@frappe.whitelist(allow_guest=True)
def update_monthly_expense(id,data):
    try:
        doc = frappe.get_doc("FD Monthly Expenses",id)
        if doc and data:
            doc.reload()
            doc.expense_name = data.get('expense_name')
            doc.amount = data.get('amount')

            doc.save(ignore_permissions=True)
            return doc
        else:
            frappe.log_error({ "message":"FD Monthly Expenses is not valid!"})
            return False
    except Exception as e:
            return e

@frappe.whitelist(allow_guest=True)
def delete_monthly_expense(id):  # Delete Monthly Expense
    try:
        doc = frappe.get_doc("FD Monthly Expenses",id)
        if doc:
            frappe.delete_doc("FD Monthly Expenses",id)
            return True
        else:
            frappe.log_error({ "message":"FD Monthly Expenses is not valid!"})
            return False
    except Exception as e:
        return e




# FD Other Assets Functions

@frappe.whitelist(allow_guest=True)
def get_other_assets(id):  # Get Other Assets
    try:
        if id:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            other_assets = frappe.db.get_all(
                                "FD Other Assets", 
                                fields=["name", "cash_savings","financial_discovery","superannuation","shares_equities",
                                        "weekly_savings_capacity", "extra_yearly_contributions","creation","investor.name as investor","investor.first_name","investor.surname"],
                                filters={
                                    "financial_discovery": id
                                },order_by='creation asc')  
            return other_assets
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
        return e
    
@frappe.whitelist(allow_guest=True)
def create_other_assets(id,investor,data):
    try:
        # Get Financial Discovery and Buyer
        financial_discovery = frappe.get_doc("FD Financial Discovery",id)
        buyer = frappe.get_doc("FD Individual",investor)
        if financial_discovery and buyer and data:
            # Create FD Other Assets
            doc = frappe.get_doc({
                "doctype": "FD Other Assets",
                "financial_discovery": id,
                "investor": investor,
                "cash_savings": data.get("cash_savings")
            })

            if "superannuation" in data:
                doc.superannuation = data.get("superannuation")
            if "shares_equities" in data:
                doc.shares_equities = data.get("shares_equities")
            if "weekly_savings_capacity" in data:
                doc.weekly_savings_capacity = data.get("weekly_savings_capacity")
            if "extra_yearly_contributions" in data:
                doc.extra_yearly_contributions = data.get("extra_yearly_contributions")

            doc.insert(ignore_permissions=True) 

            return doc
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
            return e
    
@frappe.whitelist(allow_guest=True)
def update_other_assets(id,investor,data):
    try:
        doc = frappe.get_doc("FD Other Assets",id)
        buyer = frappe.get_doc("FD Individual",investor)
        if doc and buyer and data:
            doc.reload()
            doc.investor = data.get('investor')
            doc.cash_savings = data.get('cash_savings')

            if "superannuation" in data:
                doc.superannuation = data.get("superannuation")
            if "shares_equities" in data:
                doc.shares_equities = data.get("shares_equities")
            if "weekly_savings_capacity" in data:
                doc.weekly_savings_capacity = data.get("weekly_savings_capacity")
            if "extra_yearly_contributions" in data:
                doc.extra_yearly_contributions = data.get("extra_yearly_contributions")

            doc.save(ignore_permissions=True)
            return doc
        else:
            frappe.log_error({ "message":"FD Other Assets is not valid!"})
            return False
    except Exception as e:
            return e

@frappe.whitelist(allow_guest=True)
def delete_other_assets(id):  # Delete Other Assets
    try:
        doc = frappe.get_doc("FD Other Assets",id)
        if doc:
            frappe.delete_doc("FD Other Assets",id)
            return True
        else:
            frappe.log_error({ "message":"FD Other Assets is not valid!"})
            return False
    except Exception as e:
        return e




# FD Real Estate Assets Functions


@frappe.whitelist(allow_guest=True)
def get_real_estate_assets(id):  # Get Real Estate Assets
    try:
        if id:
            financial_discovery = frappe.get_doc("FD Financial Discovery",id)
            real_estate_assets = frappe.db.get_all(
                                    "FD Real Estate Assets", 
                                    fields=["name","type","location","current_value","purchase_price","year_aquired",
                                            "ownership_type","ownership_structure","loan_amount","interest_rate",
                                            "lender","p_io","fixed_or_var","monthly_repayment","weekly_rent_income"],
                                    filters={
                                        "financial_discovery": id
                                    },order_by='creation asc')
            return real_estate_assets
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
        return e
 
@frappe.whitelist(allow_guest=True)
def create_real_estate_assets(id,data):
    try:
        # Get Financial Discovery
        financial_discovery = frappe.get_doc("FD Financial Discovery",id)
        if financial_discovery and data:
            # Create FD Real Estate Assets

            doc = frappe.get_doc({
                "doctype": "FD Real Estate Assets",
                "financial_discovery": id,
                "type": data.get("type"),
                "location": data.get("location"),
                "current_value": data.get("current_value"),
                "purchase_price": data.get("purchase_price"),
                "year_aquired": data.get("year_aquired"),
                "ownership_type": data.get("ownership_type"),
                "ownership_structure": data.get("ownership_structure"),
                "weekly_rent_income":data.get("weekly_rent_income"),
                "loan_amount": data.get("loan_amount"),
                "interest_rate": data.get("interest_rate")
            })

            if data.get('type') == "PPOR":
                doc.weekly_rent_income = 0
            if "lender" in data:
                doc.lender = data.get("lender")
            if "p_io" in data:
                doc.p_io = data.get("p_io")
            if "fixed_or_var" in data:
                doc.fixed_or_var = data.get("fixed_or_var")
            if "monthly_repayment" in data:
                doc.monthly_repayment = data.get("monthly_repayment")

            doc.insert(ignore_permissions=True) 

            return doc
        else:
            frappe.log_error({ "message":"Financial Discovery is not valid!"})
            return False
    except Exception as e:
            return e   

@frappe.whitelist(allow_guest=True)
def update_real_estate_assets(id,data):
    try:
        # Get Financial Discovery
        doc = frappe.get_doc("FD Real Estate Assets",id)
        if doc and data:
            doc.type = data.get("type")
            doc.location = data.get("location")
            doc.current_value = data.get("current_value")
            doc.purchase_price = data.get("purchase_price")
            doc.year_aquired = data.get("year_aquired")
            doc.ownership_type = data.get("ownership_type")
            doc.ownership_structure = data.get("ownership_structure")
            doc.weekly_rent_income = data.get("weekly_rent_income")
            doc.loan_amount = data.get("loan_amount")
            doc.interest_rate = data.get("interest_rate")

            if data.get('type') == "PPOR":
                doc.weekly_rent_income = 0
                
            if "lender" in data:
                doc.lender = data.get("lender")
            if "p_io" in data:
                doc.p_io = data.get("p_io")
            if "fixed_or_var" in data:
                doc.fixed_or_var = data.get("fixed_or_var")
            if "monthly_repayment" in data:
                doc.monthly_repayment = data.get("monthly_repayment")

            doc.save(ignore_permissions=True) 

            return doc
        else:
            frappe.log_error({ "message":"Real Estate Assets is not valid!"})
            return False
    except Exception as e:
            return e   

@frappe.whitelist(allow_guest=True)
def delete_real_estate_assets(id):  
    try:
        doc = frappe.get_doc("FD Real Estate Assets",id)
        if doc:
            frappe.delete_doc("FD Real Estate Assets",id)
            return True
        else:
            frappe.log_error({ "message":"FD Real Estate Assets is not valid!"})
            return False
    except Exception as e:
        return e































@frappe.whitelist(allow_guest=True)
def calculateAllFDFields(fdId):
    try:
        doc = frappe.get_doc("FD Financial Discovery",fdId)
        doc.reload()
        if doc.name == None or doc.name == "":
            return False
        
        year_until_retirement = 0
        eldest_year_until_retirement = 0
        smallAge = 1000000
        current_eldest_age = 0

        total_gross_annual_income = 0
        for buyer in doc.buyers:
            total_gross_annual_income += buyer.gross_annual_income
        doc.total_gross_annual_income = total_gross_annual_income
        allTaxRates = frappe.db.get_all("FD Tax Rates",fields=['*'])
        total_tax = 0
        for buyer in doc.buyers:
            rate = getTaxRate(buyer.gross_annual_income, allTaxRates)
            total_tax += rate.fixed_portion + (buyer.gross_annual_income - rate.low_limit) * rate.variable_portion
            if int(buyer.age) < int(smallAge):
                smallAge = buyer.age
                year_until_retirement = timeframe(buyer.date_of_birth,doc.retirement_age_goal); 
            if int(buyer.age) > int(current_eldest_age):
                current_eldest_age = buyer.age 
                eldest_year_until_retirement = timeframe(buyer.date_of_birth,doc.retirement_age_goal); 

        if eldest_year_until_retirement < 0:
            eldest_year_until_retirement = 0
        if year_until_retirement < 0:
            year_until_retirement = 0

        doc.timeframe = eldest_year_until_retirement
        doc.total_tax = total_tax
        if total_tax != 0:
            doc.total_tax_daily = total_tax / 365
        else:
            doc.total_tax_daily = 0
        
        if total_tax != 0 and eldest_year_until_retirement != 0:
            doc.total_lifetime_tax = total_tax * math.floor(eldest_year_until_retirement * 10000) / 10000
        else:
            doc.total_lifetime_tax = 0

        total_of_month_in_year_for_pay_tax = 0
        if total_tax != 0 and total_gross_annual_income != 0:
            total_of_month_in_year_for_pay_tax = 12 * ( total_tax / total_gross_annual_income )
            
        if total_of_month_in_year_for_pay_tax != 0:
            doc.total_of_month_in_year_for_pay_tax =  math.floor(total_of_month_in_year_for_pay_tax * 100) / 100
        else:
            doc.total_of_month_in_year_for_pay_tax = 0

        home_mortgage_current = 0
        home_mortgage_interest_rate = 0

        currentInvestment = 0
        currentInvestmentLiabilities = 0
        current_monthly_repayment = 0
        allRealEstateAssets = frappe.db.get_all("FD Real Estate Assets",filters={"financial_discovery": fdId},fields=['*'])

        doc.total_home_mortgage = 0
        doc.current_home_debt = 0
        doc.current_interest_rate = 0
        doc.home_mortgage_current = 0
        doc.current_monthly_repayment = 0
        doc.total_net_annual_income = 0
        doc.total_annual_mortgage_payments = 0
        doc.portion_of_income_going_to_tax_and_mortgage = 0
        doc.day_of_year_when_start_making_money = ""
        doc.interest_liability_still_payable = 0
        doc.actual_cost_of_mortgage_including_interest_after_tax = 0
        doc.actual_cost_of_mortgage_including_interest_before_tax = 0
        doc.tax_liabilities_pay_over_off_years = 0
        
        for asset in allRealEstateAssets:
            if asset.type == "PPOR":
                current_monthly_repayment = asset.monthly_repayment
                doc.current_monthly_repayment = current_monthly_repayment
                doc.total_net_annual_income = total_gross_annual_income - total_tax - (asset.monthly_repayment * 12)
                total_annual_mortgage_payments = asset.monthly_repayment * 12
                doc.total_annual_mortgage_payments = total_annual_mortgage_payments

                portion_of_income_going_to_tax_and_mortgage = 0
                if total_gross_annual_income != 0 and (total_annual_mortgage_payments + total_tax) != 0:
                    portion_of_income_going_to_tax_and_mortgage = (total_annual_mortgage_payments + total_tax) / total_gross_annual_income
                    doc.portion_of_income_going_to_tax_and_mortgage = math.ceil(portion_of_income_going_to_tax_and_mortgage * 100)

                if portion_of_income_going_to_tax_and_mortgage != 0:
                    doc.day_of_year_when_start_making_money = getOrdinalSuffix(portion_of_income_going_to_tax_and_mortgage)

                doc.total_home_mortgage = asset.loan_amount
                doc.current_home_debt = asset.loan_amount
                doc.current_interest_rate = asset.interest_rate
                
                nper = 0
                if asset.interest_rate != 0 and asset.monthly_repayment != 0:
                    nper = calculateNPER(asset.interest_rate / 100,asset.monthly_repayment,asset.loan_amount)
                    doc.how_many_years_pay_for_home_free = math.ceil(nper)

                interest_liability_still_payable = (asset.monthly_repayment * 12 * nper) - asset.loan_amount
                doc.interest_liability_still_payable = interest_liability_still_payable

                actual_cost_of_mortgage_including_interest_after_tax = asset.loan_amount + interest_liability_still_payable
                doc.actual_cost_of_mortgage_including_interest_after_tax = actual_cost_of_mortgage_including_interest_after_tax
                
                actual_cost_of_mortgage_including_interest_before_tax = 0
                if total_gross_annual_income != 0 and total_tax != 0 and actual_cost_of_mortgage_including_interest_after_tax != 0:
                    actual_cost_of_mortgage_including_interest_before_tax = actual_cost_of_mortgage_including_interest_after_tax / ( 1 - total_tax / total_gross_annual_income)
                
                doc.actual_cost_of_mortgage_including_interest_before_tax = actual_cost_of_mortgage_including_interest_before_tax
                doc.tax_liabilities_pay_over_off_years = actual_cost_of_mortgage_including_interest_before_tax - actual_cost_of_mortgage_including_interest_after_tax
                
                home_mortgage_current = asset.loan_amount
                doc.home_mortgage_current = home_mortgage_current
                home_mortgage_interest_rate = asset.interest_rate
            else:
                currentInvestment += asset.current_value
                currentInvestmentLiabilities += asset.loan_amount

        doc.investment_property_current = currentInvestment
        doc.liabilities_investment_property_current = currentInvestmentLiabilities
        doc.liabilities_investment_property_after_projection_year = currentInvestmentLiabilities

        property_total = 0
        property_portfolio_ivps = 0
        smsf_total = 0
        smsf_portfolio_ivps = 0
        
        for asset in allRealEstateAssets:
            year_held = datetime.now().year - asset.year_aquired
            annual_growth = 0
            
            if year_held != 0 and asset.current_value != 0 and asset.purchase_price != 0:
                annual_growth = (math.pow(asset.current_value / asset.purchase_price, 1 / year_held) - 1) * 100

            if asset.type == "SMSF":
                smsf_total += 1
                smsf_portfolio_ivps += annual_growth
            else:
                property_total += 1
                property_portfolio_ivps += annual_growth
        

        investment_property_after_projection_year = 0
        property_investment_growth = 0
        
        if doc.annual_growth_of_investment_property != 0:
            property_investment_growth = doc.annual_growth_of_investment_property
        else:
            if property_portfolio_ivps != 0 and smsf_portfolio_ivps != 0 and property_total != 0 and smsf_total != 0:
                property_investment_growth = ((property_portfolio_ivps / property_total) + (smsf_portfolio_ivps / smsf_total)) / 2
                doc.annual_growth_of_investment_property = property_investment_growth
        
        if property_investment_growth != 0 and year_until_retirement != 0:
            investment_property_after_projection_year = currentInvestment *  math.pow(1 + (property_investment_growth / 100), math.floor(year_until_retirement))
        
        doc.investment_property_after_projection_year = investment_property_after_projection_year

        cash_savings = 0
        superannuation = 0
        others = 0
        allOtherAssets = frappe.db.get_all("FD Other Assets",filters={"financial_discovery": fdId},fields=['*'])
        for asset in allOtherAssets:
            cash_savings += asset.cash_savings
            superannuation += asset.superannuation
            others += asset.shares_equities
        
        doc.cash_savings_current = cash_savings
        doc.superannuation_current = superannuation
        doc.others_current = others

        temp = 0
        if eldest_year_until_retirement != 0:
            temp = math.ceil(eldest_year_until_retirement * 100) / 100
        superannuation_after_projection_year = 0
        if doc.annual_growth_of_superannuation != 0:
            superannuation_after_projection_year = superannuation *  math.pow((1 + (doc.annual_growth_of_superannuation / 100)), temp)
        if doc.annual_growth_of_cash_savings != 0:
            cash_savings_after_projection_year = cash_savings *  math.pow((1 + (doc.annual_growth_of_cash_savings / 100)), temp)
        if doc.annual_growth_of_share_equities != 0:
            others_after_projection_year = others *  math.pow((1 + (doc.annual_growth_of_share_equities / 100)), temp)
        doc.superannuation_after_projection_year = superannuation_after_projection_year
        doc.cash_savings_after_projection_year = cash_savings_after_projection_year
        doc.others_after_projection_year = others_after_projection_year

        total_assets_current = currentInvestment + cash_savings + superannuation + others
        doc.total_assets_current = total_assets_current
        doc.total_assets__after_projection_year = investment_property_after_projection_year + superannuation_after_projection_year

        other_debt_current = 0
        allLiabilities = frappe.db.get_all("FD Liabilities",filters={"financial_discovery": fdId},fields=['*'])
        for liability in allLiabilities:
            other_debt_current += liability.owning

        doc.other_debt_current = other_debt_current
        total_liabilities_current = home_mortgage_current + currentInvestmentLiabilities + other_debt_current
        doc.total_liabilities_current = total_liabilities_current

        future_balance = 0
        if home_mortgage_interest_rate != 0 and current_monthly_repayment != 0 and home_mortgage_current != 0:
            t = eldest_year_until_retirement
            r = home_mortgage_interest_rate / 100
            future_balance = home_mortgage_current * math.ceil(math.pow(1 + r, t)) - (math.ceil((current_monthly_repayment * 12) / r) * int(math.pow(1+r,eldest_year_until_retirement - 1)))
        
        doc.home_mortgage_after_projection_year = future_balance

        net_wealth_current = total_assets_current - total_liabilities_current
        doc.net_wealth_current = net_wealth_current
        net_wealth_after_projection_year = investment_property_after_projection_year + superannuation_after_projection_year  - currentInvestmentLiabilities
        doc.net_wealth_after_projection_year = net_wealth_after_projection_year
        
        doc.years_retired_up_to_life_expectancy = doc.life_expectancy - doc.retirement_age_goal
        doc.current_eldest_age = current_eldest_age
        doc.years_until_retirement = year_until_retirement

        #  Lump Sum current Year Value
        if doc.average_annual_inflation_rate != 0 and doc.passive_income_rate_of_return_in_retirement != 0:
            if doc.retirement_income_method == "Passive Income":
                ava_inflation_rate = doc.average_annual_inflation_rate / 100
                if ((1 + doc.passive_income_rate_of_return_in_retirement) / (1) - 1) != 0:
                    rate = ((1 + doc.passive_income_rate_of_return_in_retirement) / (1) - 1) / 100
                    nper = doc.years_retired_up_to_life_expectancy
                    pmt = doc.annual_income_goal * math.pow(1 + ava_inflation_rate,int(year_until_retirement))
                    pv = (pmt * (1 - (1 + rate) ** -nper) / rate) * (1 + rate * 1)
                    doc.lump_sum_needed = math.floor(pv)
            else:        
                doc.lump_sum_needed = doc.annual_income_goal * (doc.life_expectancy - doc.retirement_age_goal)
        else:
            doc.lump_sum_needed = 0
        
        #  Lump Sum current Year Value  (inflation adjusted)
        pi = 0
        pva = 0
        if doc.average_annual_inflation_rate != 0 and doc.passive_income_rate_of_return_in_retirement != 0:
            ava_inflation_rate = doc.average_annual_inflation_rate / 100
            if doc.retirement_income_method != "Lump Sum":
                pi = doc.passive_income_rate_of_return_in_retirement / 100
                
            if ((1 + pi) / (1 + ava_inflation_rate) - 1) != 0:
                rate = ((1 + pi) / (1 + ava_inflation_rate) - 1) / 1
                nper = doc.years_retired_up_to_life_expectancy
                pmt = doc.annual_income_goal * math.pow(1 + ava_inflation_rate,int(year_until_retirement))
                pva = (pmt * (1 - (1 + rate) ** -nper) / rate) * (1 + rate * 1)
                doc.lump_sum_needed_inflation_adjusted = math.floor(pva)
        else:
            doc.lump_sum_needed_inflation_adjusted = 0
        

        retirement_shortfall_including_inflation_current = net_wealth_current - pva
        doc.retirement_shortfall_including_inflation_current = retirement_shortfall_including_inflation_current
        doc.retirement_shortfall_including_inflation_after_projection_year = net_wealth_after_projection_year + retirement_shortfall_including_inflation_current

        yearly_savings_required_starting_today = 0
        if retirement_shortfall_including_inflation_current != 0 and year_until_retirement != 0 and int(year_until_retirement) > 0:
            yearly_savings_required_starting_today = -(retirement_shortfall_including_inflation_current / int(year_until_retirement))
            doc.yearly_savings_required_starting_today = yearly_savings_required_starting_today
        else:
            doc.yearly_savings_required_starting_today = 0
            

        if yearly_savings_required_starting_today != 0:
            doc.daily_savings_required_starting_today = yearly_savings_required_starting_today / 365
        else:
            doc.daily_savings_required_starting_today = 0

        doc.db_update()
        return doc
    except Exception as e:
        return e


def getTaxRate(income,allTaxRates):
	taxRate = False
	for rate in allTaxRates:
		if income >= rate.low_limit and income <= rate.high_limit:
			taxRate = rate
	return taxRate

def calculateNPER(ratePerYear, monthly_repayment, loanAmount):
    ratePerMonth = ratePerYear / 12
    nperMonths = nper(ratePerMonth, monthly_repayment, loanAmount)
    return nperMonths / 12

def nper(rate, monthly_repayment, loanAmount):
    if rate == 0:
        return loanAmount / monthly_repayment
    return math.log(monthly_repayment / (monthly_repayment - rate * loanAmount)) / math.log(1 + rate)

def timeframe(date,age):
    birthdate = datetime.strptime(str(date), "%Y-%m-%d").timestamp() * 1000
    today = datetime.now().timestamp() * 1000
    difference = today - birthdate
    differenceDays = difference / (1000 * 60 * 60 * 24 * 365)
    timeframe = age - differenceDays
    return timeframe 

def getOrdinalSuffix(data):
    startDate = datetime(2022,1,1)
    targetDate = startDate + timedelta(days=365 * data + 1)
    day = targetDate.day
    if day == 1 or day == 21 or day == 31: 
        suffix = "st"
    elif day == 2 or day == 22:
        suffix = "nd"
    elif day == 3 or day == 23:
        suffix = "rd"
    else:
        suffix = "th"
    
    month = targetDate.strftime('%b')
    return f"{day}{suffix} {month}"

    