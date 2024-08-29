SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'scisketch'
AND table_type = 'BASE TABLE'
AND table_name IN (
    SELECT table_name
    FROM information_schema.columns
    WHERE table_schema = 'scisketch'
    AND column_name = 'GraphicalAbstract'
);
