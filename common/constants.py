from enum import Enum

# https://plaid.com/docs/#account-types


class PlaidAccountType(Enum):
    BROKERAGE = "brokerage"
    CREDIT = "credit"
    DEPOSITORY = "depository"
    LOAN = "loan"
    OTHER = "other"


class PlaidDepositoryAccountSubtype(Enum):
    CD = "cd"
    CHECKING = "checking"
    SAVINGS = "savings"
    MONEY_MARKET = "money_market"
    PAYPAL = "paypal"
    PREPAID = "prepaid"


# NOTE: This is not an all-inclusive list (plaid.com/docs/#account-object)
class PlaidLoanAccountSubtype(Enum):
    LOAN = "loan"
    STUDENT = "student"
