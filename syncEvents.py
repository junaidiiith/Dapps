from web3.auto import w3
import time

def handle_event(event):
    print(event)

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main(contract):
    # block_filter = w3.eth.filter('latest')
    # log_loop(block_filter, 2)
    event_filter = contract.eventFilter(eventName, {'fromBlock': 0,'toBlock': 'latest'}) #needs work obviously

    log_loop(event_filter,2)

if __name__ == '__main__':
    main(contract)