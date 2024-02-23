import os
import requests
from colorama import Fore, Style

def stripe_vers(url2):
    try:
        response = requests.get(url2)
        if response.status_code == 200:
            html = response.text
            if 'v1' in html:
                print(f"{Fore.GREEN} {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.CYAN} Website has stripe v1!{Style.RESET_ALL}")
            elif 'v2' in html:
                print(f"{Fore.GREEN} {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.CYAN} Website has stripe v2!{Style.RESET_ALL}")
            elif 'v3' in html:
                print(f"{Fore.GREEN} {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.CYAN} Website has stripe v3!{Style.RESET_ALL}")
           
                
            else:
                print(f"{Fore.RED}{Fore.WHITE}[{Fore.RED}+{Fore.WHITE}] {Fore.CYAN} Website does not have stripe!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{Fore.WHITE}[{Fore.RED}+{Fore.WHITE}] {Fore.CYAN} Error: Unable to access website!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def gate_check(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            if 'paypal' in html | 'stripe' in html | 'braintree' in html | 'shopify' in html | 'skrill' in html | 'adyen' in html:
                print(f"{Fore.GREEN} {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.CYAN} Website has payment processors!{Style.RESET_ALL}")
                if 'paypal' in html:
                    print(f"{Fore.GREEN}PayPal{Style.RESET_ALL}")
                if 'stripe' in html:
                    print(f"{Fore.GREEN}Stripe{Style.RESET_ALL}")
                if 'braintree' in html:
                    print(f"{Fore.GREEN}Braintree{Style.RESET_ALL}")
                if 'adyen' in html:
                    print(f"{Fore.GREEN}Adyen{Style.RESET_ALL}")
                if 'shopify' in html:
                    print(f"{Fore.GREEN}Shopify{Style.RESET_ALL}")
                if 'skrill' in html:
                    print(f"{Fore.GREEN}Skrill{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Website does not have payment processors!{Style.RESET_ALL}")
        else:
            print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] {Fore.CYAN}Error: Unable to access website!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.WHITE}[{Fore.RED}!{Fore.WHITE}] {Fore.CYAN}Error: {e}{Style.RESET_ALL}")

def bin_lookup(bin):
    try:
        response = requests.get(f'https://lookup.binlist.net/{bin}')
        if response.status_code == 200:
            data = response.json()
            if data['type'] == 'credit':
                print(f"{Fore.GREEN}BIN Type: {data['type']}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Country: {data['country']['name']}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Bank: {data['bank']['name']}{Style.RESET_ALL}")
                vbv_status = check_vbv(bin)
                print(f"{Fore.GREEN}VBV Status: {vbv_status}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}BIN Type: {data['type']}{Style.RESET_ALL}")
                   print(f"{Fore.GREEN}Country: {data['country']['name']}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Bank: {data['bank']['name']}{Style.RESET_ALL}")
                vbv_status = check_vbv(bin)
                print(f"{Fore.GREEN}VBV Status: {vbv_status}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: Unable to access BIN list!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def check_vbv(bin):
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {'query': f'{{"clientToken": "{bin}"}}'}
        response = requests.post('https://payments.braintree-api.com/graphql', json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            token = data['data']['clientToken']['token']
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
            response = requests.post('https://www.wineowine.it/checkout/cart/', json={}, headers=headers)
            if response.status_code == 200:
                response = requests.get(f'https://api.braintreegateway.com/merchants/6j5mnzyxsd8x83n2/client_api/v1/payment_methods/{token}/three_d_secure/lookup', headers=headers)
                if response.status_code != 200:
                    return f'{Fore.GREEN}NonVBV'
                else:
                    return f'{Fore.RED}VBV'
            else:
                return f'{Fore.RED}VBV'
        else:
            return f'{Fore.RED}VBV'
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return f'{Fore.RED}VBV'

def main():
    print(Fore.BLUE+"Multi-tool Options:")
    print(Fore.YELLOW+"    1. Gate Check")
    print(Fore.YELLOW+"    2. Bin Lookup")
    print(Fore.YELLOW+"    3. Stripe Version Check")
    choice = input("Enter the number of the tool you want to use: ")
    if choice == '1':
        url = input(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.CYAN} Enter the website URL: ")
        gate_check(url)
    elif choice == '2':
        bin = input(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.CYAN} Enter the BIN number: ")
        bin_lookup(bin)
    elif choice == '3':
        url2 = input(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}] {Fore.CYAN} Enter the website URL: ")
        stripe_vers(url2)
    else:
        print(f"{Fore.WHITE}[{Fore.RED}+{Fore.WHITE}] {Fore.CYAN} Invalid choice. Please try again.")

if __name__ == "__main__":
    main()