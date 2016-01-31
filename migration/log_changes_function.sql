CREATE FUNCTION log_changes() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    DECLARE
        user_id INTEGER;
    BEGIN
        BEGIN
            user_id = current_setting('radar.user_id');
        EXCEPTION WHEN OTHERS THEN
            user_id = NULL;
        END;

        IF (TG_OP = 'UPDATE') THEN
            INSERT INTO logs (
                type,
                user_id,
                table_name,
                original_data,
                new_data,
                statement
            ) VALUES (
                'UPDATE',
                user_id,
                TG_TABLE_NAME,
                row_to_json(OLD)::jsonb,
                row_to_json(NEW)::jsonb,
                current_query()
            );
            RETURN NEW;
        ELSIF (TG_OP = 'DELETE') THEN
            INSERT INTO logs (
                type,
                user_id,
                table_name,
                original_data,
                statement
            ) VALUES (
                'DELETE',
                user_id,
                TG_TABLE_NAME,
                row_to_json(OLD)::jsonb,
                current_query()
            );
            RETURN OLD;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO logs (
                type,
                user_id,
                table_name,
                new_data,
                statement
            ) VALUES (
                'INSERT',
                user_id,
                TG_TABLE_NAME,
                row_to_json(NEW)::jsonb,
                current_query()
            );
            RETURN NEW;
        ELSE
            RAISE WARNING '[log_action] Unknown action: % at %', TG_OP, now();
            RETURN NULL;
        END IF;
    END;
    $$;
