# Program to calculate One Stop Insurance Company
# startin Date: Nov 24,2023 - End Date: Nov 29, 2023
#Written by: Francisco Garcia


from datetime import datetime, timedelta
import calendar

# Default values
NEXT_POLI_NUM = 1944
BASIC_PREM = 869.00
DISC_ADD_CAR = 0.25
LIAB_COVE_RATE = 130.00
GLASS_COVE_RATE = 86.00
LOANER_COVE_RATE = 58.00
HST_RATE = 0.15
PROCE_FEE = 39.99

# Program start here
customer_list = []
claims_list = []

def validate_province(province):
    valid_provinces = ['ON', 'QC', 'BC', 'AB', 'MB', 'SK', 'NS', 'NB', 'NL', 'PE', 'NT', 'NU', 'YT']
    return province.upper() in valid_provinces

def validate_payment_method(method):
    valid_methods = ['FULL', 'MONTHLY', 'DOWN PAY']
    return method.upper() in valid_methods

def get_valid_input(prompt, validator):
    while True:
        value = input(prompt)
        if validator(value):
            return value
        else:
            print('Invalid input. Please try again.')

#Customer Information
def get_customer_information():
    first_name = input("Enter first name: ").title()
    last_name = input("Enter last name: ").title()
    address = input("Enter address: ")
    city = input("Enter city: ").title()
    province = get_valid_input("Enter province (2 characters): ", validate_province)
    postal_code = input("Enter postal code: ")
    phone_number = input("Enter phone number: ")
#Lambda x: is a interested function. 
    cars_insured = int(input("Enter the number of cars being insured: "))
    extra_liability = get_valid_input("Extra liability coverage (Y/N): ", lambda x: x.upper() in ['Y', 'N'])
    glass_coverage = get_valid_input("Glass coverage (Y/N): ", lambda x: x.upper() in ['Y', 'N'])
    loaner_car = get_valid_input("Loaner car coverage (Y/N): ", lambda x: x.upper() in ['Y', 'N'])
    payment_method = get_valid_input("Enter payment method (Full, Monthly, or Down Pay): ", validate_payment_method)

    if payment_method == 'DOWN PAY':
        down_payment = float(input("Enter the amount of the down payment: "))
    else:
        down_payment = 0.0

    return {
        'first_name': first_name,
        'last_name': last_name,
        'address': address,
        'city': city,
        'province': province,
        'postal_code': postal_code,
        'phone_number': phone_number,
        'cars_insured': cars_insured,
        'extra_liability': extra_liability,
        'glass_coverage': glass_coverage,
        'loaner_car': loaner_car,
        'payment_method': payment_method,
        'down_payment': down_payment
    }

def calculate_premium(customer_info):
    total_extra_costs = customer_info['cars_insured'] * (LIAB_COVE_RATE(customer_info['extra_liability']) +
        GLASS_COVE_RATE(customer_info['glass_coverage']) + LOANER_COVE_RATE(customer_info['loaner_car'])
    )
    total_premium = BASIC_PREM + BASIC_PREM * DISC_ADD_CAR* (customer_info['cars_insured'] - 1) + total_extra_costs
    total_hst = total_premium * HST_RATE
    total_cost = total_premium + total_hst

    if customer_info['payment_method'] == 'DOWN PAY':
        total_cost -= customer_info['down_payment']

    return {
        'total_premium': total_premium,
        'total_extra_costs': total_extra_costs,
        'total_hst': total_hst,
        'total_cost': total_cost
    } 

def LIAB_COVE_RATE(choice):
    return LIAB_COVE_RATE if choice == 'Y' else 0.0

def GLASS_COVE_RATE(choice):
    return GLASS_COVE_RATE if choice == 'Y' else 0.0

def LOANER_COVE_RATE(choice):
    return LOANER_COVE_RATE if choice == 'Y' else 0.0

#Calculation Monthly Payment 
def calculate_monthly_payment(total_cost, down_payment):
    total_cost_with_fee = total_cost + PROCE_FEE
    remaining_cost = total_cost_with_fee - down_payment
    monthly_payment = remaining_cost / 8
    return monthly_payment

#This is the receipt 
def display_receipt(customer_info, premium_info):
    print()
    print(f'One Stop Insurance Company')
    print()
    print('Receipt:')
    print('=======================================')
    print(f'Policy Number: {NEXT_POLI_NUM}')
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Customer: {customer_info['first_name']} {customer_info['last_name']}")
    print(f"Address: {customer_info['address']}, {customer_info['city']}, {customer_info['province']} {customer_info['postal_code']}")
    print(f"Phone Number: {customer_info['phone_number']}")
    print(f"Cars Insured: {customer_info['cars_insured']}")
    print(f"Extra Liability: {customer_info['extra_liability']}")
    print(f"Glass Coverage: {customer_info['glass_coverage']}")
    print(f"Loaner Car: {customer_info['loaner_car']}")
    print(f"Payment Method: {customer_info['payment_method']}")
    if customer_info['payment_method'] == 'DOWN PAY':
        print(f"Down Payment: ${customer_info['down_payment']:.2f}")
    print("---------------------------------------")
    print(f"Basic Premium: ${BASIC_PREM:.2f}")
    print(f"Additional Cars Discount: ${BASIC_PREM * DISC_ADD_CAR * (customer_info['cars_insured'] - 1):.2f}")
    print(f"Extra Liability Coverage: ${LIAB_COVE_RATE(customer_info['extra_liability']):.2f}")
    print(f"Glass Coverage: ${GLASS_COVE_RATE(customer_info['glass_coverage']):.2f}")
    print(f"Loaner Car Coverage: ${LOANER_COVE_RATE(customer_info['loaner_car']):.2f}")
    print("---------------------------------------")
    print(f"Total Premium: ${premium_info['total_premium']:.2f}")
    print(f"HST ({HST_RATE * 100}%): ${premium_info['total_hst']:.2f}")
    print("---------------------------------------")
    print(f"Total Cost: ${premium_info['total_cost']:.2f}")

    if customer_info['payment_method'] in ['MONTHLY', 'DOWN PAY']:
        monthly_payment = calculate_monthly_payment(premium_info['total_cost'], customer_info['down_payment'])
        print(f"Monthly Payment: ${monthly_payment:.2f}")

    print("=======================================")

# Here we enter the Previous Claims
def get_previous_claims():
    claims = []
    while True:
        claim_date = input("Enter claim date (YYYY-MM-DD) or press Enter to finish: ")
        if not claim_date:
            break
        claim_amount = float(input("Enter claim amount: "))
        claims.append((claim_date, claim_amount))
    return claims

def display_previous_claims(claims):
    print()
    print("Previous Claims:")
    print("=======================================")
    for i, (claim_date, claim_amount) in enumerate(claims, start=1):
        print(f"Claim #    Claim Date      Amount")
    print("---------------------------------------")
    print(f"{i}.         {claim_date}      ${claim_amount:.2f}")
    print("=======================================")

def main():
    global NEXT_POLI_NUM

#
    while True:
        customer_info = get_customer_information()
        premium_info = calculate_premium(customer_info)
        display_receipt(customer_info, premium_info)

        claims = get_previous_claims()
        display_previous_claims(claims)

        customer_list.append({
            'customer_info': customer_info,
            'premium_info': premium_info,
            'claims': claims
        })

        NEXT_POLI_NUM += 1
# The Program will repeat if Y
        repeat = input("Do you want to enter another customer? (Y/N): ").upper()
        if repeat != 'Y':
            break

if __name__ == "__main__":
    main()