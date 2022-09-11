# ROLVR



# Protocol

ROLVR (pronounced rollover) is a fully permissionless trading protocol that recovers part of the MEV extracted by searchers and validators. ROLVR protocol enables Liquidity Providers to minimize their costs by auctioning off Top of Block MEV opportunities. The top of block rights to interact in a specific pool is selled to the highest bidder through a first-priced auction. This auction is run by an auctioneer, a player responsible for constructing bundles with the auctioning protocol mentioned in the following section. Once the on top of block auction is executed for a set of pools $P_1,...,P_k$, then all other composable bundles (interacting with $P_1,...,P_k$) transactions can be executed. Observe that this protocol is not incentive compatible since the auctioneer and the block proposal can arrenge side-payment agreements, capturing the MEV generated by the assets provided by LPs.


# Creation of Pools

Auctioneers create CFMMs (in general, we will assume that are Uniswap V2 pools, however this can be generalized to different CFMMs). The owner of the pools are saved in a variable owner. For each block, the first transaction of the block must change the bool variable **Trade** from **False** to **True**. In order to do so, the auctioneer must provide a signature of the blockNumber. The auctioneer imposes an auction mechanism to maximize their revenue. For each block, the auctioneer receives a set of bundles and transactions and construct the block with highest payload. Afterwards this payload can be splited among auctioneer, builder, LP providers and himself, to maximize the probablity of being included and to incentivize LP to provided liquidity.

We forked the uniswap v2 protocol. We allow each auctioneer to create its own Uniwap V2 Factory and pool. Before trading, each auctionner has to execute the function **open()** to be able to trade. In the future we will make this more gas efficient (Multicall open).

# MEV distribution

The auctioneer have different ways of splitting the MEV profits among LP to increase his pools liquidity. We will propose two categories to split the MEV.

- Ex-ante: The LP can add and remove liquidity in time $t_1$, $t_2$,.... Each slot of time $[t_i,t_{i+1}]$ the auctioneer commits to a payment in function of the variance and the price of the assets. This mechanism can be coded using a smart conctract and off-chain (and also on-chain) oracles. In general, this method is safer for the liquidity provider but generates more risk to the auctioneer. This will be translated to smaller payement to the LP since the auctioneer has to hedge the risk.
- Ex-post: The LP can add and remove liquidity in time $t_1$, $t_2$,.... The auctioneer reapays to the LPs a proportion of the MEV extracted per block. This method does not incurr any risk to the auctioneer. Moreover, is more capital efficient (no need of locking capital at time $t_i$). However, this is sensitive auctioneer deviations and off chain agreements between the auctionner and the Proposal. This leads to a higher need of trust among LPs and auctioneers.

# Auctioneer competition

Auctioneer compete to run auctions, and collect the associated fees. This competition incentivizes correct behaviour.

# Auctioneer cooperation

To be more capital, gas and MEV efficient, auctioneers can create collaborative factories using multisig keys, delegating auction rights to other auctioneers. To do so, auctioneers must trust each other, for example using smart contract deposits + slashing, ZK proofs of correct behavour, etc..


