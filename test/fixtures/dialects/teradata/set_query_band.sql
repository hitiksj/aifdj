SET QUERY_BAND = 'cat=siamese;dog=akita;' 
UPDATE FOR SESSION VOLATILE;

SET QUERY_BAND = 'area=west;city=sandiego;tree=maple;flower=rose;' FOR SESSION;

SET QUERY_BAND = 'city=san diego;' UPDATE FOR SESSION;

SET QUERY_BAND='PROXYUSER=fred;'
     FOR TRANSACTION;

SET QUERY_BAND = NONE FOR TRANSACTION;

SET QUERY_BAND=NONE FOR TRANSACTION;

SET QUERY_BAND = '' FOR TRANSACTION;
