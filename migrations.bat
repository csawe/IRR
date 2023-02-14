echo "Making migrations"
manage.py makemigrations
echo "Migrating"
manage.py migrate
echo "Done"
