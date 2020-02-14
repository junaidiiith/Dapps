from django.shortcuts import render
from buyerseller.forms import DocumentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import DefaultStorage
import json
from buyerseller.forms import CustomForm
from buyerseller.models import *
from users.models import Profile
from RentalDapp.web3Connection import *
from RentalDapp.rentalManager import *


url = "http://127.0.0.1:7545"

def connect(url):
    return Web3(Web3.HTTPProvider(url))

w3 = connect(url)
gas = 3000000
gasPrice = w3.eth.gasPrice


def get_owned(user):
	contracts = [contract for contract in Contract.objects.all() for stakeholder in Stakeholder.objects.all() if stakeholder.user == user and stakeholder.type == 1 and contract.landlord == stakeholder and contract.current == 1]
	modified_contracts = list()
	for contract in contracts:
		if contract.tenant:
			c = w3.eth.contract(address=contract.address, abi=contract.abi)
			if c.caller().getNext() != '0x0000000000000000000000000000000000000000':
				contract.next = True
			if c.caller().getPrev() != '0x0000000000000000000000000000000000000000':
				contract.prev = True
		modified_contracts.append(contract)

	return modified_contracts

def get_bought(user):
	return [contract for contract in Contract.objects.all() for stakeholder in Stakeholder.objects.all() if stakeholder.user == user and stakeholder.type == 2 and contract.tenant == stakeholder and contract.current == 1]

def get_balance(user):
	return w3.fromWei(w3.eth.getBalance(w3.eth.account.privateKeyToAccount(user.private_key).address), 'ether')

def get_terminated(user):
	landlord = Stakeholder.objects.filter(user=user, type=1)
	if landlord:
		landlord = landlord[0]

	tenant = Stakeholder.objects.filter(user=user, type=2)
	if tenant:
		tenant = tenant[0]
	return [contract for contract in Contract.objects.all() if contract.current == 0 and (contract.landlord == landlord or contract.tenant == tenant) ]


def home(request):
	uploads = Document.objects.all()
	owned_contracts, tenant_contracts, unconfirmed_contracts, terminated_contracts = list(), list(), list(), list()
	user = request.user
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=request.user)
		owned_contracts = get_owned(profile)
		tenant_contracts = get_bought(profile)
		terminated_contracts = get_terminated(profile)
		print(profile)
		try:
			landlord = Stakeholder.objects.filter(user=profile, type=1)[0]
		except:
			landlord = None
		print(landlord)
		unconfirmed_contracts = [contract for contract in Contract.objects.all() if not contract.tenant and contract.landlord != landlord and contract.current == 1]
		user.balance = get_balance(profile)


	return render(request, 'home.html', {'user': user, 'uploads': uploads, 'bought_contracts': tenant_contracts, 'sold_contracts': owned_contracts, 'unconfirmed_contracts': unconfirmed_contracts, 'terminated_contracts': terminated_contracts})

def upload(request):
    if request.method == 'POST':
    	form = DocumentForm(request.POST, request.FILES)
    	if form.is_valid():
    		print('saving form here')
    		form.save()
    		return redirect('home')
    	else:
    		return HttpResponse('Invalid form')
    else:
    	form = DocumentForm()
    return render(request, 'upload.html', {
		'form': form
	})


def deploy(request, pk):
	document = get_object_or_404(Document, id=pk)
	# print(document.abi.read())
	abi = json.loads(document.abi.read())
	bytecode = json.loads(document.bytecode.read())
	fields = list()
	# print(functions)
	for function in abi:
		if function['type'] == 'constructor':
			fields = function['inputs']
			break

	if request.method == 'POST':
		form = CustomForm(fields, request.POST, request.FILES)
		# print(form)
		if form.is_valid():
			print("Form valid")
			# print(form.data)
			# print(form.cleaned_data['_rent'], form.cleaned_data['_house'])
			profile = Profile.objects.get(user=request.user)
			print(profile)
			try:
				stakeholder = Stakeholder.objects.filter(user=profile, type=1)[0]
				# print("stakeholder found")
			except:
				stakeholder = Stakeholder(user=profile, type=1)
				stakeholder.save()
			

			account = w3.eth.account.privateKeyToAccount(profile.private_key)

			# print(contract_interface, account)
			contract_interface = {"abi": abi, "bin": bytecode}
			contract_address = deploy_contract(account, contract_interface, w3.toWei(int(form.cleaned_data['_rent']), 'ether'), form.cleaned_data['_house'], frm=account.address,
			nonce=w3.eth.getTransactionCount(account.address), gas=gas, gasPrice=gasPrice)
			contract = Contract(address=contract_address, current=True, landlord=stakeholder, abi=abi, name=document.name)
			contract.save()
			print("Contract saved!")
		else:
			print("Form invalid")
		return redirect('home')
	else:
		form = CustomForm(fields)
		print(form)
	return render(request, 'deploy.html', {'user': request.user, 'form': form})


def confirmAgreement(request, pk):
	contract_ = get_object_or_404(Contract,id=pk)
	contract = w3.eth.contract(address=contract_.address, abi=contract_.abi)
	profile = Profile.objects.get(user=request.user)
	stakeholder = Stakeholder(user=profile, type=2)
	stakeholder.save()
	account = w3.eth.account.privateKeyToAccount(profile.private_key)

	tx_reciept = do_transaction(account, contract, "confirmAgreement",
			nonce=w3.eth.getTransactionCount(account.address),
			frm=account.address,
			gas=gas,
			gasPrice=gasPrice)
			# ,value=contract.caller().deposit())

	print("Agreement Confirmed! with: ", tx_reciept)

	contract_.tenant = stakeholder
	contract_.save()

	return redirect('home')


def pay(request, pk):
	contract_ = get_object_or_404(Contract,id=pk)
	contract = w3.eth.contract(address=contract_.address, abi=contract_.abi)
	profile = Profile.objects.get(user=request.user)
	value = contract.caller().rent()
	try:
		value += contract.caller().maintenence()
	except:
		value += 0
	account = w3.eth.account.privateKeyToAccount(profile.private_key)
	tx_receipt = do_transaction(account, contract, "payRent",
			nonce=w3.eth.getTransactionCount(account.address),
			frm=account.address,
			value=value,
			gas=gas,
			gasPrice=gasPrice)
	print(tx_receipt)
	print("Payment received!")

	return redirect('home')


def terminateContract(request, pk):
	contract_ = get_object_or_404(Contract,id=pk)
	contract = w3.eth.contract(address=contract_.address, abi=contract_.abi)
	profile = Profile.objects.get(user=request.user)

	account = w3.eth.account.privateKeyToAccount(profile.private_key)
	tx_reciept = do_transaction(account, contract, "terminateContract",
			nonce=w3.eth.getTransactionCount(account.address),
			frm=account.address,
			gas=gas,
			gasPrice=gasPrice)
	contract_.current = 0
	contract_.save()
	print("Contract terminated")
	print(tx_reciept)
	return redirect('home')

def deploy_with_confirmation(request, doc_id, c_id):
	previous_contract = get_object_or_404(Contract, id=c_id)
	tenant = previous_contract.tenant
	landlord = previous_contract.landlord

	document = get_object_or_404(Document, id=doc_id)
	abi = json.loads(document.abi.read())
	bytecode = json.loads(document.bytecode.read())
	
	fields = list()
	for function in abi:
		if function['type'] == 'constructor':
			fields = function['inputs']
			break

	if request.method == 'POST':
		form = CustomForm(fields, request.POST, request.FILES)
		print(form)
		if form.is_valid():
			print("Form valid")	
			print(form)
			account = w3.eth.account.privateKeyToAccount(landlord.user.private_key)

			# print(contract_interface, account)
			contract_interface = {"abi": abi, "bin": bytecode}
			contract_address = deploy_contract(account, contract_interface, w3.toWei(int(form.cleaned_data['_rent']), 'ether'), w3.toWei(int(form.cleaned_data['_maintenence']), 'ether'),
			form.cleaned_data['_house'], 
			frm=account.address, nonce=w3.eth.getTransactionCount(account.address), gas=gas, gasPrice=gasPrice)

			contract = Contract(address=contract_address, current=True, landlord=landlord, abi=abi, name=document.name)
			contract.save()
			print("Contract saved!")

			old_contract = w3.eth.contract(address=previous_contract.address, abi=previous_contract.abi)
			new_contract = w3.eth.contract(address=contract.address, abi=contract.abi)

			do_transaction(account, old_contract,"setNext", contract.address,
			nonce=w3.eth.getTransactionCount(account.address),
			gas=gas,
			gasPrice=gasPrice)
			
			do_transaction(account,new_contract,"setPrev", previous_contract.address,
			nonce=w3.eth.getTransactionCount(account.address),
			gas=gas,
			gasPrice=gasPrice)

			tenant_account = w3.eth.account.privateKeyToAccount(tenant.user.private_key)

			# add previous transactions list code

			previous_contract.current = 2
			previous_contract.save()
		else:
			print("Form invalid")
		return redirect('home')
	else:
		form = CustomForm(fields)
		print(form)
	return render(request, 'deploy.html', {'user': request.user, 'form': form})

def deploy_next(request, pk):
    contract = get_object_or_404(Contract, id=pk)
    uploads = Document.objects.all()
    if request.method == 'POST':
    	form = DocumentForm(request.POST, request.FILES)
    	if form.is_valid():
    		print('saving form here')
    		doc = form.save()
    		print(doc.id, doc.abi, contract.id)
    	else:
    		return HttpResponse('Invalid form')
    else:
    	form = DocumentForm()
    return render(request, 'deploy_next.html', {
		'form': form, 'uploads': uploads, 'contract': contract
    })

def shift_next(request, pk):
	contract_ = get_object_or_404(Contract, id=pk)
	contract_.current = 2
	contract_.save()
	contract = w3.eth.contract(address=contract_.address, abi=contract_.abi)
	new_contract = Contract.objects.filter(address=contract.caller().getNext())[0]
	new_contract.current = 1
	new_contract.save()
	return redirect('home')

def shift_prev(request, pk):
	contract_ = get_object_or_404(Contract, id=pk)
	contract_.current = 2
	contract_.save()
	contract = w3.eth.contract(address=contract_.address, abi=contract_.abi)
	new_contract = Contract.objects.filter(address=contract.caller().getPrev())[0]
	new_contract.current = 1
	new_contract.save()
	return redirect('home')




def modify(request, old_contract, new_contract, *args, **kwargs):
	profile = Profile.objects.get(user=request.user)
	account = profile.address
	do_transaction(account, old_contract,"setNext", contract.address,
			nonce=w3.eth.getTransactionCount(account.address),
			gas=gas,
			gasPrice=gasPrice)
			
	do_transaction(account,new_contract,"setPrev", previous_contract.address,
			nonce=w3.eth.getTransactionCount(account.address),
			gas=gas,
			gasPrice=gasPrice)
	deploy(account, new_contract)
	

