test:
	./odoo-bin --addons-path="./addons" -d mydb

p:
	./odoo-bin --addons-path="./addons","./addonstokobaju" -d tokobaju -u tokobaju

run:
	./odoo-bin --addons-path="./addons","./addonstokobaju" --xmlrpc-port=8071 --db_port 5432 -d tokobaju --limit-memory-hard 0 --limit-time-real=10000 -u tokobaju

PHONY: p run test