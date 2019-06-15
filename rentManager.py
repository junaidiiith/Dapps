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
    	kwargs['from'] = kwargs['frm']
    	kwargs.pop('frm')
    except:
    	pass
    print(args,"----",kwargs)
    try:
    	print("Here!")
    	print(w3.fromWei(w3.eth.getBalance(account.address),'ether'))
    	print(w3.fromWei(kwargs['value'],'ether'))
    	print("there")
    except:
    	pass
    # try:
    txn = contract.get_function_by_name(function)(*args).buildTransaction(kwargs)
    print("built transaction")
    signed = account.signTransaction(txn)
    print("signed transaction")
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    print("sent transaction")
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt
    # except Exception:
    #     print("Some error occured while executing transaction!!")
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


url = "http://127.0.0.1:8545"
w3 = connect(url)
gas = 3000000
gasPrice = w3.eth.gasPrice




contract_interface = {"bin": json.load(open('rentAgreement.bin')), "abi": json.load(open('rentAgreement.abi'))}
mod_contract_interface = {"bin" : json.load(open('modifiedRentAgreement.bin')), "abi": json.load(open('modifiedRentAgreement.abi'))}

landlordprivateKey = "0x32f9f82ea7686b8dfc495055d698659c2b80666488e743407074b6de87e37da1"
tenantprivateKey = "0x788024e322ae06281a2a1613e2ac262f3ebe6d2f440577a64b58525a45e4fe8b"

landlord = w3.eth.account.privateKeyToAccount(landlordprivateKey)
tenant = w3.eth.account.privateKeyToAccount(tenantprivateKey)

m = dict()
m[landlord.address] = ('landlord', w3.eth.getBalance(landlord.address))
m[tenant.address] = ('tenant', w3.eth.getBalance(tenant.address))

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
		self.address = deploy_contract(landlord,contract_interface,w3.toWei(5,'ether'),"Junaid",
			frm=landlord.address,
			nonce= w3.eth.getTransactionCount(landlord.address),
			gas=gas,
			gasPrice=gasPrice)
		self.contract = w3.eth.contract(address=self.address, abi=contract_interface['abi'])

	def deploy_another(self, *args, **kwargs):
		new_address = deploy_contract(landlord,mod_contract_interface,w3.toWei(5,'ether'),w3.toWei(1,'ether'),"NewHouse",
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
			value = 6
		else:
			value = 5
		print(w3.fromWei(w3.toWei(value,'ether'), 'ether'))
		tx_receipt = do_transaction(tenant,self.contract, "payRent",
			nonce=w3.eth.getTransactionCount(tenant.address),
			frm=tenant.address,
			value=w3.toWei(value,'ether'),
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
	m[landlord.address] = ('landlord', w3.fromWei(w3.eth.getBalance(landlord.address),'ether'))
	m[tenant.address] = ('tenant', w3.fromWei(w3.eth.getBalance(tenant.address),'ether'))
	print(m)
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
