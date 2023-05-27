from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db
# from server import mongoDB_master_access
from flask_login import login_required


Bank_Analysis_Blueprint = Blueprint('MCA_Bank_Analysis', __name__)
@Bank_Analysis_Blueprint.route('/api/funder/advances/pre_funded/bank_analysis/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_Bank_Analysis():




    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    else:

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]



        get_company = mongoDB.Company.find()






        anylitic_response =  {
            "average_daily_balance": "8931.06",
            "average_deposit_by_month": {
              "02/2020": 'null',
              "01/2020": "2667.62"
            },
            "average_daily_balance_by_month": {
              "01/2020": "7127.41",
              "02/2020": "11012.19"
            },
            "cash_expense_days_by_month": {
              "01/2020": "53.34",
              "02/2020": "600.12"
            },
            "txn_count": 13,
            "daily_balances_weekday": {
              "01/17/2020": "8302.77",
              "01/20/2020": "8302.77",
              "01/21/2020": "8302.77",
              "01/22/2020": "8302.77",
              "01/23/2020": "8302.77",
              "01/24/2020": "6592.77",
              "01/27/2020": "6115.18",
              "01/28/2020": "4160.28",
              "01/29/2020": "4160.28",
              "01/30/2020": "4160.28",
              "01/31/2020": "11372.61",
              "02/03/2020": "11372.61",
              "02/04/2020": "11319.30",
              "02/05/2020": "10919.30",
              "02/06/2020": "10919.30",
              "02/07/2020": "10840.39",
              "02/10/2020": "10840.39",
              "02/11/2020": "10840.39",
              "02/12/2020": "10840.39",
              "02/13/2020": "10840.39"
            },
            "mca_payments_by_month": {
              "01/2020": "0.00",
              "02/2020": "0.00"
            },
            "estimated_daily_expense_by_month": {
              "01/2020": "133.63",
              "02/2020": "18.35"
            },
            "estimated_revenue_by_month": {
              "01/2020": "10645.46",
              "02/2020": "0.00"
            },
            "average_by_month": {
              "02/2020": "177.41",
              "01/2020": "1483.80"
            },
            "negative_balances_by_month_weekday": {
              "01/2020": [],
              "02/2020": []
            },
            "deposit_sum": "10670.46",
            "withdrawal_sum": "-4699.71",
            "daily_balances_weekday_by_month": {
              "01/2020": {
                "01/17/2020": "8302.77",
                "01/20/2020": "8302.77",
                "01/21/2020": "8302.77",
                "01/22/2020": "8302.77",
                "01/23/2020": "8302.77",
                "01/24/2020": "6592.77",
                "01/27/2020": "6115.18",
                "01/28/2020": "4160.28",
                "01/29/2020": "4160.28",
                "01/30/2020": "4160.28",
                "01/31/2020": "11372.61"
              },
              "02/2020": {
                "02/03/2020": "11372.61",
                "02/04/2020": "11319.30",
                "02/05/2020": "10919.30",
                "02/06/2020": "10919.30",
                "02/07/2020": "10840.39",
                "02/10/2020": "10840.39",
                "02/11/2020": "10840.39",
                "02/12/2020": "10840.39",
                "02/13/2020": "10840.39"
              }
            },
            "daily_balances_by_month": {
              "01/2020": {
                "01/17/2020": "8302.77",
                "01/18/2020": "8302.77",
                "01/19/2020": "8302.77",
                "01/20/2020": "8302.77",
                "01/21/2020": "8302.77",
                "01/22/2020": "8302.77",
                "01/23/2020": "8302.77",
                "01/24/2020": "6592.77",
                "01/25/2020": "6115.18",
                "01/26/2020": "6115.18",
                "01/27/2020": "6115.18",
                "01/28/2020": "4160.28",
                "01/29/2020": "4160.28",
                "01/30/2020": "4160.28",
                "01/31/2020": "11372.61"
              },
              "02/2020": {
                "02/01/2020": "11372.61",
                "02/02/2020": "11372.61",
                "02/03/2020": "11372.61",
                "02/04/2020": "11319.30",
                "02/05/2020": "10919.30",
                "02/06/2020": "10919.30",
                "02/07/2020": "10840.39",
                "02/08/2020": "10840.39",
                "02/09/2020": "10840.39",
                "02/10/2020": "10840.39",
                "02/11/2020": "10840.39",
                "02/12/2020": "10840.39",
                "02/13/2020": "10840.39"
              }
            },
            "alt_lender_payments_by_month": {
              "01/2020": "0.00",
              "02/2020": "0.00"
            },
            "negative_balances_by_month": {
              "01/2020": [],
              "02/2020": []
            },
            "estimated_expense_by_month": {
              "01/2020": "4142.49",
              "02/2020": "532.22"
            },
            "withdrawal_count": 9,
            "daily_balances": {
              "01/17/2020": "8302.77",
              "01/18/2020": "8302.77",
              "01/19/2020": "8302.77",
              "01/20/2020": "8302.77",
              "01/21/2020": "8302.77",
              "01/22/2020": "8302.77",
              "01/23/2020": "8302.77",
              "01/24/2020": "6592.77",
              "01/25/2020": "6115.18",
              "01/26/2020": "6115.18",
              "01/27/2020": "6115.18",
              "01/28/2020": "4160.28",
              "01/29/2020": "4160.28",
              "01/30/2020": "4160.28",
              "01/31/2020": "11372.61",
              "02/01/2020": "11372.61",
              "02/02/2020": "11372.61",
              "02/03/2020": "11372.61",
              "02/04/2020": "11319.30",
              "02/05/2020": "10919.30",
              "02/06/2020": "10919.30",
              "02/07/2020": "10840.39",
              "02/08/2020": "10840.39",
              "02/09/2020": "10840.39",
              "02/10/2020": "10840.39",
              "02/11/2020": "10840.39",
              "02/12/2020": "10840.39",
              "02/13/2020": "10840.39"
            },
            "deposit_count": 4,
            "pk": 15616113,
            "name": "af5b6d2911d959f7908ec549325a0091",
            "bank_accounts": [
              {
                "pk": 8159848,
                "book_pk": 15616113,
                "name": "900090009 BANK OF AMERICA CHECKING",
                "bank_name": "BANK OF AMERICA",
                "activity_info": {
                  "active": [
                    {
                      "start": {
                        "year": 2020,
                        "month": 1,
                        "day": 17
                      },
                      "end": {
                        "year": 2020,
                        "month": 2,
                        "day": 13
                      }
                    }
                  ],
                  "missing": []
                },
                "account_type": "CHECKING",
                "account_holder": "Sam Bobley",
                "account_number": "900090009",
                "holder_zip": "10006",
                "holder_country": "US",
                "holder_state": "NY",
                "holder_city": "New York",
                "holder_address_1": "101 Greenwich St",
                "holder_address_2": "FL 23",
                "account_category": "PERSONAL ACCOUNT",
                "id": 8159848,
                "periods": [
                  {
                    "calculated_end_balance": "10285.43",
                    "period_month_txns": {
                      "01/2020": 9,
                      "02/2020": 3
                    },
                    "period_month_days": {
                      "01/2020": 11,
                      "02/2020": 9
                    },
                    "pk": 22623168,
                    "uuid": "3231bc17-c538-492d-a343-2b04148a4555",
                    "bank_account_pk": 8159848,
                    "begin_date": "01/17/2020",
                    "end_date": "02/13/2020",
                    "begin_balance": "4339.68",
                    "end_balance": "10530.87",
                    "primary_recon_error_reason": "File Tampering Detected",
                    "secondary_recon_error_reason": "Tampering on pages: [1, 3, 4, 5]",
                    "uploaded_doc_pk": 34706486
                  }
                ],
                "account_holders": [
                  "Sam Bobley"
                ],
                "average_by_month": {
                  "01/2020": "1645.88",
                  "02/2020": "177.41"
                },
                "daily_balances": {
                  "01/17/2020": "7772.81",
                  "01/18/2020": "7772.81",
                  "01/19/2020": "7772.81",
                  "01/20/2020": "7772.81",
                  "01/21/2020": "7772.81",
                  "01/22/2020": "7772.81",
                  "01/23/2020": "7772.81",
                  "01/24/2020": "6062.81",
                  "01/25/2020": "5560.22",
                  "01/26/2020": "5560.22",
                  "01/27/2020": "5560.22",
                  "01/28/2020": "3605.32",
                  "01/29/2020": "3605.32",
                  "01/30/2020": "3605.32",
                  "01/31/2020": "10817.65",
                  "02/01/2020": "10817.65",
                  "02/02/2020": "10817.65",
                  "02/03/2020": "10817.65",
                  "02/04/2020": "10764.34",
                  "02/05/2020": "10364.34",
                  "02/06/2020": "10364.34",
                  "02/07/2020": "10285.43",
                  "02/08/2020": "10285.43",
                  "02/09/2020": "10285.43",
                  "02/10/2020": "10285.43",
                  "02/11/2020": "10285.43",
                  "02/12/2020": "10285.43",
                  "02/13/2020": "10285.43"
                },
                "deposit_min_by_month": {
                  "01/2020": [
                    {
                      "page_idx": 2,
                      "bank_account_pk": 8159848,
                      "amount": "3433.13",
                      "bbox": [
                        231,
                        2664,
                        3763,
                        2747
                      ],
                      "txn_date": "01/17/2020",
                      "page_doc_pk": 169980203,
                      "pk": 2156721582,
                      "uploaded_doc_pk": 34706486,
                      "description": "INSIKT INC DES:DEPOSIT ID 350209 CAPGEMINI AMERICA INC CO ID:11775843 PPD"
                    }
                  ],
                  "02/2020": 'null'
                },
                "nsf_transactions": [],
                "daily_cash_flows": {
                  "01/17/2020": "3433.13",
                  "01/18/2020": "0",
                  "01/19/2020": "0",
                  "01/20/2020": "0",
                  "01/21/2020": "0",
                  "01/22/2020": "0",
                  "01/23/2020": "0",
                  "01/24/2020": "-1710.00",
                  "01/25/2020": "-502.59",
                  "01/26/2020": "0",
                  "01/27/2020": "0",
                  "01/28/2020": "-1954.90",
                  "01/29/2020": "0",
                  "01/30/2020": "0",
                  "01/31/2020": "7212.33",
                  "02/01/2020": "0",
                  "02/02/2020": "0",
                  "02/03/2020": "0",
                  "02/04/2020": "-53.31",
                  "02/05/2020": "-400.00",
                  "02/06/2020": "0",
                  "02/07/2020": "-78.91",
                  "02/08/2020": "0",
                  "02/09/2020": "0",
                  "02/10/2020": "0",
                  "02/11/2020": "0",
                  "02/12/2020": "0",
                  "02/13/2020": "0"
                },
                "insurance_credits": [],
                "withdrawal_sum": "-4699.71",
                "deposits_sum_by_month": {
                  "01/2020": "10645.46",
                  "02/2020": "0.00"
                },
                "withdrawals_max_by_month": {
                  "01/2020": [
                    {
                      "page_idx": 3,
                      "bank_account_pk": 8159848,
                      "amount": "-1954.90",
                      "bbox": [
                        233,
                        2374,
                        3752,
                        2526
                      ],
                      "txn_date": "01/28/2020",
                      "page_doc_pk": 169980201,
                      "pk": 2156721592,
                      "uploaded_doc_pk": 34706486,
                      "description": "CITI CARD ONLINE DES:PAYMENT ID:132867132295963 INDN:SIRISHA CHIGURUPATI CO\nID:CITICTP WEB"
                    }
                  ],
                  "02/2020": [
                    {
                      "page_idx": 3,
                      "bank_account_pk": 8159848,
                      "amount": "-400.00",
                      "bbox": [
                        233,
                        1122,
                        3752,
                        1205
                      ],
                      "txn_date": "02/05/2020",
                      "page_doc_pk": 169980201,
                      "pk": 2156721587,
                      "uploaded_doc_pk": 34706486,
                      "description": "BKOFAMERICA ATM 02/05 #000005706 WITHDRWL CANOGA PARK CANOGA PARK CA"
                    }
                  ]
                },
                "estimated_revenue_by_month": {
                  "01/2020": "10645.46",
                  "02/2020": "0.00"
                },
                "round_number_txns": [],
                "deposit_sum": "10645.46",
                "alt_lender_payments_by_month": {
                  "01/2020": "0.00",
                  "02/2020": "0.00"
                },
                "period_balance_mismatches": [],
                "negative_balances_by_month": {
                  "01/2020": [],
                  "02/2020": []
                },
                "deposit_max_by_month": {
                  "01/2020": [
                    {
                      "page_idx": 2,
                      "bank_account_pk": 8159848,
                      "amount": "3664.67",
                      "bbox": [
                        232,
                        2782,
                        3751,
                        2866
                      ],
                      "txn_date": "01/31/2020",
                      "page_doc_pk": 169980203,
                      "pk": 2156721583,
                      "uploaded_doc_pk": 34706486,
                      "description": "INSIKT INC DES:DEPOSIT ID:350209 INDN:CHIGURUPATI SIRISHA CO ID:11775843 PPD"
                    }
                  ],
                  "02/2020": 'null'
                },
                "ppp_loan_txns": [],
                "average_daily_balance_by_month": {
                  "01/2020": "6585.78",
                  "02/2020": "10457.23"
                },
                "withdrawals_sum_by_month": {
                  "01/2020": "4167.49",
                  "02/2020": "532.22"
                },
                "interbank_transactions": [
                  {
                    "page_idx": 3,
                    "bank_account_pk": 8159848,
                    "amount": "-1510.00",
                    "bbox": [
                      233,
                      1764,
                      3751,
                      1846
                    ],
                    "txn_date": "01/24/2020",
                    "page_doc_pk": 169980201,
                    "pk": 2156721588,
                    "uploaded_doc_pk": 34706486,
                    "description": "BANK OF AMERICA CREDIT CARD BILL PAYMENT"
                  },
                  {
                    "page_idx": 3,
                    "bank_account_pk": 8159848,
                    "amount": "-293.13",
                    "bbox": [
                      233,
                      1881,
                      3753,
                      2034
                    ],
                    "txn_date": "01/25/2020",
                    "page_doc_pk": 169980201,
                    "pk": 2156721589,
                    "uploaded_doc_pk": 34706486,
                    "description": "AMERICAN EXPRESS DES:ACH PMT ID:WL 674 INDN:SIRISHA CHIGURUPATI CO\nID:1133133497 WEB"
                  },
                  {
                    "page_idx": 3,
                    "bank_account_pk": 8159848,
                    "amount": "-184.46",
                    "bbox": [
                      233,
                      2069,
                      3785,
                      2222
                    ],
                    "txn_date": "01/25/2020",
                    "page_doc_pk": 169980201,
                    "pk": 2156721590,
                    "uploaded_doc_pk": 34706486,
                    "description": "AMERICAN EXPRESS DES:ACH PMT ID:W0914 INDN:SIRISHA CHIGURUPATI CO\nID:1133133497 WEB"
                  },
                  {
                    "page_idx": 3,
                    "bank_account_pk": 8159848,
                    "amount": "-1954.90",
                    "bbox": [
                      233,
                      2374,
                      3752,
                      2526
                    ],
                    "txn_date": "01/28/2020",
                    "page_doc_pk": 169980201,
                    "pk": 2156721592,
                    "uploaded_doc_pk": 34706486,
                    "description": "CITI CARD ONLINE DES:PAYMENT ID:132867132295963 INDN:SIRISHA CHIGURUPATI CO\nID:CITICTP WEB"
                  }
                ],
                "mca_payments_by_month": {
                  "01/2020": "0.00",
                  "02/2020": "0.00"
                },
                "alternative_lender_transactions": [],
                "estimated_expense_by_month": {
                  "01/2020": "4142.49",
                  "02/2020": "532.22"
                },
                "total_days": 28,
                "average_deposit_by_month": {
                  "01/2020": "3548.49",
                  "02/2020": 'null'
                },
                "deposits_count_by_month": {
                  "01/2020": 3,
                  "02/2020": 0
                },
                "deposit_count": 3,
                "withdrawal_count": 9,
                "average_daily_balance": "8383.24",
                "minimum_balance_by_month": {
                  "01/2020": "3605.32",
                  "02/2020": "10285.43"
                },
                "outside_source_deposits": [
                  {
                    "page_idx": 2,
                    "bank_account_pk": 8159848,
                    "amount": "3433.13",
                    "bbox": [
                      231,
                      2664,
                      3763,
                      2747
                    ],
                    "txn_date": "01/17/2020",
                    "page_doc_pk": 169980203,
                    "pk": 2156721582,
                    "uploaded_doc_pk": 34706486,
                    "description": "INSIKT INC DES:DEPOSIT ID 350209 CAPGEMINI AMERICA INC CO ID:11775843 PPD"
                  },
                  {
                    "page_idx": 2,
                    "bank_account_pk": 8159848,
                    "amount": "3664.67",
                    "bbox": [
                      232,
                      2782,
                      3751,
                      2866
                    ],
                    "txn_date": "01/31/2020",
                    "page_doc_pk": 169980203,
                    "pk": 2156721583,
                    "uploaded_doc_pk": 34706486,
                    "description": "INSIKT INC DES:DEPOSIT ID:350209 INDN:CHIGURUPATI SIRISHA CO ID:11775843 PPD"
                  },
                  {
                    "page_idx": 2,
                    "bank_account_pk": 8159848,
                    "amount": "3547.66",
                    "bbox": [
                      232,
                      2900,
                      3750,
                      2983
                    ],
                    "txn_date": "01/31/2020",
                    "page_doc_pk": 169980203,
                    "pk": 2156721584,
                    "uploaded_doc_pk": 34706486,
                    "description": "INSIKT INC DES:DEPOSIT ID:350209 INDN:CHIGURUPATI SIRISHA CO ID:11775843 PPD"
                  }
                ],
                "insurance_debits": [],
                "txn_count": 12
              },
              {
                "pk": 8159849,
                "book_pk": 15616113,
                "name": "900090009 BANK OF AMERICA SAVINGS",
                "bank_name": "BANK OF AMERICA",
                "activity_info": {
                  "active": [
                    {
                      "start": {
                        "year": 2020,
                        "month": 1,
                        "day": 17
                      },
                      "end": {
                        "year": 2020,
                        "month": 2,
                        "day": 13
                      }
                    }
                  ],
                  "missing": []
                },
                "account_type": "SAVINGS",
                "account_holder": "Sam Bobley",
                "account_number": "900090009",
                "holder_zip": "10006",
                "holder_country": "US",
                "holder_state": "NY",
                "holder_city": "New York",
                "holder_address_1": "101 Greenwich St",
                "holder_address_2": "FL 23",
                "account_category": "PERSONAL ACCOUNT",
                "id": 8159849,
                "periods": [
                  {
                    "period_month_txns": {
                      "01/2020": 1
                    },
                    "period_month_days": {
                      "01/2020": 11,
                      "02/2020": 9
                    },
                    "pk": 22623169,
                    "uuid": "9fcae3d0-a848-458a-a495-7a3e77559c8b",
                    "bank_account_pk": 8159849,
                    "begin_date": "01/17/2020",
                    "end_date": "02/13/2020",
                    "begin_balance": "529.96",
                    "end_balance": "554.96",
                    "primary_recon_error_reason": "File Tampering Detected",
                    "secondary_recon_error_reason": "Tampering on pages: [1, 3, 4, 5]",
                    "uploaded_doc_pk": 34706486
                  }
                ],
                "account_holders": [
                  "Sam Bobley"
                ],
                "mca_payments_by_month": {
                  "01/2020": "0.00"
                },
                "daily_cash_flows": {
                  "01/17/2020": "0",
                  "01/18/2020": "0",
                  "01/19/2020": "0",
                  "01/20/2020": "0",
                  "01/21/2020": "0",
                  "01/22/2020": "0",
                  "01/23/2020": "0",
                  "01/24/2020": "0",
                  "01/25/2020": "25.00",
                  "01/26/2020": "0",
                  "01/27/2020": "0",
                  "01/28/2020": "0",
                  "01/29/2020": "0",
                  "01/30/2020": "0",
                  "01/31/2020": "0",
                  "02/01/2020": "0",
                  "02/02/2020": "0",
                  "02/03/2020": "0",
                  "02/04/2020": "0",
                  "02/05/2020": "0",
                  "02/06/2020": "0",
                  "02/07/2020": "0",
                  "02/08/2020": "0",
                  "02/09/2020": "0",
                  "02/10/2020": "0",
                  "02/11/2020": "0",
                  "02/12/2020": "0",
                  "02/13/2020": "0"
                },
                "outside_source_deposits": [],
                "estimated_revenue_by_month": {
                  "01/2020": "0.00"
                },
                "nsf_transactions": [],
                "average_deposit_by_month": {
                  "01/2020": "25.00"
                },
                "negative_balances_by_month": {
                  "01/2020": [],
                  "02/2020": []
                },
                "withdrawals_max_by_month": {
                  "01/2020": 'null'
                },
                "deposit_max_by_month": {
                  "01/2020": [
                    {
                      "page_idx": 4,
                      "bank_account_pk": 8159849,
                      "amount": "25.00",
                      "bbox": [
                        188,
                        2548,
                        3792,
                        2645
                      ],
                      "txn_date": "01/25/2020",
                      "page_doc_pk": 169980200,
                      "pk": 2156721594,
                      "uploaded_doc_pk": 34706486,
                      "description": "AUTOMATIC TRANSFER FROM CHK 6139 CONFIRMATION# 1327975029"
                    }
                  ]
                },
                "average_daily_balance_by_month": {
                  "01/2020": "541.63",
                  "02/2020": "554.96"
                },
                "estimated_expense_by_month": {
                  "01/2020": "0.00"
                },
                "ppp_loan_txns": [],
                "withdrawal_count": 0,
                "insurance_debits": [],
                "daily_balances": {
                  "01/17/2020": "529.96",
                  "01/18/2020": "529.96",
                  "01/19/2020": "529.96",
                  "01/20/2020": "529.96",
                  "01/21/2020": "529.96",
                  "01/22/2020": "529.96",
                  "01/23/2020": "529.96",
                  "01/24/2020": "529.96",
                  "01/25/2020": "554.96",
                  "01/26/2020": "554.96",
                  "01/27/2020": "554.96",
                  "01/28/2020": "554.96",
                  "01/29/2020": "554.96",
                  "01/30/2020": "554.96",
                  "01/31/2020": "554.96",
                  "02/01/2020": "554.96",
                  "02/02/2020": "554.96",
                  "02/03/2020": "554.96",
                  "02/04/2020": "554.96",
                  "02/05/2020": "554.96",
                  "02/06/2020": "554.96",
                  "02/07/2020": "554.96",
                  "02/08/2020": "554.96",
                  "02/09/2020": "554.96",
                  "02/10/2020": "554.96",
                  "02/11/2020": "554.96",
                  "02/12/2020": "554.96",
                  "02/13/2020": "554.96"
                },
                "round_number_txns": [],
                "deposits_count_by_month": {
                  "01/2020": 1
                },
                "deposits_sum_by_month": {
                  "01/2020": "25.00"
                },
                "alt_lender_payments_by_month": {
                  "01/2020": "0.00"
                },
                "period_balance_mismatches": [],
                "txn_count": 1,
                "total_days": 28,
                "withdrawal_sum": "0",
                "average_daily_balance": "547.82",
                "insurance_credits": [],
                "deposit_sum": "25.00",
                "alternative_lender_transactions": [],
                "deposit_count": 1,
                "minimum_balance_by_month": {
                  "01/2020": "529.96",
                  "02/2020": "554.96"
                },
                "interbank_transactions": [],
                "deposit_min_by_month": {
                  "01/2020": [
                    {
                      "page_idx": 4,
                      "bank_account_pk": 8159849,
                      "amount": "25.00",
                      "bbox": [
                        188,
                        2548,
                        3792,
                        2645
                      ],
                      "txn_date": "01/25/2020",
                      "page_doc_pk": 169980200,
                      "pk": 2156721594,
                      "uploaded_doc_pk": 34706486,
                      "description": "AUTOMATIC TRANSFER FROM CHK 6139 CONFIRMATION# 1327975029"
                    }
                  ]
                },
                "withdrawals_sum_by_month": {
                  "01/2020": "0.00"
                },
                "average_by_month": {
                  "01/2020": "25.00"
                }
              }
            ],
            "book_uuid": "faeca992-bc1c-4f72-be8f-408c0b8e72e9"
          }





    transaction_response =  {
    "txns": [
      {
        "page_idx": 4,
        "bank_account_pk": 8164269,
        "amount": "25.00",
        "bbox": [
          188,
          2548,
          3792,
          2645
        ],
        "txn_date": "01/25/2020",
        "page_doc_pk": 170120326,
        "pk": 2158262125,
        "uploaded_doc_pk": 34725634,
        "description": "AUTOMATIC TRANSFER FROM CHK 6139 CONFIRMATION# 1327975029",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'true',
        "tags": {}
      },
      {
        "page_idx": 2,
        "bank_account_pk": 8164270,
        "amount": "3433.13",
        "bbox": [
          231,
          2664,
          3763,
          2747
        ],
        "txn_date": "01/17/2020",
        "page_doc_pk": 170120329,
        "pk": 2158262113,
        "uploaded_doc_pk": 34725634,
        "description": "INSIKT INC DES:DEPOSIT ID 350209 CAPGEMINI AMERICA INC CO ID:11775843 PPD",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 3,
        "bank_account_pk": 8164270,
        "amount": "-1510.00",
        "bbox": [
          233,
          1764,
          3751,
          1846
        ],
        "txn_date": "01/24/2020",
        "page_doc_pk": 170120327,
        "pk": 2158262119,
        "uploaded_doc_pk": 34725634,
        "description": "BANK OF AMERICA CREDIT CARD BILL PAYMENT",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 3,
        "bank_account_pk": 8164270,
        "amount": "-200.00",
        "bbox": [
          233,
          888,
          3753,
          970
        ],
        "txn_date": "01/24/2020",
        "page_doc_pk": 170120327,
        "pk": 2158262116,
        "uploaded_doc_pk": 34725634,
        "description": "BKOFAMERICA ATM 01 /24 #000007230 WITHDRWL CANOGA PARK CANOGA PARK CA",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 3,
        "bank_account_pk": 8164270,
        "amount": "-184.46",
        "bbox": [
          233,
          2069,
          3785,
          2222
        ],
        "txn_date": "01/25/2020",
        "page_doc_pk": 170120327,
        "pk": 2158262121,
        "uploaded_doc_pk": 34725634,
        "description": "AMERICAN EXPRESS DES:ACH PMT ID:W0914 INDN:SIRISHA CHIGURUPATI CO\nID:1133133497 WEB",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 3,
        "bank_account_pk": 8164270,
        "amount": "-25.00",
        "bbox": [
          232,
          2256,
          3752,
          2339
        ],
        "txn_date": "01/25/2020",
        "page_doc_pk": 170120327,
        "pk": 2158262122,
        "uploaded_doc_pk": 34725634,
        "description": "AUTOMATIC TRANSFER TO CHK 8976 CONFIRMATION# 1327975029",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 3,
        "bank_account_pk": 8164270,
        "amount": "-293.13",
        "bbox": [
          233,
          1881,
          3753,
          2034
        ],
        "txn_date": "01/25/2020",
        "page_doc_pk": 170120327,
        "pk": 2158262120,
        "uploaded_doc_pk": 34725634,
        "description": "AMERICAN EXPRESS DES:ACH PMT ID:WL 674 INDN:SIRISHA CHIGURUPATI CO\nID:1133133497 WEB",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 3,
        "bank_account_pk": 8164270,
        "amount": "-1954.90",
        "bbox": [
          233,
          2374,
          3752,
          2526
        ],
        "txn_date": "01/28/2020",
        "page_doc_pk": 170120327,
        "pk": 2158262123,
        "uploaded_doc_pk": 34725634,
        "description": "CITI CARD ONLINE DES:PAYMENT ID:132867132295963 INDN:SIRISHA CHIGURUPATI CO\nID:CITICTP WEB",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 2,
        "bank_account_pk": 8164270,
        "amount": "3664.67",
        "bbox": [
          232,
          2782,
          3751,
          2866
        ],
        "txn_date": "01/31/2020",
        "page_doc_pk": 170120329,
        "pk": 2158262114,
        "uploaded_doc_pk": 34725634,
        "description": "INSIKT INC DES:DEPOSIT ID:350209 INDN:CHIGURUPATI SIRISHA CO ID:11775843 PPD",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 2,
        "bank_account_pk": 8164270,
        "amount": "3547.66",
        "bbox": [
          232,
          2900,
          3750,
          2983
        ],
        "txn_date": "01/31/2020",
        "page_doc_pk": 170120329,
        "pk": 2158262115,
        "uploaded_doc_pk": 34725634,
        "description": "INSIKT INC DES:DEPOSIT ID:350209 INDN:CHIGURUPATI SIRISHA CO ID:11775843 PPD",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 3,
        "bank_account_pk": 8164270,
        "amount": "-53.31",
        "bbox": [
          233,
          1005,
          3755,
          1087
        ],
        "txn_date": "02/04/2020",
        "page_doc_pk": 170120327,
        "pk": 2158262117,
        "uploaded_doc_pk": 34725634,
        "description": "SMART AND FINA 02/02 #000929704 PURCHASE SMART AND FINAL SIMI VALLEY CA",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 3,
        "bank_account_pk": 8164270,
        "amount": "-400.00",
        "bbox": [
          233,
          1122,
          3752,
          1205
        ],
        "txn_date": "02/05/2020",
        "page_doc_pk": 170120327,
        "pk": 2158262118,
        "uploaded_doc_pk": 34725634,
        "description": "BKOFAMERICA ATM 02/05 #000005706 WITHDRWL CANOGA PARK CANOGA PARK CA",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      },
      {
        "page_idx": 3,
        "bank_account_pk": 8164270,
        "amount": "-78.91",
        "bbox": [
          232,
          2562,
          3752,
          2714
        ],
        "txn_date": "02/07/2020",
        "page_doc_pk": 170120327,
        "pk": 2158262124,
        "uploaded_doc_pk": 34725634,
        "description": "MOSAIC DES:SURE PAY ID:15140049758*RL INDN:KISHORE GARIKAPATI CO\nID:CSCSM59063 PPD",
        "txn_pk_duplicate_of": 'null',
        "comment": "",
        "explanation": "",
        "has_probable_transfers": 'false',
        "tags": {}
      }
    ],
    "uploaded_docs": {
      "34725633": {
        "name": "ISO_Document_9ecc3e5f817e5fc6ab2104e47e81720a.pdf",
        "status": "REJECTED",
        "pages": 1,
        "pk": 34725633,
        "uuid": "4c373733b4f8412b9dc0413112b691ad"
      },
      "34725634": {
        "name": "Bank_Statements_1cb1fea2cee07588f9c0f6b7400cd1793.pdf",
        "status": "VERIFICATION_COMPLETE",
        "pages": 6,
        "pk": 34725634,
        "uuid": "91fb20334560435596cac89b31281b4f"
      }
    },
    "bank_accounts": {
      "8164269": {
        "pk": 8164269,
        "book_pk": 15626071,
        "name": "900090009 BANK OF AMERICA SAVINGS",
        "bank_name": "BANK OF AMERICA",
        "activity_info": {
          "active": [
            {
              "start": {
                "year": 2020,
                "month": 1,
                "day": 17
              },
              "end": {
                "year": 2020,
                "month": 2,
                "day": 13
              }
            }
          ],
          "missing": []
        },
        "account_type": "SAVINGS",
        "account_holder": "Sam Bobley",
        "account_number": "900090009",
        "holder_zip": "10006",
        "holder_country": "US",
        "holder_state": "NY",
        "holder_city": "New York",
        "holder_address_1": "101 Greenwich St",
        "holder_address_2": "FL 23",
        "account_category": "PERSONAL ACCOUNT",
        "id": 8164269,
        "book_uuid": "3fd413352a65473b9e60622bed126c24",
        "periods": [
          {
            "pk": 22640106,
            "uuid": "703b2c7e-10e5-4860-859b-69c08f0b4f0f",
            "bank_account_pk": 8164269,
            "begin_date": "01/17/2020",
            "end_date": "02/13/2020",
            "begin_balance": "529.96",
            "end_balance": "554.96",
            "primary_recon_error_reason": "File Tampering Detected",
            "secondary_recon_error_reason": "Tampering on pages: [1, 3, 4, 5]",
            "uploaded_doc_pk": 34725634
          }
        ],
        "account_holders": [
          "Sam Bobley"
        ]
      },
      "8164270": {
        "pk": 8164270,
        "book_pk": 15626071,
        "name": "900090009 BANK OF AMERICA CHECKING",
        "bank_name": "BANK OF AMERICA",
        "activity_info": {
          "active": [
            {
              "start": {
                "year": 2020,
                "month": 1,
                "day": 17
              },
              "end": {
                "year": 2020,
                "month": 2,
                "day": 13
              }
            }
          ],
          "missing": []
        },
        "account_type": "CHECKING",
        "account_holder": "Sam Bobley",
        "account_number": "900090009",
        "holder_zip": "10006",
        "holder_country": "US",
        "holder_state": "NY",
        "holder_city": "New York",
        "holder_address_1": "101 Greenwich St",
        "holder_address_2": "FL 23",
        "account_category": "PERSONAL ACCOUNT",
        "id": 8164270,
        "book_uuid": "3fd413352a65473b9e60622bed126c24",
        "periods": [
          {
            "pk": 22640107,
            "uuid": "a531c4ff-1dde-41aa-8361-0b32521829da",
            "bank_account_pk": 8164270,
            "begin_date": "01/17/2020",
            "end_date": "02/13/2020",
            "begin_balance": "4339.68",
            "end_balance": "10530.87",
            "primary_recon_error_reason": "File Tampering Detected",
            "secondary_recon_error_reason": "Tampering on pages: [1, 3, 4, 5]",
            "uploaded_doc_pk": 34725634
          }
        ],
        "account_holders": [
          "Sam Bobley"
        ]
      }
    },
    "tags": {}
  }







    txn_list = []
    for trans in transaction_response['txns']:
        txn_list.append([trans['txn_date'], trans['amount'], trans['description']])


    average_daily_balance_by_month = anylitic_response['average_daily_balance_by_month'].items()

    daily_balances_weekday = anylitic_response['daily_balances_weekday'].items()

    mca_payments_by_month = anylitic_response['mca_payments_by_month'].items()

    mca_payments_total = 0
    for pay in mca_payments_by_month:
        mca_payments_total += float(pay[1])

    alt_lender_payments_by_month = anylitic_response['alt_lender_payments_by_month'].items()

    estimated_revenue_by_month = anylitic_response['estimated_revenue_by_month'].items()

    deposit_sum = anylitic_response['deposit_sum']

    withdrawal_sum = anylitic_response['withdrawal_sum']





    if request.method == 'POST':
        session.clear()
        return redirect("MCA_Public_Homepage")

    return render_template("/Funder/Advances/Pre_Funded/Bank_Analysis/bank_analysis.html", access_status=access_status, notification_count=notification_count, txn_list=txn_list, mca_payments_total=mca_payments_total, average_daily_balance_by_month=average_daily_balance_by_month, daily_balances_weekday=daily_balances_weekday, mca_payments_by_month=mca_payments_by_month, alt_lender_payments_by_month=alt_lender_payments_by_month, estimated_revenue_by_month=estimated_revenue_by_month, deposit_sum=deposit_sum, withdrawal_sum=withdrawal_sum)
