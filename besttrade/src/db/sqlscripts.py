from besttrade.src.domain import Investor

all_active_investors_sql = (
    "select name, status, id from investor where status='ACTIVE'")

all_investors_sql = 'select name, status, id from investor'

new_investor_sql = (
    f"insert into investor (name, status) values (?, 'ACTIVE')")

investor_by_id_sql = (
    f'select name, status, id from investor where id=?')

update_investor_status = (f'update investor set status=? where id=?')
