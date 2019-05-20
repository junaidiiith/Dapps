pragma solidity ^0.5.0;
import "./Vcontract.sol";


contract RentalAgreement is vcontract {
    /* This declares a new complex type which will hold the paid rents*/
    struct PaidRent {
        uint id; /* The paid rent id*/
        uint value; /* The amount of rent that is paid*/
    }

    PaidRent[] public paidrents;

    uint public createdTimestamp;

    uint public rent;
    /* Combination of zip code and house number*/
    string public house;

    address public landlord;

    address public tenant;
    enum State {Created, Started, Terminated}
    State public state;

    constructor (uint _rent, string memory _house) public  {
        rent = _rent;
        house = _house;
        landlord = msg.sender;
        createdTimestamp = block.timestamp;
        state = State.Created;
    }

    /* Events for DApps to listen to */
    event agreementConfirmed();

    event paidRent();

    event contractTerminated();

    /* Confirm the lease agreement as tenant*/
    function confirmAgreement() public {
        require(msg.sender != landlord && state == State.Created);
        tenant = msg.sender;
        state = State.Started;
        emit agreementConfirmed();
    }

    function payRent() public payable{
        require (msg.sender == tenant && msg.value == rent && state == State.Started);
        landlord.transfer(msg.value);
        paidrents.push(PaidRent({
        id : paidrents.length + 1,
        value : msg.value
        }));
        emit paidRent();
    }
    /* Terminate the contract so the tenant can’t pay rent anymore,
    and the contract is terminated */
    function terminateContract() public payable
    {
        require (msg.sender == landlord);
        emit contractTerminated();
        landlord.transfer(address(this).balance);
        /* If there is any value on the
              contract send it to the landlord*/
        state = State.Terminated;
    }
}