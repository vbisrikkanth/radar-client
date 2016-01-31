TABLE_NAME="$1"

echo "CREATE TRIGGER ${TABLE_NAME}_log_changes
AFTER INSERT OR UPDATE OR DELETE ON ${TABLE_NAME}
FOR EACH ROW EXECUTE PROCEDURE log_changes()"
