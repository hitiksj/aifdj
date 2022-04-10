CREATE OR REPLACE EXTERNAL FUNCTION LOCAL_ECHO(STRING_COL VARCHAR)
    RETURNS VARIANT
    API_INTEGRATION = DEMONSTRATION_EXTERNAL_API_INTEGRATION_01
    AS 'https://xyz.execute-api.us-west-2.amazonaws.com/prod/remote_echo'
;
CREATE OR REPLACE EXTERNAL FUNCTION MY_SCHEMA.LOCAL_ECHO(STRING_COL VARCHAR)
    RETURNS VARIANT
    NOT NULL
    STRICT
    VOLATILE
    API_INTEGRATION = DEMONSTRATION_EXTERNAL_API_INTEGRATION_01
    HEADERS = (
        'volume-measure' = 'liters',
        'distance-measure' = 'kilometers'
    )
    CONTEXT_HEADERS = (CURRENT_TIMESTAMP)
    MAX_BATCH_ROWS = 50
    COMPRESSION = NONE
    REQUEST_TRANSLATOR = UTILITY.SOME_FUNCTION
    RESPONSE_TRANSLATOR = UTILITY.SOME_FUNCTION
    AS 'https://xyz.execute-api.us-west-2.amazonaws.com/prod/remote_echo'
;
CREATE OR REPLACE EXTERNAL FUNCTION MY_SCHEMA.LOCAL_ECHO(STRING_COL VARCHAR)
    RETURNS VARIANT
    NOT NULL
    RETURNS NULL ON NULL INPUT
    VOLATILE
    API_INTEGRATION = DEMONSTRATION_EXTERNAL_API_INTEGRATION_01
    HEADERS = (
        'volume-measure' = 'liters',
        'distance-measure' = 'kilometers'
    )
    CONTEXT_HEADERS = (CURRENT_TIMESTAMP)
    MAX_BATCH_ROWS = 50
    COMPRESSION = NONE
    REQUEST_TRANSLATOR = UTILITY.SOME_FUNCTION
    RESPONSE_TRANSLATOR = UTILITY.SOME_FUNCTION
    AS 'https://xyz.execute-api.us-west-2.amazonaws.com/prod/remote_echo'
;
CREATE OR REPLACE EXTERNAL FUNCTION MY_SCHEMA.LOCAL_ECHO(OBJ OBJECT)
    RETURNS VARCHAR
    NULL
    CALLED ON NULL INPUT
    IMMUTABLE
    COMMENT = 'SQLFluff rocks!'
    API_INTEGRATION = DEMONSTRATION_EXTERNAL_API_INTEGRATION_01
    HEADERS = (
        'volume-measure' = 'liters',
        'distance-measure' = 'kilometers'
    )
    CONTEXT_HEADERS = (CURRENT_TIMESTAMP)
    MAX_BATCH_ROWS = 50
    COMPRESSION = NONE
    REQUEST_TRANSLATOR = UTILITY.SOME_FUNCTION
    RESPONSE_TRANSLATOR = UTILITY.SOME_FUNCTION
    AS 'https://xyz.execute-api.us-west-2.amazonaws.com/prod/remote_echo'
;