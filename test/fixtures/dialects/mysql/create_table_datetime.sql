CREATE TABLE `foo` (
  created_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  ts1 TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  dt1 DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  ts2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dt2 DATETIME DEFAULT CURRENT_TIMESTAMP,
  ts3 TIMESTAMP DEFAULT 0,
  dt3 DATETIME DEFAULT 0,
  ts4 TIMESTAMP DEFAULT 0 ON UPDATE CURRENT_TIMESTAMP,
  dt4 DATETIME DEFAULT 0 ON UPDATE CURRENT_TIMESTAMP,
  ts5 TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,     -- default 0
  ts6 TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP, -- default NULL
  dt5 DATETIME ON UPDATE CURRENT_TIMESTAMP,         -- default NULL
  dt6 DATETIME NOT NULL ON UPDATE CURRENT_TIMESTAMP, -- default 0
  ts7 TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  ts8 TIMESTAMP NULL DEFAULT NULL,
  ts9 TIMESTAMP NULL DEFAULT 0,
  ts10 TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  ts11 TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  ts12 TIMESTAMP NULL DEFAULT '0000-00-00 00:00:00',
  ts13 TIMESTAMP NULL DEFAULT NOW,
  ts14 TIMESTAMP NULL DEFAULT NOW(),
  ts15 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
