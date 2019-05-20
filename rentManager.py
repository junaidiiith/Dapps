import json
from web3Connection import *

def call_function(contract, function, *args):
    try:
        return contract.get_function_by_name(function)(*args).call()
    except:
        print("Some error occured while calling the function "+str(function)+"!!")
    # Wait for transaction to be mined...
   
def do_transaction(account,contract,function,*args,**kwargs):
    
    print(contract.get_function_by_name(function))
    try:
	    txn = contract.get_function_by_name(function)(*args).buildTransaction(kwargs)
	    print("built transaction")
	    signed = account.signTransaction(txn)
	    print("signed transaction")
	    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
	    print("sent transaction")
	    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
	    return tx_receipt
    except Exception:
        print("Some error occured while executing transaction!!")
    # Wait for transaction to be mined...

def deploy_contract(account, contract_interface, *args, **kwargs):
    # Instantiate and deploy contract
    # acct = w3.eth.account.privateKeyToAccount(privateKey)
    kwargs['from'] = kwargs['frm']
    kwargs.pop('frm')
    print(args,"----",kwargs)
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']['object']
    )
    # Get transaction hash from deployed contract
    txn = contract.constructor(*args).buildTransaction(kwargs)
    signed = account.signTransaction(txn)
    # Get tx receipt to get contract address
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt['contractAddress']
   

# def get_kwargs(account, gas, price, value):
#     nonce = get_nonce(account)
#     return {'nonce' :  nonce,
#     'gas': gas,
#     'gasPrice' : price,
#     'value' : value}

# def get_nonce(account):
#     return w3.eth.getTransactionCount(account)


url = "http://127.0.0.1:7545"
w3 = connect(url)
gas = 3000000
gasPrice = w3.eth.gasPrice




contract_interface = {"bin": json.load(open('rentAgreement.bin')), "abi": json.load(open('rentAgreement.abi'))}
mod_contract_interface = {"bin" : json.load(open('modifiedRentAgreement.bin')), "abi": json.load(open('modifiedRentAgreement.abi'))}

landlordprivateKey = "541927bd3d1c1b23ecc3781c92458687a61867e8ee701d38311aa7f6f7cec1cd"
tenantprivateKey = "ae5d7dbafa62274248b8b2467c4b6e7ba36407f0224736926204059b3b25935f"

landlord = w3.eth.account.privateKeyToAccount(landlordprivateKey)
tenant = w3.eth.account.privateKeyToAccount(tenantprivateKey)

print("-------Starting renting contract-------")
menu = '''
	1) Confirm agreement\n\t
	2) Pay Rent \n\t
	3) Terminate contract \n\t
	4) Deploy different contract \n\t
	5) Move to next contract \n\t 
	6) Move to prev contract\n
	'''


class RentalAgreementManager:
	def __init__(self):
		self.address = deploy_contract(landlord,contract_interface,20,"Junaid",
			frm=landlord.address,
			nonce= w3.eth.getTransactionCount(landlord.address),
			gas=gas,
			gasPrice=gasPrice)
		self.contract = w3.eth.contract(address=self.address, abi=contract_interface['abi'])

	def deploy_another(self, *args, **kwargs):
		new_address = deploy_contract(landlord,mod_contract_interface,20,5,"NewHouse",
			frm=landlord.address,
			nonce=w3.eth.getTransactionCount(landlord.address),
			gas=gas,
			gasPrice=gasPrice)
		new_contract = w3.eth.contract(address=new_address, abi=mod_contract_interface['abi'])
		tx_receipt = do_transaction(landlord,self.contract,"setNext",new_address,
			nonce=w3.eth.getTransactionCount(landlord.address),
			gas=gas,
			gasPrice=gasPrice)
		tx_receipt1 = do_transaction(landlord,new_contract,"setPrev", self.address,
			nonce=w3.eth.getTransactionCount(landlord.address),
			gas=gas,
			gasPrice=gasPrice)
		self.address = new_address
		self.contract = new_contract

	def terminateContract(self):
		tx_receipt = do_transaction(landlord,self.contract,"terminateContract",
			nonce= w3.eth.getTransactionCount(landlord.address),
			gas=gas,
			gasPrice=gasPrice)

	def confirmAgreement(self):
		tx_receipt = do_transaction(tenant, self.contract, "confirmAgreement", 
			nonce=w3.eth.getTransactionCount(tenant.address),
			gas=gas,
			gasPrice=gasPrice)
		print(tx_receipt)

	def payRent(self):
		prev = call_function(self.contract,"getPrev")
		print(prev)
		if prev != '0x0000000000000000000000000000000000000000':
			value = 25
		else:
			value = 20
		print(value)
		tx_receipt = do_transaction(tenant,self.contract, "payRent",
			nonce=w3.eth.getTransactionCount(tenant.address),
			value=value,
			gas=gas,
			gasPrice=gasPrice)

	def go_back_to_prev_contract(self):
		old_address = call_function(landlord,self.contract, "getPrev")
		if old_address:
			self.contract = w3.eth.contract(address=old_address, abi=contract_interface['abi'])
			self.address = old_address
		else:
			print("Already on the earliest contract")

	def go_to_next_contract(self):
		next_address = call_function(landlord,self.contract, "getNext")
		if next_address:
			self.contract = w3.eth.contract(address=next, abi=mod_contract_interface)
			self.address = next_address
		else:
			print("Already at the updated contract")


rental = RentalAgreementManager()
while True:
	print(menu)
	choice = int(input())
	if choice == 1:
		rental.confirmAgreement()
	elif choice == 2:
		rental.payRent()
	elif choice == 3:
		rental.terminateContract()
	elif choice == 4:
		rental.deploy_another()
	elif choice == 5:
		rental.go_to_next_contract()
	elif choice == 6:
		rental.go_back_to_prev_contract()
	else:
		print("Invalid choice!")
