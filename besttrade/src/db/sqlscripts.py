from besttrade.src.domain import Investor

all_active_investors_sql = (
    "select name, status, id from investor where status='ACTIVE'")

all_investors_sql = 'select name, status, id from investor'

new_investor_sql = (
    f"insert into investor (name, status) values (?, 'ACTIVE')")

investor_by_id_sql = (
    f'select name, status, id from investor where id=?')

update_investor_status = (f'update investor set status=? where id=?')

get_investors_by_name = (
    f'select name, status, id from investor where name =?')

update_investor_by_name = (f'update investor set name = ? where id = ?')

get_accounts = (f'select investor_id, balance, account_number from account')

get_account_by_id = (
    f'select investor_id, balance, account_number from account where account_number = ?')

get_accounts_by_investor_id = (
    f'select investor_id, balance, account_number from account where investor_id = ?')

delete_account = (f'delete from account where account_number = ?')

update_account_balance = (
    f'update account set balance = ? where account_number = ?')

create_account = (f'insert into account (investor_id, balance) values (?, ?)')
