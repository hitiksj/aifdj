CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062,
    [test] STATISTICAL_SEMANTICS
) KEY INDEX [KEY_INDEX];

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 'french'
) KEY INDEX [KEY_INDEX];

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] STATISTICAL_SEMANTICS
) KEY INDEX [KEY_INDEX];

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE
) KEY INDEX [KEY_INDEX];

-- catalog_filegroup_options
CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] ON [ft_catalog_name];

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] ON [ft_catalog_name], FILEGROUP [filegroup_name];

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] ON FILEGROUP [filegroup_name], [ft_catalog_name],;

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] ON FILEGROUP [filegroup_name];

-- change_tracking (MANUAL | AUTO | OFF | OFF, NO POPULATION)
CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] ON [ft_catalog_name] WITH (
    CHANGE_TRACKING MANUAL
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] ON [ft_catalog_name] WITH (
    CHANGE_TRACKING = MANUAL
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] ON [ft_catalog_name] WITH (
    CHANGE_TRACKING AUTO
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] ON [ft_catalog_name] WITH (
    CHANGE_TRACKING = AUTO
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    CHANGE_TRACKING OFF
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    CHANGE_TRACKING = OFF
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    CHANGE_TRACKING OFF, NO POPULATION
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    CHANGE_TRACKING = OFF, NO POPULATION
);

-- stoplist (OFF | SYSTEM | stoplist_name)
CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    STOPLIST OFF
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    STOPLIST = OFF
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    STOPLIST SYSTEM
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    STOPLIST = SYSTEM
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    STOPLIST [custom_stoplist_name]
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    STOPLIST = [custom_stoplist_name]
);

-- search property list
CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    SEARCH PROPERTY LIST [property_list_name]
);

CREATE FULLTEXT INDEX ON [dbo].[TEST_FULLTEXT_INDEX] (
    [id] LANGUAGE 1062
) KEY INDEX [PK_IDENTIFIER] WITH (
    SEARCH PROPERTY LIST = [property_list_name]
);
