# solana-token-holders

Shows the supply and the largest holders of a Solana SPL token using only RPC calls. SPL balances
live in token accounts rather than in wallets, so this takes three calls:

1. `getTokenSupply(mint)` for the total supply and decimals.
2. `getTokenLargestAccounts(mint)` for the 20 largest token accounts.
3. `getMultipleAccounts(accounts, jsonParsed)` for the owner wallet (or program) of each token
   account, since one owner can have several.

```bash
python holders.py JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN
python holders.py DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 --rpc https://your-rpc
```

The output shows the supply, the holders grouped by owner with their amount and share, and how much
of the supply the top 20 accounts hold together. A token where a few owners hold most of the supply
behaves very differently from a widely held one.

For very large mints such as USDC, `getTokenLargestAccounts` can be too expensive for the public RPC
and it returns an error. Use your own RPC for those.

## Tests

```bash
python -m unittest -v
```
