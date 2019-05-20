pragma solidity ^0.5.0;
import "./Vcontract.sol";

contract ModifiedRentalAgreement is vcontract {
    /* This declares a new complex type which will hold the paid rents*/
    struct PaidRentMaintence {
        uint id; /* The paid rent id*/
        uint rent; /* The amount of rent that is paid*/
        uint maintenence; /* The amount of maintenence that is paid*/
    }

    PaidRentMaintence[] public paidrents;

    uint public createdTimestamp;

    uint public rent;
    uint public maintenence;
    /* Combination of zip code and house number*/
    string public house;

    address payable public landlord;

    address public tenant;
    enum State {Created, Started, Terminated}
    State public state;

    constructor (uint _rent, uint _maintenence, string memory _house) public  {
        rent = _rent;
        house = _house;
        maintenence = _maintenence;
        landlord = msg.sender;
        createdTimestamp = block.timestamp;
        state = State.Created;
    }

    /* Events for DApps to listen to */
    event agreementConfirmed();

    event paidRent();

    event contractTerminated();
    
    event paidMaintenence();

    /* Confirm the lease agreement as tenant*/
    function confirmAgreement() public {
        require(msg.sender != landlord);
        require(state == State.Created);
        tenant = msg.sender;
        state = State.Started;
        emit agreementConfirmed();
    }
    
    function payRent() public payable{
        require (msg.sender == tenant);
        require(msg.value == (rent+maintenence));
        require(state == State.Started);
        landlord.transfer(rent);
        landlord.transfer(maintenence);
        emit paidMaintenence();
        paidrents.push(PaidRentMaintence({
        id : paidrents.length + 1,
        rent : rent,
        maintenence : maintenence
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