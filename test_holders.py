import unittest

from holders import group_by_owner


def parsed(owner):
    return {"data": {"parsed": {"info": {"owner": owner}}}}


class HoldersTest(unittest.TestCase):
    def test_groups_accounts_by_owner(self):
        largest = [{"address": "a1", "uiAmount": 100.0}, {"address": "a2", "uiAmount": 50.0}, {"address": "a3", "uiAmount": 70.0}]
        infos = [parsed("walletA"), parsed("walletB"), parsed("walletA")]
        self.assertEqual(group_by_owner(largest, infos), [("walletA", 170.0), ("walletB", 50.0)])

    def test_missing_account_info(self):
        self.assertEqual(group_by_owner([{"address": "x", "uiAmount": 1.0}], [None]), [("unknown", 1.0)])


if __name__ == "__main__":
    unittest.main()
