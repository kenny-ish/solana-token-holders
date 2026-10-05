"""Largest holders of a Solana SPL token via RPC."""
import argparse
import json
import time
import urllib.error
import urllib.request
from collections import defaultdict


def rpc(url, method, params, retries=4):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "User-Agent": "solana-token-holders"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                resp = json.load(r)
            break
        except urllib.error.HTTPError as e:
            # the public mainnet RPC answers bursts with 429; back off and retry
            if e.code != 429 or attempt == retries - 1:
                raise RuntimeError(f"{method}: HTTP {e.code}") from None
            time.sleep(2 ** (attempt + 1))
    if "error" in resp:
        raise RuntimeError(resp["error"].get("message"))
    return resp["result"]


def group_by_owner(largest, parsed_accounts):
    """Sum token amounts by owner. `largest` items: {address, uiAmount}; parsed accounts align with them."""
    owners = defaultdict(float)
    for acc, info in zip(largest, parsed_accounts):
        owner = "unknown"
        if info and isinstance(info.get("data"), dict):
            owner = info["data"]["parsed"]["info"].get("owner", "unknown")
        owners[owner] += acc.get("uiAmount") or 0.0
    return sorted(owners.items(), key=lambda kv: -kv[1])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mint")
    ap.add_argument("--rpc", default="https://api.mainnet-beta.solana.com")
    a = ap.parse_args()

    supply = rpc(a.rpc, "getTokenSupply", [a.mint])["value"]
    total = float(supply["uiAmountString"])
    try:
        largest = rpc(a.rpc, "getTokenLargestAccounts", [a.mint])["value"]
    except RuntimeError as e:
        raise SystemExit(f"getTokenLargestAccounts failed ({e}); large mints need your own RPC")
    infos = rpc(a.rpc, "getMultipleAccounts", [[x["address"] for x in largest], {"encoding": "jsonParsed"}])["value"]

    print(f"mint     {a.mint}")
    print(f"supply   {total:,.2f} (decimals {supply['decimals']})\n")
    print(f"{'owner':<46}{'amount':>22}{'share':>9}")
    grouped = group_by_owner(largest, infos)
    for owner, amount in grouped:
        print(f"{owner:<46}{amount:>22,.2f}{amount / total:>9.2%}")
    top = sum(x.get("uiAmount") or 0 for x in largest)
    print(f"\ntop {len(largest)} token accounts ({len(grouped)} owners) hold {top / total:.1%} of supply")


if __name__ == "__main__":
    main()
