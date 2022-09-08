// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.4.22 <0.9.0;

contract protocolName{
    
    mapping(address => uint256) _addressDepositAmounts;
    address[] public _nonZeroDeposits;

    // _lastValidCheck must equal the current block number for protocols to accept transactions
    uint256 public _lastValidCheck;
    address _nullAddress=0;
    uint256 _alphaDenominator;
    uint256 _delta;

    constructor(uint256 alphaDenominator){
        _lastValidCheck=0;
        _alphaDenominator=alphaDenominator;
        _delta=1;
    }

    // to be run every block
    function _openTheGates(address[] _addresses, uint256[] _amounts) public payable returns (bool) {
        require (_addresses.length == _amounts.length, "arrays must be same length");
        uint256 _totalBid=0;
        for (uint256 i = 0; i < _addresses.length; i++) {
            if (_addressDepositAmounts[_addresses[i]]==0){
                _nonZeroDeposits.push(_addresses[i]);
            }
            _addressDepositAmounts[_addresses[i]]+= (
                SafeMath.div(_amounts[i],(_alphaDenominator*_alphaDenominator))-_delta);  
            _totalBid+=_amounts[i];
        }
        // send (1-\alpha) of bids to the proposer, and effectively burn the rest. See paper for details.
        payable(msg.sender).transfer(_totalBid - SafeMath.div(_totalBid,_alphaDenominator));
        _lastValidCheck=block.number;
    }

    function _distributeFunds() public payable returns (bool){
        for (uint256 i = 0; i < _nonZeroDeposits.length; i++) {
            payable(_nonZeroDeposits[i]).transfer(_addressDepositAmounts[_nonZeroDeposits[i]]);
            _addressDepositAmounts[_nonZeroDeposits[i]]=0;   
        }
        delete _nonZeroDeposits;
    }

    
}