pragma solidity ^0.5.0;
contract PropertyLease {
//StatesDefinition
    enum States {
        Created, PropertyAssessed, Paid, AwaitingPay, Conflict,
    PaidExtended, AwaitingPayExtended, ConflictExtended, FinalToBePaid,
    LeaseEnd, LeaseClosed, Finished
    }
    States public state = States.Created;
    //VariablesDefinition
    uint public securityDeposit;
    uint public rent;
    uint public fine;
    uint public deposit;
    uint monthCounter;
    uint rentCounter;
    uint creationTime;
    bool private payDepositTrue;
    bool private notice;
    bool assess;
    address public landlord;
    address public tenant;
    address public propertymanager;
    
     // Locking
     bool private locked = false ;
     modifier locking {
         require (! locked );
         locked = true ;
         _;
         locked = false ;
     }
     // Transition counter
     uint private transitionCounter = 0;
     modifier transitionCounting ( uint nextTransitionNumber ) {
         require ( nextTransitionNumber == transitionCounter );
         transitionCounter += 1;
         _;
     }
    // Timed transtion
    modifier timedTransitions {
        if ((state == States.Paid) && (now >= rentCounter + 30 days))
            {state = States.AwaitingPay;}
        
        if ((state == States.AwaitingPay) && (now >= rentCounter + 35
        days))
            {state = States.Conflict;}
        
        if ((state == States.PaidExtended) && (now >= rentCounter + 30
        days))
            {state = States.AwaitingPayExtended;}
        
        if ((state == States.AwaitingPayExtended) && (now >= rentCounter
        + 35 days))
            {state = States.ConflictExtended;}
        _;
    }
    //Constructor function
     constructor (uint inputRent, uint inputFine) public {
        landlord = msg.sender;
        rent = inputRent;
        fine = inputFine;
        creationTime = now;
        securityDeposit = 2 * inputRent;
    }
    function Assess (uint nextTransitionNumber) locking 
    transitionCounting ( nextTransitionNumber ) public { 
        require (state == States.Created);
         // Statements
        state == States.PropertyAssessed;
    }
    function PayDeposit (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber ) public
    {
        require (state == States.PropertyAssessed);
     // Statements
        state == States.Paid;
    }
    function RentDue (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber )
    timedTransitions private
    {
        require (state == States.Paid);
     // Statements
        state == States.AwaitingPay;
    }
    
    function RentDueExtended (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber )
    timedTransitions private
    {
        require (state == States.PaidExtended);
     // Statements
        state == States.AwaitingPayExtended; 
    }
    function PayRent (uint nextTransitionNumber) payable
    locking
    transitionCounting ( nextTransitionNumber ) public
    {
        require (state == States.AwaitingPay);
     // Statements
        state == States.Paid;
    }
    function PayRentExtended (uint nextTransitionNumber) payable
    locking
    transitionCounting ( nextTransitionNumber ) public
    {
        require (state == States.AwaitingPayExtended);
     // Statements
        state == States.PaidExtended;
    }
    function PayRentFinal (uint nextTransitionNumber) payable
    locking
    transitionCounting ( nextTransitionNumber ) public
    {
        require (state == States.FinalToBePaid);
 // Statements
        state == States.LeaseEnd;
    }
    function RentLate (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber )
    timedTransitions private
    {
        require (state == States.AwaitingPay);
 // Statements
        state == States.Conflict;
    }
    function RentLateExtended (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber )
    timedTransitions private
    { require (state == States.AwaitingPayExtended);
        // Statements
        state == States.ConflictExtended;
    }
    
    function PayLate (uint nextTransitionNumber) payable
    locking
    transitionCounting ( nextTransitionNumber ) public
    {
        require (state == States.Conflict);
     // Statements
        state == States.Paid;
    }
    function PayLateExtended (uint nextTransitionNumber) payable
    locking
    transitionCounting ( nextTransitionNumber ) public
    {
        require (state == States.Conflict);
     // Statements
        state == States.Paid;
    } 

    function PayLateFinal (uint nextTransitionNumber) payable
    locking
    transitionCounting ( nextTransitionNumber ) public
    {
        require (state == States.ConflictExtended);
        require (notice == true);
     // Statements
        state == States.Paid;
    }
    
    function TerminateContract (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber )
    timedTransitions private
    {
        require (state == States.Conflict);
     // Statements
        state == States.Finished;
    }
    function TerminateContractExtended (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber )
    timedTransitions private
    {
        require (state == States.ConflictExtended);
     // Statements
        state == States.Finished;
    }
    
    function Extend (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber ) private
    {
        require (state == States.Paid);
     // Statements
        state == States.PaidExtended;
    }
    function EarlyTerminate (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber ) private
    {
        require (state == States.Paid);
     // Statements
        state == States.FinalToBePaid;
    }
    function EndLease (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber ) private
    {
        require (state == States.Paid);
     // Statements
        state == States.LeaseEnd;
    }
    function GiveNotice (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber ) public
    {
        require (state == States.AwaitingPayExtended);
     // Statements
        state == States.FinalToBePaid;
    }
    function ReturnDeposit (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber ) public
    {
        require (state == States.LeaseEnd);
        require (assess = true);
     // Statements
        state == States.Finished;
    }
    
    function DepositRetract (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber ) private
    {
        require (state == States.LeaseEnd);
        require (assess = false);
     // Statements
        state == States.Finished;
    }
    function ReturnDepositLate (uint nextTransitionNumber) private
    locking
    transitionCounting ( nextTransitionNumber )
    {
        require (state == States.LeaseClosed);
        require (assess = true);
     // Statements
        state == States.Finished;
    }
    
    function DepositRetractLate (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber ) private
    {
        require (state == States.LeaseClosed);
        require (assess = false);
     // Statements
        state == States.Finished;
    }
    
    function EndLeaseFinal (uint nextTransitionNumber)
    locking
    transitionCounting ( nextTransitionNumber ) private
    {
        require (state == States.LeaseEnd);
     // Statements
        state == States.Finished;
    }
}
