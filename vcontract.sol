pragma solidity ^0.5.0;

contract vcontract{
    address private next;
    address private previous;
    
    function getNext() public view returns (address) {
        return next;    
    }
    function getPrev() public view returns (address) {
        return previous;    
    }

    function setNext(address _next) public {
        next = _next;    
    }
    function setPrev(address _prev) public {
        previous = _prev;    
    }
}